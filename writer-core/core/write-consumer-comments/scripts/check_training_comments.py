#!/usr/bin/env python3
"""Check training-fiction draft structure, never the truth of its source claims."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


LABEL = "培训用假想消费者草稿"
HEADER = re.compile(r"^##\s+(\d+)｜(.+?)\s*$")
MAIN = re.compile(r"^(\d+)\.\s+(.+?)\s*$")
REPLY = re.compile(r"^(?: {4}|\t)-\s+(.+?)\s*$")
SOURCE_KINDS = {"post", "product", "synthetic_post"}
ASSERTION_KINDS = {"post_fact", "product_fact", "fictional_experience"}
PROFILES = ("legacy", "cw5")


def parse_draft(text):
    """Return sections in display order, with local numbered comment IDs."""
    sections, errors = [], []
    section = main = None
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        match = HEADER.fullmatch(line)
        if match:
            section = {"section": int(match[1]), "title": match[2], "comments": {}, "mains": []}
            sections.append(section)
            main = None
            continue
        if section is None:
            if MAIN.fullmatch(line) or REPLY.fullmatch(line) or line.startswith("##"):
                errors.append(f"MD第{line_no}行：评论或章节缺少正确的章节标题")
            continue
        match = MAIN.fullmatch(line)
        if match:
            cid = match[1]
            if int(cid) != len(section["mains"]) + 1:
                errors.append(f"第{section['section']}帖：主评必须从1连续编号")
            if cid in section["comments"]:
                errors.append(f"第{section['section']}帖：重复评论编号{cid}")
            section["comments"][cid] = {"text": match[2], "main": cid, "reply": False}
            section["mains"].append(cid)
            main = cid
            continue
        match = REPLY.fullmatch(line)
        if match and main is not None:
            number = sum(c["reply"] and c["main"] == main for c in section["comments"].values()) + 1
            cid = f"{main}.{number}"
            section["comments"][cid] = {"text": match[1], "main": main, "reply": True}
            continue
        errors.append(f"MD第{line_no}行：须使用主评编号或四空格缩进的单层回复")
    if not sections:
        errors.append("MD缺少 ## 1｜链接或材料定位 格式的章节")
    if len({s["section"] for s in sections}) != len(sections):
        errors.append("MD章节号重复")
    return sections, errors


def has_sentence_period(text):
    # Retain a trailing full stop after a URL; ignore dots inside URLs/decimals.
    text = re.sub(r"https?://[^\s<>，。！？、；]+", lambda m: "." if m[0].endswith(".") else "", text)
    text = re.sub(r"(?<=\d)\.(?=\d)", "", text)
    return any(char in text for char in ".。｡．")


def is_nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def local_file(base, value, label, errors):
    if not is_nonempty_text(value) or Path(value).is_absolute():
        errors.append(f"{label}：必须提供相对state的文件路径")
        return None
    path = base / value
    if not path.is_file():
        errors.append(f"{label}：文件不存在 {value}")
        return None
    return path


def check_state(state_path, profile="legacy"):
    """Validate one draft; legacy quantity limits remain the default."""
    if profile not in PROFILES:
        return [f"不支持的检查profile：{profile}；只允许legacy/cw5"]
    errors = []
    state_path = Path(state_path).resolve()
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"无法读取state：{exc}"]
    if not isinstance(state, dict):
        return ["state必须是JSON对象"]
    if state.get("content_mode") != "training_fiction":
        errors.append("仅接受 content_mode=training_fiction；真实消费者模式不能通过本检查器")
    draft = local_file(state_path.parent, state.get("draft"), "draft", errors)
    if draft is None:
        return errors
    try:
        draft_bytes = draft.read_bytes()
        text = draft_bytes.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        return errors + [f"无法读取UTF-8草稿：{exc}"]
    actual_hash = hashlib.sha256(draft_bytes).hexdigest()
    if state.get("draft_sha256") != actual_hash:
        errors.append("draft_sha256缺失或与最终MD不一致；修改草稿后须重新绑定")
    if text.count(LABEL) != 1:
        errors.append(f"批次MD必须恰好出现一次“{LABEL}”标识")
    sections, parse_errors = parse_draft(text)
    errors.extend(parse_errors)
    posts = state.get("posts")
    if not isinstance(posts, list) or not posts or not all(isinstance(p, dict) for p in posts):
        return errors + ["posts必须是非空对象数组"]
    if [p.get("section") for p in posts] != [s["section"] for s in sections]:
        errors.append("state posts顺序/section必须与MD全部章节一一对应")
    if any(not is_nonempty_text(p.get("id")) for p in posts):
        errors.append("每帖id必须是原帖ID或明确的用户材料ID")
    if len({p.get("id") for p in posts if isinstance(p.get("id"), str)}) != len(posts):
        errors.append("每帖id必须唯一")
    by_section = {s["section"]: s for s in sections}
    for post in posts:
        section_num = post.get("section")
        if not isinstance(section_num, int) or isinstance(section_num, bool):
            errors.append("section必须是整数章节号")
            continue
        section = by_section.get(section_num)
        if section is None:
            continue
        prefix = f"第{section_num}帖"
        if post.get("title") != section["title"]:
            errors.append(f"{prefix}：title必须精确对应MD标题中的链接或材料定位")
        if not is_nonempty_text(post.get("product_line")):
            errors.append(f"{prefix}：缺少本帖product_line")
        comments = section["comments"]
        if not 2 <= len(section["mains"]) <= 4:
            errors.append(f"{prefix}：须有2–4条主评")
        reply_counts = {
            cid: sum(c["reply"] and c["main"] == cid for c in comments.values())
            for cid in section["mains"]
        }
        reply_limit = 8 if profile == "cw5" else 4
        for cid, count in reply_counts.items():
            if count > reply_limit:
                errors.append(f"{prefix}主评{cid}：回复须为0–{reply_limit}条")
        if profile == "cw5" and not any(count >= 5 for count in reply_counts.values()):
            errors.append(f"{prefix}：CW5至少一组主评须有5–8条回复")
        aliases = post.get("english_aliases")
        if not isinstance(aliases, list) or not all(is_nonempty_text(a) and re.search(r"[A-Za-z]", a) and not re.search(r"\s", a) for a in aliases):
            errors.append(f"{prefix}：english_aliases须为含英文字母且无内部空格的别名数组，可为空")
            aliases = []
        for cid, comment in comments.items():
            body = comment["text"]
            if has_sentence_period(body):
                errors.append(f"{prefix}评论{cid}：正文含句号")
            # Only this post's product line determines the Pocket naming restriction.
            if str(post.get("product_line", "")).casefold() == "pocket" and re.search(r"osmo", body, re.I):
                errors.append(f"{prefix}评论{cid}：Pocket正文禁用Osmo")
            for alias in aliases:
                spaced = r"\s*".join(re.escape(char) for char in alias)
                if any(re.search(r"\s", m[0]) for m in re.finditer(spaced, body, re.I)):
                    errors.append(f"{prefix}评论{cid}：英文产品名须写作无空格别名{alias}")
        sources = post.get("sources")
        if not isinstance(sources, dict) or not sources:
            errors.append(f"{prefix}：sources须登记原帖或用户材料文件")
            sources = {}
        source_texts, source_kinds = {}, {}
        for key, source in sources.items():
            if not isinstance(source, dict) or not isinstance(source.get("kind"), str) or source.get("kind") not in SOURCE_KINDS:
                errors.append(f"{prefix}来源{key}：kind只允许post/product/synthetic_post，人物设定不能作为来源")
                continue
            kind = source["kind"]
            source_kinds[key] = kind
            if kind == "synthetic_post" and (not re.search(r"合成|synthetic", str(source.get("description", "")), re.I) or not re.search(r"合成|synthetic", section["title"], re.I)):
                errors.append(f"{prefix}来源{key}：合成原帖须在description和MD章节标题明示合成")
            path = local_file(state_path.parent, source.get("path"), f"{prefix}来源{key}", errors)
            if path:
                if path.resolve() in {state_path, draft.resolve()}:
                    errors.append(f"{prefix}来源{key}：训练state或最终draft不能作为事实来源自证")
                    continue
                try:
                    source_texts[key] = path.read_text(encoding="utf-8")
                    if not source_texts[key].strip():
                        errors.append(f"{prefix}来源{key}：证据文件为空")
                except (OSError, UnicodeError) as exc:
                    errors.append(f"{prefix}来源{key}：须提供UTF-8证据文本，截图可另存可见文字/画面描述：{exc}")
        if not any(kind in {"post", "synthetic_post"} for kind in source_kinds.values()):
            errors.append(f"{prefix}：至少登记一个post或明示合成的synthetic_post来源")
        personas = post.get("personas", {})
        if not isinstance(personas, dict) or not all(is_nonempty_text(k) and is_nonempty_text(v) for k, v in personas.items()):
            errors.append(f"{prefix}：personas须为说话者→假想人物设定的对象，可为空")
            personas = {}
        context = post.get("reply_context")
        if not isinstance(context, dict):
            errors.append(f"{prefix}：reply_context须为对象，无回复填{{}}")
            context = {}
        expected_replies = {cid for cid, c in comments.items() if c["reply"]}
        if set(context) != expected_replies:
            errors.append(f"{prefix}：reply_context必须完整且仅映射实际回复")
        speakers = {}
        ordered_ids = list(comments)
        for cid, info in context.items():
            if cid not in expected_replies or not isinstance(info, dict):
                errors.append(f"{prefix}回复{cid}：无效回复上下文")
                continue
            parent_id = info.get("parent_id")
            if not isinstance(parent_id, str) or parent_id not in comments:
                errors.append(f"{prefix}回复{cid}：parent_id必须指向实际评论")
                continue
            if comments[parent_id]["main"] != comments[cid]["main"] or ordered_ids.index(parent_id) >= ordered_ids.index(cid):
                errors.append(f"{prefix}回复{cid}：直接父句必须是同楼较早评论")
            if info.get("parent_text") != comments[parent_id]["text"]:
                errors.append(f"{prefix}回复{cid}：parent_text须逐字保留直接父句")
            for comment_id, field in ((cid, "speaker"), (parent_id, "parent_speaker")):
                speaker = info.get(field)
                if not isinstance(speaker, str) or speaker not in personas:
                    errors.append(f"{prefix}回复{cid}：{field}须对应personas中的假想说话者")
                    continue
                if comment_id in speakers and speakers[comment_id] != speaker:
                    errors.append(f"{prefix}评论{comment_id}：说话者映射冲突")
                speakers[comment_id] = speaker
        assertions = post.get("assertions")
        if not isinstance(assertions, list):
            errors.append(f"{prefix}：assertions须为数组，无需事实引用时可为空，覆盖完整性仍须语义审稿")
            continue
        for i, assertion in enumerate(assertions, 1):
            label = f"{prefix}断言{i}"
            if not isinstance(assertion, dict):
                errors.append(f"{label}：须为对象")
                continue
            cid, fragment, kind = assertion.get("comment_id"), assertion.get("text"), assertion.get("kind")
            if not isinstance(cid, str) or cid not in comments or not is_nonempty_text(fragment) or fragment not in comments[cid]["text"]:
                errors.append(f"{label}：comment_id/text须绑定最终正文的实际片段")
            if not isinstance(kind, str) or kind not in ASSERTION_KINDS:
                errors.append(f"{label}：无效kind")
                continue
            evidence = assertion.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"{label}：evidence须为数组")
                continue
            if kind == "fictional_experience":
                if evidence:
                    errors.append(f"{label}：假想经历evidence须为空，人物设定与真实事实依据分离")
                continue
            if not evidence:
                errors.append(f"{label}：事实断言缺少证据")
            allowed = {"product"} if kind == "product_fact" else {"post", "synthetic_post"}
            for ref in evidence:
                if not isinstance(ref, dict):
                    errors.append(f"{label}：证据须为source/quote对象")
                    continue
                key, quote = ref.get("source"), ref.get("quote")
                if not isinstance(key, str) or source_kinds.get(key) not in allowed:
                    errors.append(f"{label}：{kind}来源类型混用或未在本帖登记")
                    continue
                if not is_nonempty_text(quote) or quote not in source_texts.get(key, ""):
                    errors.append(f"{label}：quote不在本帖来源{key}的实际文件中")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="培训模式state JSON路径")
    parser.add_argument("--profile", choices=PROFILES, default="legacy", help="数量检查配置；默认legacy保留旧稿限制，新稿显式选择cw5")
    parser.add_argument("--json", action="store_true", help="输出结构检查报告JSON")
    args = parser.parse_args(argv)
    errors = check_state(args.state, profile=args.profile)
    if args.json:
        print(json.dumps({"structure_ok": not errors, "profile": args.profile, "scope": "training_fiction_structure_only", "semantic_review_required": True, "errors": errors}, ensure_ascii=False, indent=2))
    elif errors:
        print("培训草稿结构检查未通过：\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
    else:
        print("培训草稿结构检查通过；原帖/产品事实真实性、断言覆盖及语言自然度仍须语义审稿")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
