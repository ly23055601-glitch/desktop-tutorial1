#!/usr/bin/env python3
"""Audit DJI Mic comment drafts for structure, repetition, and staged AI patterns."""

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


SECTION_RE = re.compile(r"^##\s*(\d+)\s*(?:[.．、｜|]\s*)?(.*?)\s*$")
LABELED_MAIN_RE = re.compile(r"^\s*主评论\s*[：:]\s*(.+?)\s*$")
NUMBERED_MAIN_RE = re.compile(r"^\s*([1-3])\s*[.．、]\s+(.+?)\s*$")
LABELED_REPLY_RE = re.compile(r"^\s*↳\s*回复\s*(\d+)?\s*[：:]\s*(.+?)\s*$")
PLAIN_REPLY_RE = re.compile(r"^\s*↳\s*(.+?)\s*$")

MODEL = r"(?:Mini\s*2S|Mini\s*2|Mini|2|3)"
FULL_PRODUCT_RE = re.compile(rf"(?:(?:DJI|大疆)\s*Mic\s*{MODEL})", re.IGNORECASE)
PRODUCT_NAME_RE = re.compile(
    rf"(?:(?:DJI|大疆)\s*Mic(?:\s*{MODEL})?|"
    rf"(?<![A-Za-z0-9])Mic\s*{MODEL}(?![A-Za-z0-9])|"
    r"大疆(?:这个|这颗)?(?:小麦|无线麦|麦克风))",
    re.IGNORECASE,
)
PRODUCT_CUE_RE = re.compile(
    rf"{PRODUCT_NAME_RE.pattern}|这个麦|这颗麦|这颗小方块|小方块|领夹麦|毛衣麦|"
    r"发射器|接收器|接收端|充电盒|防风毛套|磁吸背夹|收音|录音|音轨|声道|内录|"
    r"32\s*[- ]?bit|浮点|增益|低切|降噪|限幅|爆音|风噪|传输|兼容",
    re.IGNORECASE,
)

BANNED = (
    "本质上", "这说明", "这才是", "产品价值", "核心优势", "适合哪类人",
    "适合谁", "说到底", "所以说", "逻辑很顺", "工作流闭环",
)
SUMMARY_REPLY_RE = re.compile(
    r"^(?:对[，。 ]|所以|这才|确实|哈哈这|说到底|总结|重点是|没错|归根结底)"
)
TRIPLE_SEQUENCE_RE = re.compile(r"先.{0,24}再.{0,24}最后")
ROLE_LABEL_RE = re.compile(
    r"(?:^|[，。！？!? ])[\u4e00-\u9fffA-Za-z0-9]{1,8}(?:党|派)"
    r"(?:路过|不同意|先来|出现|集合|点头|沉默|狂喜|赢了|[：:])"
)
ROLE_COLON_RE = re.compile(r"^[\u4e00-\u9fffA-Za-z0-9]{1,8}[：:]")
MODEL_QUESTION_RE = re.compile(r"什么麦|哪款麦|哪个麦|求型号|用的啥|用的什么|型号是")
PURCHASE_CLOSE_RE = re.compile(r"^(?:懂了|明白了|种草了|那我买|这就买|安排了|冲了|下单)")
EXPERIENCE_RE = re.compile(
    r"我(?:刚|已经|也|真|正)?(?:买了|下单|入手|到手|用了|用过|正在用|换了|升级了|"
    r"实测|亲测|带去|退了|卖了)|"
    r"(?:朋友|同事|室友|对象|男朋友|女朋友|家里人).{0,12}(?:买了|在用|用了|入手|有一套)"
)
IDENTITY_RE = re.compile(
    r"(?:作为|身为)[^，。！？!?]{1,14}|"
    r"(?:我是|我做|我在做|我当)[^，。！？!?]{0,10}"
    r"(?:老师|学生|博主|店主|摄影师|摄像师|主播|运营|记者|导游|主持)"
)
SHORT_REPLY_EXEMPT = {"哈哈", "哈哈哈", "同问", "确实", "我也是", "真的", "笑死", "+1", "＋1"}


