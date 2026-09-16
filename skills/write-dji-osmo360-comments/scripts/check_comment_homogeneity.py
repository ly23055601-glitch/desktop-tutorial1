#!/usr/bin/env python3
"""Audit Osmo 360 pure-comment Markdown for structure and repeated writing patterns."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit


SECTION_RE = re.compile(
    r"^##\s+(?:(?P<number>\d+)\s*[｜|]\s*)?(?P<url>https?://\S+)(?:\s.*)?$",
    re.IGNORECASE,
)
MAIN_NUMBER_RE = re.compile(r"^\s*(?P<number>[1-9]\d*)\.\s*(?P<text>\S.*?)\s*$")
MAIN_LABEL_RE = re.compile(r"^\s*主评论\s*[：:]\s*(?P<text>.+?)\s*$")
REPLY_RE = re.compile(r"^\s*↳\s*(?:回复\s*\d*\s*[：:]\s*)?(?P<text>.+?)\s*$")

# Longest and most specific alternatives come first so one surface expression is
# counted once. A bare generation number must stand alone; without this
# boundary, strings such as "Osmo 360 24fps" are incorrectly read as generation 2.
SECOND_GEN_SUFFIX = r"(?:II(?![A-Za-z0-9])|二代|2(?=$|[\s，,。.!！?？、/|｜)）\]】]))"
PRODUCT_RE = re.compile(
    rf"(?:DJI\s*Osmo\s*360\s*{SECOND_GEN_SUFFIX}|"
    rf"大疆\s*(?:Osmo\s*)?360\s*{SECOND_GEN_SUFFIX}|"
    rf"Osmo\s*360\s*{SECOND_GEN_SUFFIX}|"
    r"360\s*二代|这台二代|"
    r"DJI\s*Osmo\s*360|大疆\s*Osmo\s*360|Osmo\s*360|大疆\s*360|"
    r"这台全景机|这个小相机|360画面|全景视角|这个模式|全景素材)",
    re.IGNORECASE,
)
SECOND_GEN_CLAIM_RE = re.compile(
    r"(?:第二代|第?\d+代|二代|Ⅱ|(?<![A-Za-z])II(?![A-Za-z0-9])|"
    r"(?:DJI\s*)?(?:Osmo\s*360|大疆\s*(?:Osmo\s*)?360)\s*"
    r"(?:II[A-Za-z0-9]+|I{3,}[A-Za-z0-9]*|[2-9]\d*))",
    re.IGNORECASE,
)
NORMALIZED_SECOND_GEN_RE = re.compile(
    r"(?:Osmo360II(?![A-Za-z0-9])|360二代(?![A-Za-z0-9])|这台二代(?![A-Za-z0-9]))",
    re.IGNORECASE,
)
GENERIC_PRODUCT_TERMS = {"这个模式", "全景素材", "全景视角", "360画面"}

BANNED_STYLE = (
    "本质上",
    "这说明",
    "产品价值",
    "核心优势",
    "适合哪类人",
    "适合谁",
    "真正需要的是",
    "行程闭环",
    "分水岭",
)
TEMPLATE_FAMILIES = {
    "expect_twist": re.compile(r"(?:我还以为|本来以为|刚想|正准备).{0,24}(?:结果|没想到|却)"),
    "before_next": re.compile(r"前面.{0,24}下一秒"),
    "what_is_this": re.compile(r"这哪是.{0,24}(?:这是|分明是|明明是|简直是)"),
    "role_colon": re.compile(r"^[\u4e00-\u9fffA-Za-z]{1,8}[：:]"),
    "stock_slang": re.compile(r"我宣布|谁懂|直接封神|DNA动了", re.IGNORECASE),
    "body_triplet": re.compile(r"手上.{0,20}脚下.{0,20}前面|脚下.{0,20}手上.{0,20}前面"),
}
MOMENT_RE = re.compile(r"(?:这|那)(?:一下|一秒|一张|张|一段|段|一格|格|一帧|帧)|最后")
REACTION_RE = re.compile(r"我(?:的)?第一反应|我下意识|我暂停|我反而|我偏偏|比.{0,12}更抢眼")
TRIPLE_RE = re.compile(
    r"(?:把|从).{0,28}(?:、|/).{0,22}(?:、|/).{0,22}|"
    r"(?:把|从).{0,18}，.{0,18}，.{0,22}(?:都|全|留|收|拍|带)"
)


@dataclass
class Item:
    file: str
    line: int
    section: str
    url: str
    group: int
    role: str
    text: str
    trailing_spaces: str = ""


@dataclass
class Group:
    main: Item
    replies: list[Item] = field(default_factory=list)


@dataclass
class Section:
    file: str
    line: int
    number: str
    url: str
    groups: list[Group] = field(default_factory=list)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def word_chars(text: str) -> str:
    return "".join(
        char
        for char in clean(text).lower()
        if unicodedata.category(char)[0] in {"L", "N"} or "\u4e00" <= char <= "\u9fff"
    )


def product_mentions(text: str) -> list[str]:
    mentions = [re.sub(r"\s+", "", match.group(0)).lower() for match in PRODUCT_RE.finditer(text)]
    named_mentions = [mention for mention in mentions if mention not in GENERIC_PRODUCT_TERMS]
    return named_mentions or mentions


def trailing_body_spaces(line: str) -> str:
    return line[len(line.rstrip(" \u3000")) :]


def has_nonstandard_second_gen_name(text: str) -> bool:
    return bool(SECOND_GEN_CLAIM_RE.search(NORMALIZED_SECOND_GEN_RE.sub("", text)))


def scaffold(text: str) -> str:
    value = PRODUCT_RE.sub("", clean(text).lower())
    value = re.sub(r"\d+(?:\.\d+)?", "数字", value)
    return word_chars(value)


def prefix(text: str, size: int = 6) -> str:
    return scaffold(text)[:size]


def shingles(text: str, size: int = 3) -> set[str]:
    if len(text) < size:
        return set()
    return {text[index : index + size] for index in range(len(text) - size + 1)}


def dice(left: str, right: str, size: int = 3) -> float:
    a, b = shingles(left, size), shingles(right, size)
    if not a or not b:
        return 0.0
    return 2 * len(a & b) / (len(a) + len(b))


def similarity(left: str, right: str) -> tuple[float, float]:
    return dice(left, right), difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()


def diagnostic(severity: str, code: str, message: str, item: Item | Section | None = None, **extra) -> dict:
    result = {"severity": severity, "code": code, "message": message}
    if item is not None:
        result["location"] = {
            "file": item.file,
            "line": item.line,
            "section": item.section if isinstance(item, Item) else item.number,
            "group": item.group if isinstance(item, Item) else None,
        }
    result.update(extra)
    return result


def collect_paths(values: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for value in values:
        path = Path(value).expanduser()
        if path.is_file():
            paths.add(path.resolve())
        elif path.is_dir():
            paths.update(item.resolve() for item in path.rglob("*.md") if item.is_file())
        else:
            raise FileNotFoundError(value)
    return sorted(paths)


def parse_file(path: Path) -> tuple[list[Section], list[dict]]:
    sections: list[Section] = []
    diagnostics: list[dict] = []
    current: Section | None = None
    current_group: Group | None = None
    in_fence = False

    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue

        section_match = SECTION_RE.match(line)
        if section_match:
            number = section_match.group("number") or str(len(sections) + 1)
            current = Section(str(path), line_number, number, section_match.group("url"))
            current_group = None
            sections.append(current)
            continue

        main_match = MAIN_NUMBER_RE.match(line) or MAIN_LABEL_RE.match(line)
        if main_match:
            if current is None:
                diagnostics.append(diagnostic("error", "E_ORPHAN_MAIN", "主评论位于链接章节之外"))
                continue
            item = Item(
                str(path),
                line_number,
                current.number,
                current.url,
                len(current.groups) + 1,
                "main",
                main_match.group("text"),
                trailing_body_spaces(line),
            )
            current_group = Group(item)
            current.groups.append(current_group)
            continue

        reply_match = REPLY_RE.match(line)
        if reply_match:
            if current is None or current_group is None:
                diagnostics.append(diagnostic("error", "E_ORPHAN_REPLY", "楼中楼没有对应主评论"))
                continue
            current_group.replies.append(
                Item(
                    str(path),
                    line_number,
                    current.number,
                    current.url,
                    current_group.main.group,
                    "reply",
                    reply_match.group("text"),
                    trailing_body_spaces(line),
                )
            )

    return sections, diagnostics


def parse_paths(paths: list[Path]) -> tuple[list[Section], list[dict]]:
    sections: list[Section] = []
    diagnostics: list[dict] = []
    for path in paths:
        found, issues = parse_file(path)
        if not found:
            issues.append(
                diagnostic("error", "E_NO_SECTIONS", f"输入文件未解析出任何链接章节：{path}", file=str(path))
            )
        sections.extend(found)
        diagnostics.extend(issues)
    return sections, diagnostics


def section_identifiers(section: Section) -> set[str]:
    """Return explicit identifiers accepted by --allow-second-gen-id."""

    parsed = urlsplit(section.url)
    canonical_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
    content_id = parsed.path.rstrip("/").split("/")[-1]
    identifiers = {section.number, section.number.lstrip("0") or "0", section.url, canonical_url}
    if content_id:
        identifiers.add(content_id)
    return identifiers


def audit_structure(
    sections: list[Section],
    diagnostics: list[dict],
    product_policy: str,
    allow_second_gen: bool,
    second_generation_allowed_ids: set[str],
) -> dict:
    patterns: list[str] = []
    product_starts = 0
    product_mains = 0
    all_mains = 0

    for section in sections:
        section_allows_second_gen = allow_second_gen or bool(
            section_identifiers(section) & second_generation_allowed_ids
        )
        if len(section.groups) != 3:
            diagnostics.append(diagnostic("error", "E_GROUP_COUNT", f"每个链接应有3组，实际为{len(section.groups)}组", section))

        pattern = []
        expressions: list[str] = []
        for group in section.groups:
            all_mains += 1
            reply_count = len(group.replies)
            if not 2 <= reply_count <= 4:
                diagnostics.append(
                    diagnostic("error", "E_REPLY_COUNT", f"每组应有2–4条回复，实际为{reply_count}条", group.main)
                )

            mentions = product_mentions(group.main.text)
            if len(mentions) > 1:
                diagnostics.append(diagnostic("error", "E_PRODUCT_STACK", "一条主评论出现多个产品称呼", group.main, matches=mentions))
            if mentions:
                pattern.append("P")
                product_mains += 1
                expressions.append(mentions[0])
                match = PRODUCT_RE.search(group.main.text)
                if match and len(word_chars(group.main.text[: match.start()])) < 6:
                    product_starts += 1
                if mentions[0] in GENERIC_PRODUCT_TERMS:
                    diagnostics.append(
                        diagnostic("warning", "W_GENERIC_PRODUCT_TERM", "通用产品称呼需人工确认上下文确实指向 Osmo 360", group.main)
                    )
            else:
                pattern.append("C")

            for item in [group.main, *group.replies]:
                half_width_spaces = item.text.count(" ") + item.trailing_spaces.count(" ")
                full_width_spaces = item.text.count("\u3000") + item.trailing_spaces.count("\u3000")
                if half_width_spaces or full_width_spaces:
                    diagnostics.append(
                        diagnostic(
                            "error",
                            "E_BODY_SPACE",
                            "主评论和楼中楼正文不得出现半角或全角空格",
                            item,
                            role=item.role,
                            half_width_spaces=half_width_spaces,
                            full_width_spaces=full_width_spaces,
                        )
                    )
                if item.role == "reply" and len(product_mentions(item.text)) > 1:
                    diagnostics.append(diagnostic("error", "E_PRODUCT_STACK", "同一条评论出现多个产品称呼", item))
                if has_nonstandard_second_gen_name(item.text):
                    diagnostics.append(
                        diagnostic(
                            "error",
                            "E_SECOND_GEN_NAME_FORMAT",
                            "代际称呼须写作Osmo360II、360二代或有明确指代的这台二代",
                            item,
                        )
                    )
                if SECOND_GEN_CLAIM_RE.search(item.text) and not section_allows_second_gen:
                    diagnostics.append(
                        diagnostic(
                            "error",
                            "E_SECOND_GEN_EVIDENCE",
                            "出现 II/二代；仅在链接证据已确认时用 --allow-second-gen-id 放行该链接",
                            item,
                        )
                    )
                for phrase in BANNED_STYLE:
                    if phrase in item.text:
                        diagnostics.append(diagnostic("error", "E_SUMMARY_TONE", f"命中策划总结腔：{phrase}", item))
                if TRIPLE_RE.search(item.text):
                    diagnostics.append(diagnostic("warning", "W_TRIPLE_LIST", "可能存在三连景或三连动作，请人工复读", item))

        slot_pattern = "".join(pattern)
        patterns.append(slot_pattern)
        if product_policy != "off":
            severity = "error" if product_policy == "strict" else "warning"
            if pattern.count("P") != 2:
                diagnostics.append(
                    diagnostic(severity, "E_PRODUCT_MAIN_COUNT" if severity == "error" else "W_PRODUCT_MAIN_COUNT", f"应有2条产品主评，实际排列为{slot_pattern}", section)
                )
            elif slot_pattern != "PPC":
                diagnostics.append(
                    diagnostic(
                        severity,
                        "E_PRODUCT_SLOT_ORDER" if severity == "error" else "W_PRODUCT_SLOT_ORDER",
                        f"产品槽位应固定为PPC，实际为{slot_pattern}",
                        section,
                    )
                )
            if len(expressions) == 2 and expressions[0] == expressions[1]:
                diagnostics.append(
                    diagnostic(severity, "E_PRODUCT_TERM_REPEAT" if severity == "error" else "W_PRODUCT_TERM_REPEAT", "两条产品主评使用了相同称呼", section, expression=expressions[0])
                )

        if len(section.groups) == 3:
            counts = [len(group.replies) for group in section.groups]
            if len(set(counts)) == 1:
                diagnostics.append(diagnostic("warning", "W_REPLY_COUNTS_LOCAL", f"同一链接三组回复数完全一致：{counts}", section))
            if all("，" in group.main.text or "," in group.main.text for group in section.groups):
                diagnostics.append(diagnostic("warning", "W_COMMA_LOCAL", "同一链接三条主评都使用逗号骨架", section))

    if all_mains >= 12 and product_starts / all_mains > 0.35:
        diagnostics.append(
            diagnostic("warning", "W_PRODUCT_START_DENSITY", "产品称呼出现在句首附近的比例过高", ratio=round(product_starts / all_mains, 3))
        )

    return {"product_slot_patterns": Counter(patterns), "product_main_count": product_mains}


def audit_repetition(sections: list[Section], diagnostics: list[dict]) -> None:
    mains = [group.main for section in sections for group in section.groups]
    replies = [reply for section in sections for group in section.groups for reply in group.replies]

    for role, items in (("main", mains), ("reply", replies)):
        exact: dict[str, list[Item]] = defaultdict(list)
        canonical: dict[str, list[Item]] = defaultdict(list)
        for item in items:
            exact[word_chars(item.text)].append(item)
            canonical[scaffold(item.text)].append(item)
        for value, matches in exact.items():
            if value and len(matches) > 1:
                severity = "error" if role == "main" else "warning"
                diagnostics.append(
                    diagnostic(severity, "E_EXACT_MAIN" if role == "main" else "W_EXACT_REPLY", f"发现重复{ '主评论' if role == 'main' else '回复' }", matches[-1], count=len(matches))
                )
        if role == "main":
            for value, matches in canonical.items():
                if len(value) >= 8 and len(matches) > 1 and len({word_chars(item.text) for item in matches}) > 1:
                    diagnostics.append(
                        diagnostic("error", "E_PRODUCT_SWAP_DUP", "主评论只更换了产品词、数字或标点", matches[-1], count=len(matches))
                    )

    prepared = [(item, scaffold(item.text)) for item in mains]
    for index, (left_item, left) in enumerate(prepared):
        if len(left) < 12:
            continue
        for right_item, right in prepared[index + 1 :]:
            if len(right) < 12:
                continue
            if min(len(left), len(right)) / max(len(left), len(right)) < 0.68:
                continue
            score_dice, score_sequence = similarity(left, right)
            same_section = left_item.file == right_item.file and left_item.section == right_item.section
            threshold = (0.58, 0.78) if same_section else (0.68, 0.84)
            if score_dice >= threshold[0] and score_sequence >= threshold[1]:
                diagnostics.append(
                    diagnostic(
                        "warning",
                        "W_LOCAL_MAIN_OVERLAP" if same_section else "W_NEAR_MAIN",
                        "同一链接主评关注点可能重复" if same_section else "跨链接主评骨架近似",
                        right_item,
                        compared_with={"file": left_item.file, "line": left_item.line, "section": left_item.section, "group": left_item.group},
                        dice=round(score_dice, 3),
                        sequence=round(score_sequence, 3),
                    )
                )

    for section in sections:
        section_mains = [group.main for group in section.groups]
        for group in section.groups:
            for reply in group.replies:
                reply_text = scaffold(reply.text)
                if len(reply_text) < 10:
                    continue
                for main in section_mains:
                    main_text = scaffold(main.text)
                    if len(main_text) < 10:
                        continue
                    score_dice, score_sequence = similarity(reply_text, main_text)
                    if score_dice >= 0.58 and score_sequence >= 0.76:
                        diagnostics.append(
                            diagnostic(
                                "warning",
                                "W_REPLY_RESTATES_MAIN",
                                "楼中楼可能复述本组或另一组主评",
                                reply,
                                compared_with={"line": main.line, "group": main.group},
                                dice=round(score_dice, 3),
                                sequence=round(score_sequence, 3),
                            )
                        )


def audit_batch_patterns(sections: list[Section], diagnostics: list[dict]) -> dict:
    mains = [group.main for section in sections for group in section.groups]
    opening_map: dict[str, list[Item]] = defaultdict(list)
    family_map: dict[str, list[Item]] = defaultdict(list)
    reply_combos: list[tuple[int, ...]] = []

    for item in mains:
        opening = prefix(item.text)
        if len(opening) >= 4:
            opening_map[opening].append(item)
        for family, pattern in TEMPLATE_FAMILIES.items():
            if pattern.search(item.text):
                family_map[family].append(item)

    for opening, matches in opening_map.items():
        section_ids = {(item.file, item.section) for item in matches}
        if len(section_ids) >= 3:
            diagnostics.append(
                diagnostic("warning", "W_OPENING_REPEAT", f"去产品词后前6字“{opening}”跨3个以上链接重复", matches[-1], count=len(matches))
            )

    for family, matches in family_map.items():
        section_ids = {(item.file, item.section) for item in matches}
        if len(section_ids) >= 3:
            diagnostics.append(
                diagnostic("warning", "W_TEMPLATE_FAMILY", f"人工句型 {family} 跨3个以上链接重复", matches[-1], count=len(matches))
            )

    for section in sections:
        combo = tuple(len(group.replies) for group in section.groups)
        reply_combos.append(combo)
    for index in range(len(reply_combos) - 2):
        if reply_combos[index] == reply_combos[index + 1] == reply_combos[index + 2]:
            diagnostics.append(
                diagnostic("warning", "W_REPLY_COMBO_RUN", f"连续3个链接使用相同回复数组合 {reply_combos[index]}", sections[index])
            )
            break

    moment_count = sum(bool(MOMENT_RE.search(item.text)) for item in mains)
    reaction_count = sum(bool(REACTION_RE.search(item.text)) for item in mains)
    if len(mains) >= 15 and moment_count / len(mains) > 0.20:
        diagnostics.append(
            diagnostic("warning", "W_MOMENT_DENSITY", "“这段/那一下/最后”等观看指示词过密", ratio=round(moment_count / len(mains), 3))
        )
    if len(mains) >= 15 and reaction_count / len(mains) > 0.10:
        diagnostics.append(
            diagnostic("warning", "W_REACTION_DENSITY", "“第一反应/下意识/反而”等观看套语过密", ratio=round(reaction_count / len(mains), 3))
        )

    comma_count = sum("，" in item.text or "," in item.text for item in mains)
    if len(mains) >= 15 and comma_count / len(mains) > 0.75:
        diagnostics.append(
            diagnostic("warning", "W_COMMA_DENSITY", "含逗号的主评比例过高，可能形成统一作文句形", ratio=round(comma_count / len(mains), 3))
        )

    return {
        "opening_prefixes": Counter(prefix(item.text) for item in mains if len(prefix(item.text)) >= 4),
        "template_families": Counter(
            family for item in mains for family, pattern in TEMPLATE_FAMILIES.items() if pattern.search(item.text)
        ),
        "reply_count_patterns": Counter(reply_combos),
    }


def audit_baseline(current: list[Section], baseline: list[Section], diagnostics: list[dict]) -> None:
    old_mains = [group.main for section in baseline for group in section.groups]
    if not old_mains:
        return
    exact = {word_chars(item.text): item for item in old_mains}
    canonical = {scaffold(item.text): item for item in old_mains}
    for section in current:
        for group in section.groups:
            item = group.main
            raw = word_chars(item.text)
            stripped = scaffold(item.text)
            if raw in exact:
                diagnostics.append(diagnostic("error", "E_BASELINE_EXACT", "主评与历史成品完全相同", item))
                continue
            if len(stripped) >= 8 and stripped in canonical:
                diagnostics.append(diagnostic("error", "E_BASELINE_PRODUCT_SWAP", "主评与历史成品相比只更换产品词或数字", item))
                continue
            if len(stripped) < 12:
                continue
            best: tuple[float, float] = (0.0, 0.0)
            for old in old_mains:
                old_text = scaffold(old.text)
                if len(old_text) < 12:
                    continue
                if min(len(stripped), len(old_text)) / max(len(stripped), len(old_text)) < 0.68:
                    continue
                scores = similarity(stripped, old_text)
                if sum(scores) > sum(best):
                    best = scores
            if best[0] >= 0.70 and best[1] >= 0.85:
                diagnostics.append(
                    diagnostic("warning", "W_BASELINE_NEAR", "主评与历史成品骨架近似", item, dice=round(best[0], 3), sequence=round(best[1], 3))
                )


def jsonable_counter(value):
    return {str(key): count for key, count in value.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="当前批次 Markdown 文件或目录")
    parser.add_argument("--baseline", action="append", default=[], help="最近成品 Markdown，可重复传入")
    parser.add_argument("--product-policy", choices=("strict", "advisory", "off"), default="strict")
    parser.add_argument(
        "--allow-second-gen-id",
        action="append",
        default=[],
        metavar="ID",
        help="链接证据已确认 II/二代时使用；可传能唯一命中的原序号、作品ID或规范链接，可重复",
    )
    parser.add_argument(
        "--allow-second-gen",
        action="store_true",
        help="仅兼容单链接检查；批量必须使用 --allow-second-gen-id",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--max-examples", type=int, default=3)
    args = parser.parse_args()

    try:
        current_paths = collect_paths(args.inputs)
        baseline_paths = collect_paths(args.baseline) if args.baseline else []
    except FileNotFoundError as exc:
        print(f"找不到输入：{exc}", file=sys.stderr)
        return 2

    sections, diagnostics = parse_paths(current_paths)
    baseline, baseline_diagnostics = parse_paths(baseline_paths)
    if not current_paths:
        diagnostics.append(diagnostic("error", "E_NO_INPUT_FILES", "输入中没有可检查的 Markdown 文件"))
    if args.baseline and not baseline_paths:
        diagnostics.append(diagnostic("error", "E_NO_BASELINE_FILES", "baseline 中没有可检查的 Markdown 文件"))
    diagnostics.extend(issue for issue in baseline_diagnostics if issue["severity"] == "error")
    allowed_ids = {value.strip() for value in args.allow_second_gen_id if value.strip()}
    global_second_gen = args.allow_second_gen and len(sections) == 1
    if args.allow_second_gen and len(sections) != 1:
        diagnostics.append(
            diagnostic(
                "error",
                "E_SECOND_GEN_GLOBAL_BATCH",
                "--allow-second-gen 只可用于单链接；批量请按链接重复使用 --allow-second-gen-id",
            )
        )
    unique_allowed_ids: set[str] = set()
    for allowed_id in sorted(allowed_ids):
        matches = [section for section in sections if allowed_id in section_identifiers(section)]
        if not matches:
            diagnostics.append(
                diagnostic("error", "E_SECOND_GEN_ALLOW_ID_UNKNOWN", f"二代放行 ID 未匹配任何链接：{allowed_id}")
            )
        elif len(matches) > 1:
            diagnostics.append(
                diagnostic(
                    "error",
                    "E_SECOND_GEN_ALLOW_ID_AMBIGUOUS",
                    f"二代放行 ID 匹配到{len(matches)}个链接，请改用唯一作品ID或规范链接：{allowed_id}",
                )
            )
        else:
            unique_allowed_ids.add(allowed_id)
    structure_metrics = audit_structure(
        sections,
        diagnostics,
        args.product_policy,
        global_second_gen,
        unique_allowed_ids,
    )
    audit_repetition(sections, diagnostics)
    batch_metrics = audit_batch_patterns(sections, diagnostics)
    audit_baseline(sections, baseline, diagnostics)

    errors = [item for item in diagnostics if item["severity"] == "error"]
    warnings = [item for item in diagnostics if item["severity"] == "warning"]
    metrics = {
        "files": len(current_paths),
        "links": len(sections),
        "main_comments": sum(len(section.groups) for section in sections),
        "replies": sum(len(group.replies) for section in sections for group in section.groups),
        "errors": len(errors),
        "warnings": len(warnings),
        "product_main_count": structure_metrics["product_main_count"],
        "product_slot_patterns": jsonable_counter(structure_metrics["product_slot_patterns"]),
        "reply_count_patterns": jsonable_counter(batch_metrics["reply_count_patterns"]),
    }

    if args.format == "json":
        print(json.dumps({"metrics": metrics, "diagnostics": diagnostics}, ensure_ascii=False, indent=2))
    else:
        print(
            f"links={metrics['links']} mains={metrics['main_comments']} replies={metrics['replies']} "
            f"errors={metrics['errors']} warnings={metrics['warnings']}"
        )
        grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for item in diagnostics:
            grouped[(item["severity"], item["code"])].append(item)
        for (severity, code), items in sorted(grouped.items()):
            print(f"{severity.upper()} {code} x{len(items)}: {items[0]['message']}")
            for item in items[: max(args.max_examples, 0)]:
                location = item.get("location")
                if location:
                    print(
                        f"  - {location['file']}:{location['line']} "
                        f"section={location['section']} group={location['group']}"
                    )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
