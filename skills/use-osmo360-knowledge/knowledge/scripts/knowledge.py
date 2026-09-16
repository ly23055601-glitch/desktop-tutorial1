#!/usr/bin/env python3
"""本地知识卡检索、目录生成与引用审计；仅用 Python 标准库。"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    "osmo_360": "Osmo 360（第一代）",
    "osmo_360_ii": "Osmo 360 II",
    "insta360_x6": "Insta360 X6",
    "insta360_x5": "Insta360 X5",
    "gopro_max2": "GoPro MAX2",
}
FACT_ID = re.compile(r"\b(?:D1|D2|IX6|IX5|GM2)-\d{3}\b")
STATES = {"verified": "已按记录日期核验", "pending": "待核验", "conflict": "来源冲突"}
OFFICIAL_DOMAINS = ("dji.com", "djicdn.com", "dji.net", "insta360.com", "gopro.com", "sec.gov")


def load(root):
    facts, sources, errors = [], [], []
    for pattern, destination in (("products/*.facts.jsonl", facts), ("sources/*.jsonl", sources)):
        for path in sorted(root.glob(pattern)):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise ValueError("记录必须是对象")
                    destination.append(item)
                except (ValueError, json.JSONDecodeError) as exc:
                    errors.append(f"{path.relative_to(root)}:{number}: {exc}")
    return facts, sources, errors


def terms(query):
    # 问句套语不是检索主题，避免“支持卫星电话吗”仅凭“支持”命中其他能力。
    query = re.sub(r"请问|帮我|查一下|查询|介绍一下|能不能|有没有|是否|能否|支持|可以|如何|怎么|什么|多少|的|吗|呢", " ", query)
    result = set(re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", query.lower()))
    result.difference_update({"和", "与", "及", "对比", "比较"})
    for term in list(result):
        if re.fullmatch(r"[\u4e00-\u9fff]{3,}", term):
            result.update(term[i:i + 2] for i in range(len(term) - 1))
    return result


def query_scope_and_topic(query):
    """将明确型号与主题分开；先匹配二代，避免其名称的一代前缀误入范围。"""
    scope = set()
    value = query.lower().replace("ⅱ", "ii")
    sep = r"[\s_-]*"
    osmo = rf"(?<![a-z0-9])(?:dji{sep})?osmo{sep}360"
    chinese = rf"大疆{sep}(?:osmo{sep})?360"
    patterns = (
        ("osmo_360_ii", rf"(?:{osmo}|{chinese}){sep}(?:ii(?![a-z0-9])|(?:第?二|2){sep}代?(?![a-z0-9]))"),
        ("osmo_360", rf"(?:{osmo}{sep}(?:(?:第?一|1){sep}代?)?(?![a-z0-9])|{chinese}{sep}(?:第?一|1){sep}代?(?![a-z0-9]))"),
        ("insta360_x5", rf"(?<![a-z0-9])(?:insta360{sep})?x5(?![a-z0-9])"),
        ("insta360_x6", rf"(?<![a-z0-9])(?:insta360{sep})?x6(?![a-z0-9])"),
        ("gopro_max2", rf"(?<![a-z0-9])(?:gopro{sep})?max{sep}2(?![a-z0-9])"),
    )
    for model, pattern in patterns:
        value, count = re.subn(pattern, " ", value)
        if count:
            scope.add(model)
    return scope, value


def query_models(query):
    """仅从明确产品名推定范围；多型号问题保留全部命中型号。"""
    return query_scope_and_topic(query)[0]


def rank_cards(facts, query, model, limit, statuses):
    exact_id = query.strip().upper()
    if FACT_ID.fullmatch(exact_id):
        return [f for f in facts if f.get("id") == exact_id and f.get("status") in statuses
                and (not model or model in f.get("models", []))][:limit]
    inferred_scope, topic_query = query_scope_and_topic(query)
    scope = {model} if model else inferred_scope
    needles = terms(topic_query)
    ranked = []
    for fact in facts:
        if fact.get("status") not in statuses or (scope and not scope.intersection(fact.get("models", []))):
            continue
        title = " ".join([fact.get("id", ""), fact.get("topic", ""), fact.get("statement", "")]).lower()
        rest = json.dumps([fact.get("conditions", []), fact.get("limitations", []), fact.get("software")], ensure_ascii=False).lower()
        score = sum(len(term) * (3 if term in title else 1 if term in rest else 0) for term in needles)
        if score:
            ranked.append((score, fact["id"], fact))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def search(facts, query, model=None, limit=5):
    return rank_cards(facts, query, model, limit, {"verified"})


def related_issues(facts, query, model=None, limit=3):
    return rank_cards(facts, query, model, limit, {"pending", "conflict"})


def valid_date(value):
    try:
        parsed = dt.date.fromisoformat(value)
        return parsed <= dt.date.today()
    except (ValueError, TypeError):
        return False


def audit(root, facts, sources, initial_errors=()):
    errors, warnings = list(initial_errors), []
    indexes = {}
    for label, records in (("fact", facts), ("source", sources)):
        by_id = {}
        for item in records:
            identifier = item.get("id")
            if not identifier or identifier in by_id:
                errors.append(f"{label}: 缺失或重复 ID {identifier}")
            by_id[identifier] = item
        indexes[label] = by_id
    for source in sources:
        sid = source.get("id", "?")
        for field in ("title", "url", "publisher", "language", "region", "models", "checked_at", "status", "locators", "notes"):
            if field not in source:
                errors.append(f"{sid}: 缺少来源字段 {field}")
        host = urlparse(source.get("url", "")).hostname or ""
        if not any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAINS):
            errors.append(f"{sid}: 非已登记官方域名 {host}")
        if source.get("status") not in {"read", "unread"}:
            errors.append(f"{sid}: 来源读取状态无效")
        if not valid_date(source.get("checked_at")):
            errors.append(f"{sid}: 核验日期无效")
        if not source.get("models") or not set(source["models"]).issubset(MODELS):
            errors.append(f"{sid}: 来源型号无效")
    for fact in facts:
        fid = fact.get("id", "?")
        for field in ("kind", "models", "topic", "statement", "conditions", "limitations", "region", "firmware", "software", "sources", "checked_at", "status"):
            if field not in fact:
                errors.append(f"{fid}: 缺少知识卡字段 {field}")
        if not FACT_ID.fullmatch(str(fid)) or fact.get("kind") != "official_fact":
            errors.append(f"{fid}: 事实编号或类别无效")
        if not fact.get("statement") or not fact.get("topic"):
            errors.append(f"{fid}: 结论或主题为空")
        if not fact.get("models") or not set(fact["models"]).issubset(MODELS):
            errors.append(f"{fid}: 型号无效")
        if fact.get("status") not in STATES or not valid_date(fact.get("checked_at")):
            errors.append(f"{fid}: 状态或日期无效")
        for field in ("conditions", "limitations", "sources"):
            if not isinstance(fact.get(field), list):
                errors.append(f"{fid}: {field} 必须为列表")
        if fact.get("status") == "verified" and not fact.get("sources"):
            errors.append(f"{fid}: 已核验事实缺少来源")
        for ref in fact.get("sources", []):
            source = indexes["source"].get(ref.get("source_id"))
            if not source:
                errors.append(f"{fid}: 未登记来源 {ref.get('source_id')}")
                continue
            if not ref.get("locator"):
                errors.append(f"{fid}: 缺少来源定位")
            if not set(fact.get("models", [])).issubset(source.get("models", [])):
                errors.append(f"{fid}: 与来源 {source['id']} 的型号不符")
            if fact.get("status") == "verified" and source.get("status") != "read":
                errors.append(f"{fid}: 已核验事实引用未读取来源")
        if fact.get("status") != "verified":
            warnings.append(f"{fid}: {STATES.get(fact.get('status'), '无效状态')}")
    docs = list(root.rglob("*.md"))
    for path in docs:
        body = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for fid in set(FACT_ID.findall(body)):
            if fid not in indexes["fact"]:
                errors.append(f"{rel}: 引用未知知识卡 {fid}")
            elif path.parent.name == "training" and indexes["fact"][fid].get("status") != "verified":
                errors.append(f"{rel}: 培训标准答案引用未核验知识卡 {fid}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
            target = target.strip("<>")
            if urlparse(target).scheme:
                continue
            local, _, anchor = unquote(target).partition("#")
            dest = path.parent / local if local else path
            if not dest.exists():
                errors.append(f"{rel}: 本地链接不存在 {target}")
            elif anchor and dest.suffix == ".md":
                dest_text = dest.read_text(encoding="utf-8")
                headings = re.findall(r"^#{1,6}\s+(.+)$", dest_text, re.M)
                slugs = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                explicit = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', dest_text))
                if anchor not in slugs | explicit:
                    errors.append(f"{rel}: 本地锚点不存在 {target}")
    counts = {}
    for filename, prefix, expected in (("faq.md", "Q", 30), ("quiz.md", "T", 20)):
        path = root / "training" / filename
        body = path.read_text(encoding="utf-8") if path.exists() else ""
        entries = re.findall(rf"^### {prefix}(\d{{2}})\b", body, re.M)
        counts[prefix] = len(entries)
        if sorted(entries) != [f"{i:02}" for i in range(1, expected + 1)]:
            errors.append(f"training/{filename}: 应有完整且不重复的 {expected} 个编号")
        for entry in re.split(rf"^### {prefix}\d{{2}}\b", body, flags=re.M)[1:]:
            if not FACT_ID.search(entry):
                errors.append(f"training/{filename}: 某条问题缺少知识卡依据")
    for filename in ("01-basics.md", "02-models.md", "03-capture.md", "04-postproduction.md", "05-accessories.md", "06-scenarios.md", "07-comparison.md", "08-learning.md"):
        if not (root / "modules" / filename).is_file():
            errors.append(f"缺少模块 {filename}")
    for model in MODELS:
        if not any(model in fact.get("models", []) and fact.get("status") == "verified" for fact in facts):
            errors.append(f"{model}: 没有可用事实")
    return {"ok": not errors, "facts": len(facts), "verified": sum(f.get("status") == "verified" for f in facts), "sources": len(sources), "faq": counts["Q"], "quiz": counts["T"], "errors": errors, "warnings": warnings,
            "limitations": ["结构审计不等于事实语义审查；核验日期不代表未来仍适用。", "检索将已核验答案与相关未决记录分开；未覆盖的问题须查看 GAPS.md。"]}


def build(root, facts, sources):
    source_index = {source["id"]: source for source in sources}
    lines = ["# 知识卡目录", "", "由 `scripts/knowledge.py build` 根据 JSONL 生成。更新应先修改事实卡，再重新生成。已核验只表示在记录日期读取了相应来源。", ""]
    for model, title in MODELS.items():
        lines += [f"## {title}", ""]
        for fact in facts:
            if model not in fact["models"]:
                continue
            lines += [f"### {fact['id']}", "", f"**{fact['topic']}｜{STATES[fact['status']]}**", "", fact["statement"], ""]
            for label, field in (("条件", "conditions"), ("边界", "limitations")):
                values = fact.get(field) or []
                if values:
                    lines += [f"- {label}：" + "；".join(values)]
            lines += [f"- 地区：{fact['region']}；核验：{fact['checked_at']}"]
            if fact.get("firmware"):
                lines += [f"- 固件：{fact['firmware']}"]
            if fact.get("software"):
                lines += [f"- 软件：{fact['software']}"]
            for ref in fact.get("sources", []):
                source = source_index[ref["source_id"]]
                lines += [f"- 来源：[{source['id']} · {source['title']}]({source['url']})；定位：{ref['locator']}"]
            lines += [""]
    (root / "CARDS.md").write_text("\n".join(lines), encoding="utf-8")
    lines = ["# 官方来源登记", "", "由 `scripts/knowledge.py build` 生成。地区指实际读取页面的适用或销售地区；英文页面不自动代表中国大陆销售政策。", ""]
    for source in sources:
        lines += [f"## {source['id']}", "", f"[{source['title']}]({source['url']})", "", f"- 发布方：{source['publisher']}；语言：{source['language']}；地区：{source['region']}", f"- 型号：{'、'.join(MODELS[m] for m in source['models'])}", f"- 读取状态：{source['status']}；核验日期：{source['checked_at']}", f"- 定位：{'；'.join(source['locators'])}", f"- 说明：{source['notes']}", ""]
    (root / "sources" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    lookup = sub.add_parser("search")
    lookup.add_argument("query")
    lookup.add_argument("--model", choices=list(MODELS))
    lookup.add_argument("--limit", type=int, default=5)
    lookup.add_argument("--format", choices=["markdown", "json"], default="markdown")
    check = sub.add_parser("audit")
    check.add_argument("--format", choices=["markdown", "json"], default="markdown")
    sub.add_parser("build")
    args = parser.parse_args()
    root = args.root.resolve()
    facts, sources, errors = load(root)
    if args.command == "audit":
        result = audit(root, facts, sources, errors)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{'通过' if result['ok'] else '未通过'}：{result['facts']} 张卡、{result['verified']} 张已核验、{result['sources']} 个来源、{result['faq']} 个问答、{result['quiz']} 道自测")
            for item in result["errors"] + result["warnings"] + result["limitations"]:
                print(f"- {item}")
        return 0 if result["ok"] else 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if args.command == "build":
        build(root, facts, sources)
        print("已生成 CARDS.md 与 sources/INDEX.md")
        return 0
    if not args.query.strip() or not 1 <= args.limit <= 30:
        parser.error("查询不能为空，limit 须在 1 到 30 之间")
    matches = search(facts, args.query, args.model, args.limit)
    unresolved = related_issues(facts, args.query, args.model)
    if args.format == "json":
        print(json.dumps({"query": args.query, "model": args.model, "matches": matches, "unresolved": unresolved}, ensure_ascii=False, indent=2))
    else:
        if unresolved:
            print("相关缺口（不作为已核验答案）：")
            for fact in unresolved:
                print(f"- {fact['id']} · {STATES[fact['status']]}：{fact['statement']}")
                print(f"  [查看条件及记录]({root / 'CARDS.md'}#{fact['id'].lower()})")
        if not matches:
            print("未找到已核验知识卡。请查阅 GAPS.md 或更换关键词；无结果不代表产品不支持。")
        for fact in matches:
            print(f"\n### {fact['id']} · {fact['topic']}\n\n{fact['statement']}")
            print(f"\n型号：{'、'.join(MODELS[m] for m in fact['models'])}；核验：{fact['checked_at']}")
            for value in fact['conditions'] + fact['limitations']:
                print(f"- {value}")
            print(f"- 知识卡：[查看来源和条件]({root / 'CARDS.md'}#{fact['id'].lower()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