@dataclass
class Item:
    file: str
    line: int
    section: str
    group: int
    role: str
    text: str
    number: int | None = None


@dataclass
class Group:
    main: Item
    replies: list[Item] = field(default_factory=list)


@dataclass
class Section:
    file: str
    line: int
    number: str
    label: str
    groups: list[Group] = field(default_factory=list)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def word_chars(text: str) -> str:
    return "".join(
        char
        for char in clean(text)
        if unicodedata.category(char)[0] in {"L", "N"} or "\u4e00" <= char <= "\u9fff"
    )


def canonical(text: str) -> str:
    value = PRODUCT_NAME_RE.sub("产品词", clean(text).lower())
    value = re.sub(r"\d+(?:\.\d+)?", "数字", value)
    return word_chars(value)


def scaffold(text: str) -> str:
    return canonical(text).replace("产品词", "")


def valid_len(text: str) -> int:
    return len(word_chars(text))


def first_six(text: str) -> str:
    value = PRODUCT_NAME_RE.sub("", clean(text))
    return word_chars(value)[:6]


def punctuation_signature(text: str) -> str:
    return "".join(char for char in text if unicodedata.category(char).startswith("P"))


def product_in_first_six(text: str) -> bool:
    match = PRODUCT_NAME_RE.search(text)
    return bool(match and valid_len(text[: match.start()]) < 6)


def model_keys(text: str) -> list[str]:
    keys: list[str] = []
    for match in PRODUCT_NAME_RE.finditer(text):
        token = re.sub(r"\s+", "", match.group(0)).lower()
        token = token.replace("dji", "").replace("大疆", "")
        if "mini2s" in token:
            keys.append("mic-mini-2s")
        elif "mini2" in token:
            keys.append("mic-mini-2")
        elif "mini" in token:
            keys.append("mic-mini")
        elif re.search(r"mic3$", token):
            keys.append("mic-3")
        elif re.search(r"mic2$", token):
            keys.append("mic-2")
        else:
            keys.append("dji-mic-generic")
    return keys


def diag(severity: str, code: str, message: str, item: Item | None = None, **extra: object) -> dict:
    result = {"severity": severity, "code": code, "message": message}
    if item:
        result["location"] = {
            "file": item.file,
            "line": item.line,
            "section": item.section,
            "group": item.group,
        }
    result.update(extra)
    return result


def collect_paths(raw_paths: list[str]) -> list[Path]:
    found: set[Path] = set()
    for raw in raw_paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            found.update(
                item.resolve()
                for item in path.rglob("*.md")
                if item.is_file()
                and not item.name.startswith(".")
                and not re.search(r"(?:^readme(?:\.|$)|使用说明|操作说明|交付说明)", item.name, re.I)
            )
        elif path.is_file():
            found.add(path.resolve())
        else:
            raise FileNotFoundError(raw)
    return sorted(found)


def parse_file(path: Path) -> tuple[list[Section], list[dict]]:
    sections: list[Section] = []
    diagnostics: list[dict] = []
    current: Section | None = None
    group: Group | None = None
    in_fence = False
    synthetic = False

    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        raise RuntimeError(f"无法读取 {path}: {exc}") from exc

    for line_no, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue

        section_match = SECTION_RE.match(raw)
        if section_match:
            current = Section(str(path), line_no, section_match.group(1), section_match.group(2))
            sections.append(current)
            group = None
            synthetic = False
            continue

        labeled_main = LABELED_MAIN_RE.match(raw)
        numbered_main = NUMBERED_MAIN_RE.match(raw)
        if labeled_main or numbered_main:
            if current is None:
                current = Section(str(path), line_no, "1", "single-link")
                sections.append(current)
                synthetic = True
            number = int(numbered_main.group(1)) if numbered_main else len(current.groups) + 1
            text = numbered_main.group(2) if numbered_main else labeled_main.group(1)
            item = Item(str(path), line_no, current.number, len(current.groups) + 1, "main", text, number)
            group = Group(item)
            current.groups.append(group)
            continue

        labeled_reply = LABELED_REPLY_RE.match(raw)
        plain_reply = PLAIN_REPLY_RE.match(raw)
        if labeled_reply or plain_reply:
            if current is None or group is None:
                diagnostics.append(
                    diag(
                        "error",
                        "E_ORPHAN_REPLY",
                        "回复没有对应主评论",
                        Item(str(path), line_no, current.number if current else "", 0, "reply", stripped),
                    )
                )
                continue
            explicit_no = int(labeled_reply.group(1)) if labeled_reply and labeled_reply.group(1) else None
            text = labeled_reply.group(2) if labeled_reply else plain_reply.group(1)
            group.replies.append(
                Item(str(path), line_no, current.number, group.main.group, "reply", text, explicit_no)
            )

    if synthetic and len(sections) > 1:
        diagnostics.append(diag("warning", "W_SYNTHETIC_SECTION", "文件同时包含无标题与有标题评论"))
    return sections, diagnostics


def flatten(sections: list[Section]) -> tuple[list[Item], list[Item], list[Group]]:
    groups = [group for section in sections for group in section.groups]
    mains = [group.main for group in groups]
    replies = [reply for group in groups for reply in group.replies]
    return mains, replies, groups


def audit_structure(sections: list[Section], diagnostics: list[dict]) -> None:
    if not sections:
        diagnostics.append(diag("error", "E_NO_SECTIONS", "未识别到评论章节或主评论"))
        return
    for section in sections:
        if len(section.groups) != 3:
            item = Item(section.file, section.line, section.number, 0, "section", section.label)
            diagnostics.append(
                diag("error", "E_GROUP_COUNT", f"章节应有3组主评论，实际为{len(section.groups)}组", item)
            )
        numbered = [group.main.number for group in section.groups]
        if numbered and numbered != list(range(1, len(numbered) + 1)):
            diagnostics.append(
                diag("error", "E_MAIN_SEQUENCE", f"主评论编号应连续，实际为{numbered}", section.groups[0].main)
            )
        for group in section.groups:
            count = len(group.replies)
            if not 2 <= count <= 4:
                diagnostics.append(
                    diag("error", "E_REPLY_COUNT", f"每组应有2–4条回复，实际为{count}条", group.main)
                )
            explicit = [reply.number for reply in group.replies if reply.number is not None]
            if explicit and explicit != list(range(1, len(group.replies) + 1)):
                diagnostics.append(
                    diag("error", "E_REPLY_SEQUENCE", f"显式回复编号不连续：{explicit}", group.main)
                )


def audit_duplicates(
    current: list[Item],
    baseline: list[Item],
    diagnostics: list[dict],
    role: str,
) -> None:
    exact: dict[str, list[Item]] = defaultdict(list)
    canon: dict[str, list[Item]] = defaultdict(list)
    for item in current:
        exact[clean(item.text)].append(item)
        canon[canonical(item.text)].append(item)

    for value, matches in exact.items():
        if len(matches) < 2:
            continue
        if role == "reply" and (valid_len(value) <= 5 or value in SHORT_REPLY_EXEMPT):
            local = defaultdict(list)
            for item in matches:
                local[(item.file, item.section, item.group)].append(item)
            for items in local.values():
                if len(items) > 1:
                    diagnostics.append(diag("error", "E_EXACT_REPLY_LOCAL", "同一组出现重复回复", items[1]))
            continue
        severity = "error" if role == "main" else "warning"
        code = "E_EXACT_MAIN" if role == "main" else "W_EXACT_REPLY"
        diagnostics.append(diag(severity, code, f"{role} 出现完全相同文本", matches[1], count=len(matches)))

    if role == "main":
        for value, matches in canon.items():
            if len(value) >= 8 and len(matches) > 1 and len({clean(x.text) for x in matches}) > 1:
                diagnostics.append(
                    diag("error", "E_CANON_MAIN", "主评论只替换了型号、数字、标点或空格", matches[1])
                )

    prepared = [(item, scaffold(item.text)) for item in current]
    minimum = 12 if role == "main" else 14
    for index, (left_item, left) in enumerate(prepared):
        if len(left) < minimum:
            continue
        for right_item, right in prepared[index + 1 :]:
            if len(right) < minimum:
                continue
            if role == "reply" and (
                left_item.file,
                left_item.section,
                left_item.group,
            ) == (right_item.file, right_item.section, right_item.group):
                continue
            length_ratio = min(len(left), len(right)) / max(len(left), len(right))
            if length_ratio < 0.75:
                continue
            score = difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()
            if score >= (0.86 if role == "main" else 0.92):
                diagnostics.append(
                    diag(
                        "warning",
                        "W_NEAR_MAIN" if role == "main" else "W_NEAR_REPLY",
                        f"{role} 骨架高度相似",
                        right_item,
                        similarity=round(score, 3),
                    )
                )

    if not baseline:
        return
    baseline_exact = {clean(item.text): item for item in baseline}
    baseline_canon = {canonical(item.text): item for item in baseline}
    for item in current:
        raw = clean(item.text)
        if raw in baseline_exact and not (
            role == "reply" and (valid_len(raw) <= 5 or raw in SHORT_REPLY_EXEMPT)
        ):
            diagnostics.append(
                diag(
                    "warning",
                    "W_BASELINE_EXACT_MAIN" if role == "main" else "W_BASELINE_EXACT_REPLY",
                    f"{role} 与历史成品完全相同",
                    item,
                )
            )
        elif role == "main" and len(canonical(item.text)) >= 8 and canonical(item.text) in baseline_canon:
            diagnostics.append(
                diag("warning", "W_BASELINE_CANON_MAIN", "主评论与历史相比只替换型号或数字", item)
            )


def comma_triplet(text: str) -> bool:
    if text.count("、") >= 2 or TRIPLE_SEQUENCE_RE.search(text):
        return True
    pieces = [part for part in re.split(r"[，,]", text) if clean(part)]
    return len(pieces) >= 5 and sum(valid_len(part) <= 12 for part in pieces) >= 4


def audit_language(sections: list[Section], diagnostics: list[dict], product_policy: str) -> None:
    all_groups: list[Group] = []
    for section in sections:
        all_groups.extend(section.groups)
        if not section.groups:
            continue

        mains = [group.main for group in section.groups]
        product_linked = sum(bool(PRODUCT_CUE_RE.search(item.text)) for item in mains)
        if product_policy != "off" and product_linked < 2:
            severity = "error" if product_policy == "strict" else "warning"
            diagnostics.append(
                diag(
                    severity,
                    "W_PRODUCT_LINK_LOW" if severity == "warning" else "E_PRODUCT_LINK_LOW",
                    f"三条主评中仅{product_linked}条有可识别的 DJI Mic 关联",
                    mains[0],
                )
            )

        full_count = sum(len(FULL_PRODUCT_RE.findall(item.text)) for item in mains)
        if full_count > 1:
            diagnostics.append(
                diag("warning", "W_FULL_MODEL_REPEAT", "同一链接重复出现完整精确型号", mains[0])
            )

        lengths = [valid_len(item.text) for item in mains]
        signatures = [punctuation_signature(item.text) for item in mains]
        if len(lengths) == 3 and max(lengths) - min(lengths) <= 4 and len(set(signatures)) == 1:
            diagnostics.append(
                diag("warning", "W_UNIFORM_MAINS", "三条主评长度和标点过于整齐", mains[0])
            )

        role_colon_count = sum(bool(ROLE_COLON_RE.search(item.text)) for item in mains)
        if role_colon_count > 1:
            diagnostics.append(
                diag("warning", "W_ROLE_JOKE_REPEAT", "同一链接重复使用“角色：台词”造梗", mains[0])
            )

        for group in section.groups:
            combined = [group.main, *group.replies]
            joined = "\n".join(item.text for item in combined)
            for item in combined:
                for phrase in BANNED:
                    if phrase in item.text:
                        diagnostics.append(
                            diag("warning", "W_BANNED_SUMMARY", f"出现总结腔：{phrase}", item)
                        )
                if EXPERIENCE_RE.search(item.text):
                    diagnostics.append(
                        diag("warning", "W_EXPERIENCE_CLAIM", "出现购买/使用/第三方经历，需核对用户证据", item)
                    )
                if IDENTITY_RE.search(item.text) or ROLE_LABEL_RE.search(item.text):
                    diagnostics.append(
                        diag("warning", "W_IDENTITY_CLAIM", "出现身份自报或“××党/派”角色标签", item)
                    )

            if comma_triplet(group.main.text):
                diagnostics.append(
                    diag("warning", "W_TRIPLE_SCENE_ENUM", "主评论疑似连续盘点三个以上对象或步骤", group.main)
                )

            counts = Counter(model_keys(joined))
            if any(count >= 2 for key, count in counts.items() if key != "dji-mic-generic"):
                diagnostics.append(
                    diag("warning", "W_PRODUCT_NAME_ECHO_GROUP", "同一组反复点名同一精确型号", group.main)
                )

            if len(group.replies) >= 3:
                last = group.replies[-1]
                if SUMMARY_REPLY_RE.search(clean(last.text)):
                    diagnostics.append(
                        diag("warning", "W_REPLY_SUMMARY_CLOSE", "第三/第四条回复疑似负责总结收口", last)
                    )
                joke_count = sum(
                    bool(ROLE_COLON_RE.search(reply.text) or "哈哈" in reply.text or "😂" in reply.text)
                    for reply in group.replies
                )
                if joke_count >= 2:
                    diagnostics.append(
                        diag("warning", "W_STAGED_JOKE_CHAIN", "多条回复连续接梗，疑似排练式互动", group.main)
                    )

            if (
                not PRODUCT_CUE_RE.search(group.main.text)
                and group.replies
                and MODEL_QUESTION_RE.search(group.replies[0].text)
                and any(PRODUCT_NAME_RE.search(reply.text) for reply in group.replies[1:3])
            ):
                diagnostics.append(
                    diag("warning", "W_STAGED_PRODUCT_REVEAL", "疑似“问型号—报型号”的预设揭晓", group.main)
                )

            question_index = next(
                (i for i, reply in enumerate(group.replies) if "？" in reply.text or "?" in reply.text),
                None,
            )
            if question_index is not None and len(group.replies) >= 3:
                later = group.replies[question_index + 1 :]
                if later and PURCHASE_CLOSE_RE.search(clean(group.replies[-1].text)):
                    diagnostics.append(
                        diag("warning", "W_STAGED_QA_CHAIN", "疑似“提问—解答—种草/购买”完整排演", group.main)
                    )

    if not all_groups:
        return
    multi = sum(len(group.replies) >= 3 for group in all_groups)
    if len(all_groups) >= 10 and multi / len(all_groups) > 0.15:
        diagnostics.append(
            diag(
                "warning",
                "W_MULTI_REPLY_DENSITY",
                f"三条以上回复组占比{multi}/{len(all_groups)}，复核是否为制造热闹而保留",
                all_groups[0].main,
            )
        )

    mains = [group.main for group in all_groups]
    front = sum(product_in_first_six(item.text) for item in mains)
    if len(mains) >= 12 and front / len(mains) > 0.35:
        diagnostics.append(
            diag("warning", "W_PRODUCT_FIXED_FRONT", "产品名位于句首/前六字的比例偏高", mains[0])
        )

    openings: dict[str, list[Item]] = defaultdict(list)
    for item in mains:
        opening = first_six(item.text)
        if opening:
            openings[opening].append(item)
    for opening, matches in openings.items():
        sections_seen = {(item.file, item.section) for item in matches}
        if len(sections_seen) >= 3:
            diagnostics.append(
                diag("warning", "W_OPENING_REPEAT", f"前六字“{opening}”跨至少3个链接重复", matches[-1])
            )


def summarize(sections: list[Section]) -> dict:
    mains, replies, groups = flatten(sections)
    distribution = Counter(len(group.replies) for group in groups)
    return {
        "sections": len(sections),
        "mains": len(mains),
        "replies": len(replies),
        "reply_distribution": {str(key): distribution[key] for key in sorted(distribution)},
    }


def render_text(stats: dict, diagnostics: list[dict], max_examples: int) -> None:
    print(
        "DJI Mic QA | "
        f"sections={stats['sections']} mains={stats['mains']} replies={stats['replies']} "
        f"reply_distribution={stats['reply_distribution']}"
    )
    if not diagnostics:
        print("PASS | no diagnostics")
        return
    counts = Counter((item["severity"], item["code"]) for item in diagnostics)
    ordering = {"error": 0, "warning": 1}
    for (severity, code), count in sorted(
        counts.items(), key=lambda pair: (ordering.get(pair[0][0], 9), pair[0][1])
    ):
        print(f"{severity.upper()} {code} x{count}")
        shown = 0
        for item in diagnostics:
            if item["severity"] != severity or item["code"] != code:
                continue
            location = item.get("location", {})
            where = f"{location.get('file', '')}:{location.get('line', 0)}"
            print(f"  - {where} {item['message']}")
            shown += 1
            if shown >= max_examples:
                break


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit DJI Mic comment draft homogeneity.")
    parser.add_argument("inputs", nargs="+", help="Current Markdown file(s) or directories.")
    parser.add_argument("--baseline", nargs="*", default=[], help="Historical Markdown used only for similarity.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Return 1 when warnings remain.")
    parser.add_argument("--product-policy", choices=("advisory", "strict", "off"), default="advisory")
    parser.add_argument("--max-examples", type=int, default=3)
    args = parser.parse_args()

    try:
        current_paths = collect_paths(args.inputs)
        baseline_paths = collect_paths(args.baseline) if args.baseline else []
        current_sections: list[Section] = []
        baseline_sections: list[Section] = []
        diagnostics: list[dict] = []
        for path in current_paths:
            sections, parse_diags = parse_file(path)
            current_sections.extend(sections)
            diagnostics.extend(parse_diags)
        for path in baseline_paths:
            sections, _ = parse_file(path)
            baseline_sections.extend(sections)
    except (FileNotFoundError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    audit_structure(current_sections, diagnostics)
    current_mains, current_replies, _ = flatten(current_sections)
    baseline_mains, baseline_replies, _ = flatten(baseline_sections)
    audit_duplicates(current_mains, baseline_mains, diagnostics, "main")
    audit_duplicates(current_replies, baseline_replies, diagnostics, "reply")
    audit_language(current_sections, diagnostics, args.product_policy)

    stats = summarize(current_sections)
    payload = {
        "tool": "DJI Mic comment homogeneity checker",
        "stats": stats,
        "diagnostics": diagnostics,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        render_text(stats, diagnostics, max(args.max_examples, 1))

    has_error = any(item["severity"] == "error" for item in diagnostics)
    has_warning = any(item["severity"] == "warning" for item in diagnostics)
    return 1 if has_error or (args.strict and has_warning) else 0


if __name__ == "__main__":
    sys.exit(main())
