#!/usr/bin/env python3
"""Read-only DJI Mic retrieval and provenance audit; Python standard library only."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MODELS = {"mic", "mic_2", "mic_3", "mic_mini", "mic_mini_2", "mic_mini_2s"}
PRIMARY = {"mic_3", "mic_mini_2s"}
TOPICS = ("identity", "wearing", "audio", "recording", "channels", "transmission",
          "power", "connections", "controls", "export", "firmware", "kits")
TOPIC_NAMES = dict(zip(TOPICS, ("型号部件", "佩戴", "音频处理", "内录", "声道与多人",
    "传输", "续航充电", "连接", "控制操作", "文件导出", "固件更新", "套装")))
TABLES = {"models": "products/models.jsonl", "sources": "sources/*.jsonl",
          "facts": "products/*.facts.jsonl", "compatibility": "compatibility/*.jsonl",
          "scenarios": "scenarios/cards.jsonl"}
ALIASES = {
    "mic": "mic", "djimic": "mic", "djimic初代": "mic", "大疆mic初代": "mic",
    "mic2": "mic_2", "djimic2": "mic_2", "大疆mic2": "mic_2",
    "mic3": "mic_3", "djimic3": "mic_3", "大疆mic3": "mic_3",
    "micmini": "mic_mini", "djimicmini": "mic_mini", "大疆micmini": "mic_mini",
    "micmini2": "mic_mini_2", "djimicmini2": "mic_mini_2", "大疆micmini2": "mic_mini_2",
    "micmini2s": "mic_mini_2s", "djimicmini2s": "mic_mini_2s", "大疆micmini2s": "mic_mini_2s",
}
SYNONYMS = (
    ("内录", "本地录音", "录音备份", "备份", "存储", "录制文件", "不可重录", "补录"),
    ("手机", "口播", "iphone", "安卓", "android", "手机版"),
    ("相机", "单反", "微单", "3.5", "trs", "热靴"),
    ("双人", "两个人", "两人", "采访", "双发", "一对二"),
    ("多人", "四个人", "四人", "四发", "四声道", "多机位", "多接收器"),
    ("户外", "风噪", "防风", "室外", "有风", "街头", "风大"),
    ("导出", "拷贝", "电脑", "文件传输", "下载录音"),
    ("降噪", "噪声", "噪音", "低切"),
    ("爆音", "削波", "限幅", "增益", "浮点", "32-bit", "32bit"),
    ("连接", "配对", "对频", "直连", "蓝牙", "兼容", "混连"),
    ("续航", "电池", "充电", "供电", "没电"),
    ("固件", "更新", "升级", "版本"),
)


def normalize(value):
    return re.sub(r"[\s_-]", "", str(value).lower())


def resolve_model(value):
    if value in MODELS:
        return value
    found = ALIASES.get(normalize(value))
    if not found:
        raise ValueError("型号不明确或不在库中；请用 " + ", ".join(sorted(MODELS)))
    return found


def load(root=ROOT):
    data, issues = {}, []
    for table, pattern in TABLES.items():
        data[table] = []
        paths = sorted(root.glob(pattern))
        if not paths:
            issues.append({"severity": "error", "code": "missing_table", "at": pattern})
        for path in paths:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as exc:
                issues.append({"severity": "error", "code": "unreadable_file", "at": str(path), "detail": str(exc)})
                continue
            for n, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise ValueError("record must be an object")
                    data[table].append(row)
                except (ValueError, TypeError) as exc:
                    issues.append({"severity": "error", "code": "invalid_jsonl", "at": f"{path.relative_to(root)}:{n}", "detail": str(exc)})
    return data, issues


def valid_date(value):
    try:
        return date.fromisoformat(value) <= date.today()
    except (ValueError, TypeError):
        return False


def official_url(value):
    try:
        url = urlsplit(value)
        host = url.hostname or ""
        return url.scheme == "https" and not url.username and any(
            host == d or host.endswith("." + d) for d in ("dji.com", "djicdn.com", "dji-innovations.com"))
    except (ValueError, TypeError, AttributeError):
        return False


def index(rows):
    return {r["id"]: r for r in rows if isinstance(r.get("id"), str)}


def text_list(value):
    return isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value)


def schema_type_issues(data):
    """Reject malformed field shapes before walking references or computing coverage."""
    issues = []
    common = {"id": str}
    shapes = {
        "sources": {"title": str, "url": str, "source_type": str, "region": str, "language": str,
                    "checked_at": str, "read_scope": str, "summary": str},
        "models": {"official_name": str, "priority": str, "aliases": list, "components": list,
                   "fact_ids": list, "source_refs": list},
        "facts": {"models": list, "component": str, "topic": str, "statement": str, "conditions": list,
                  "limitations": list, "source_refs": list, "checked_at": str, "status": str},
        "compatibility": {"models": list, "component": str, "statement": str, "conditions": list,
                          "limitations": list, "source_refs": list, "checked_at": str, "status": str,
                          "transmitter_model": str, "host": str, "method": str, "support": str, "features": list},
        "scenarios": {"models": list, "scenario": str, "question": str, "task": str, "steps": list,
                      "answer": str, "limitations": list, "fact_ids": list, "compatibility_ids": list, "kind": str},
    }
    for table, rows in data.items():
        for number, row in enumerate(rows, 1):
            at = row.get("id") if isinstance(row.get("id"), str) else f"{table}[{number}]"
            for field, wanted in {**common, **shapes.get(table, {})}.items():
                value = row.get(field)
                valid = isinstance(value, wanted)
                if valid and wanted is list:
                    valid = all(isinstance(x, dict if field == "source_refs" else str) for x in value)
                if not valid:
                    issues.append({"severity": "error", "code": "invalid_field_type", "at": at,
                                   "detail": f"{field}: expected {wanted.__name__}"})
            for optional in ("keywords",):
                if optional in row and not text_list(row[optional]):
                    issues.append({"severity": "error", "code": "invalid_field_type", "at": at, "detail": optional})
            if "local_path" in row and row["local_path"] is not None and not isinstance(row["local_path"], str):
                issues.append({"severity": "error", "code": "invalid_field_type", "at": at, "detail": "local_path"})
            if "gap_reason" in row and not isinstance(row["gap_reason"], str):
                issues.append({"severity": "error", "code": "invalid_field_type", "at": at, "detail": "gap_reason"})
    return issues


def audit(data, initial_issues=(), root=ROOT):
    issues = list(initial_issues)
    bad_types = schema_type_issues(data)
    if bad_types:
        issues += bad_types
        return {"ok": False, "errors": sum(i["severity"] == "error" for i in issues), "warnings": 0,
                "counts": {t: len(rows) for t, rows in data.items()}, "coverage": [], "gaps": [], "issues": issues,
                "audit_scope": "字段类型错误已定位；请修正后再检查来源引用及覆盖。"}
    def issue(code, at, detail=None, severity="error"):
        item = {"severity": severity, "code": code, "at": at}
        if detail is not None:
            item["detail"] = detail
        issues.append(item)

    all_ids = []
    for table, rows in data.items():
        for row in rows:
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier.strip():
                issue("missing_id", table)
            else:
                all_ids.append(identifier)
    for identifier, count in Counter(all_ids).items():
        if count > 1:
            issue("duplicate_id", identifier)
    sources = index(data.get("sources", []))
    facts = index(data.get("facts", []))
    connections = index(data.get("compatibility", []))
    models = index(data.get("models", []))
    for model in sorted(MODELS - set(models)):
        issue("missing_model", model)
    for model in set(models) - MODELS:
        issue("unknown_model", model)

    def check_refs(row, required):
        refs = row.get("source_refs")
        identifier = row.get("id", "?")
        if not isinstance(refs, list) or (required and not refs):
            issue("missing_source_refs", identifier)
            return
        for ref in refs:
            if not isinstance(ref, dict):
                issue("invalid_source_ref", identifier)
                continue
            if not isinstance(ref.get("source_id"), str) or ref.get("source_id") not in sources:
                issue("dangling_source_ref", identifier, ref.get("source_id"))
            if not isinstance(ref.get("locator"), str) or not ref["locator"].strip():
                issue("missing_source_locator", identifier)

    for src in sources.values():
        for field in ("title", "source_type", "region", "language", "read_scope", "summary"):
            if not isinstance(src.get(field), str) or not src[field].strip():
                issue("source_context_missing", src["id"], field)
        if src.get("source_type") not in {"specs", "faq", "manual", "compatibility", "firmware", "store", "support", "index"}:
            issue("invalid_source_type", src["id"])
        if not official_url(src.get("url")):
            issue("not_official_https", src["id"])
        if not valid_date(src.get("checked_at")):
            issue("invalid_checked_date", src["id"])
        if src.get("local_path"):
            path = (root / src["local_path"]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                issue("missing_local_evidence", src["id"], src["local_path"])

    alias_owners = {}
    for model in models.values():
        if not model.get("official_name") or model.get("priority") not in {"primary", "basic"}:
            issue("invalid_model_entry", model["id"])
        for field in ("aliases", "components", "fact_ids"):
            if not text_list(model.get(field)) or not model[field]:
                issue("missing_model_field", model["id"], field)
        for alias in model.get("aliases", []):
            key = normalize(alias)
            if key in alias_owners and alias_owners[key] != model["id"]:
                issue("ambiguous_alias", model["id"], alias)
            alias_owners[key] = model["id"]
        for fid in model.get("fact_ids", []):
            if fid not in facts or model["id"] not in facts[fid].get("models", []):
                issue("invalid_model_fact", model["id"], fid)
        check_refs(model, True)

    for table in ("facts", "compatibility"):
        for row in data.get(table, []):
            identifier = row.get("id", "?")
            if not text_list(row.get("models")) or not row["models"] or not set(row["models"]) <= MODELS:
                issue("invalid_models", identifier)
            for field in ("statement", "component"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    issue("missing_field", identifier, field)
            for field in ("conditions", "limitations"):
                if not text_list(row.get(field)):
                    issue("invalid_list", identifier, field)
            if not valid_date(row.get("checked_at")):
                issue("invalid_checked_date", identifier)
            status = row.get("status")
            if status not in {"verified", "pending", "conflict"}:
                issue("invalid_status", identifier)
            if status in {"pending", "conflict"} and not row.get("gap_reason"):
                issue("missing_gap_reason", identifier)
            check_refs(row, status in {"verified", "conflict"})
            if status == "conflict" and len(row.get("source_refs", [])) < 2:
                issue("conflict_needs_two_locators", identifier)
            if table == "facts" and row.get("topic") not in TOPICS:
                issue("invalid_topic", identifier)
            if table == "compatibility":
                for field in ("transmitter_model", "host", "method"):
                    if not isinstance(row.get(field), str) or not row[field].strip():
                        issue("missing_connection_endpoint", identifier, field)
                if "receiver_model" not in row or (row["receiver_model"] is not None and not isinstance(row["receiver_model"], str)):
                    issue("invalid_receiver", identifier)
                if not text_list(row.get("features")):
                    issue("invalid_list", identifier, "features")
                support = row.get("support")
                if support not in {"supported", "not_supported", "conditional", "unconfirmed"}:
                    issue("invalid_support", identifier)
                if (status == "verified" and support == "unconfirmed") or (status != "verified" and support != "unconfirmed"):
                    issue("support_status_mismatch", identifier)

    for card in data.get("scenarios", []):
        identifier = card.get("id", "?")
        if not text_list(card.get("models")) or not card["models"] or not set(card["models"]) <= MODELS:
            issue("invalid_models", identifier)
        if card.get("kind") != "editorial_synthesis":
            issue("invalid_scenario_kind", identifier)
        for field in ("question", "scenario", "task", "answer"):
            if not isinstance(card.get(field), str) or not card[field].strip():
                issue("missing_scenario_field", identifier, field)
        for field in ("steps", "limitations", "fact_ids", "compatibility_ids"):
            if not text_list(card.get(field)):
                issue("invalid_list", identifier, field)
        if not card.get("fact_ids") and not card.get("compatibility_ids"):
            issue("scenario_without_evidence", identifier)
        for field, registry in (("fact_ids", facts), ("compatibility_ids", connections)):
            for ref in card.get(field, []):
                if ref not in registry:
                    issue("dangling_scenario_ref", identifier, ref)
                elif not set(card.get("models", [])) & set(registry[ref].get("models", [])):
                    issue("cross_model_scenario_ref", identifier, ref)
                elif registry[ref].get("status") != "verified":
                    issue("scenario_uses_unverified_claim", identifier, ref)

    coverage = []
    for model in sorted(MODELS):
        rows = [r for r in data.get("facts", []) if model in r.get("models", [])]
        topics = {t: dict(Counter(r.get("status") for r in rows if r.get("topic") == t)) for t in TOPICS}
        required = TOPICS if model in PRIMARY else ("identity", "audio", "recording", "connections", "kits")
        missing = [t for t in required if not topics[t]]
        for t in missing:
            issue("topic_gap", model, t, severity="warning")
        coverage.append({"model": model, "facts": len(rows), "statuses": dict(Counter(r.get("status") for r in rows)),
            "topics": topics, "missing_topics": missing,
            "compatibility": sum(model in r.get("models", []) for r in data.get("compatibility", [])),
            "scenarios": sum(model in r.get("models", []) for r in data.get("scenarios", []))})
    gaps = [{"id": r.get("id"), "models": r.get("models"), "status": r.get("status"),
             "statement": r.get("statement"), "reason": r.get("gap_reason"), "source_refs": r.get("source_refs", [])}
            for table in ("facts", "compatibility") for r in data.get(table, []) if r.get("status") != "verified"]
    errors = sum(i["severity"] == "error" for i in issues)
    return {"ok": errors == 0, "errors": errors,
            "warnings": sum(i["severity"] == "warning" for i in issues),
            "counts": {t: len(rows) for t, rows in data.items()}, "coverage": coverage, "gaps": gaps, "issues": issues,
            "audit_scope": "本地结构、来源定位与引用一致性；不执行联网有效性或事实正确性判定。"}


def tokens(value):
    s = str(value).lower()
    result = re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", s)
    for part in re.findall(r"[\u4e00-\u9fff]+", s):
        result.extend(part[n:n+2] for n in range(len(part)-1))
        if len(part) == 1:
            result.append(part)
    return result


def searchable(row):
    parts = [row.get(k, "") for k in ("statement", "question", "task", "answer", "scenario", "component", "host", "method")]
    parts.extend(" ".join(row.get(k, [])) for k in ("conditions", "limitations", "keywords", "features", "steps"))
    topic = row.get("topic")
    if topic:
        parts.append(TOPIC_NAMES.get(topic, topic))
    return " ".join(parts)


def expand_query(query):
    words = set(tokens(query))
    for group in SYNONYMS:
        if any(term in query.lower() for term in group):
            for term in group:
                words.update(tokens(term))
    # 常见疑问词不能独自构成产品知识命中。
    words -= {"怎么", "如何", "是否", "可以", "支持", "什么", "哪些", "需要", "使用", "不能", "能否", "一个"}
    return words


def query_models(query):
    """Extract unambiguous product names, preferring the longest full name."""
    masked = str(query).lower()
    requested = set()
    pairs = [(alias, model) for alias, model in ALIASES.items() if alias not in {"mic", "djimic"}]
    pairs += [("初代djimic", "mic"), ("mic初代", "mic")]
    for alias, model in sorted(pairs, key=lambda p: -len(p[0])):
        pattern = r"(?<![a-z0-9])" + r"[\s_-]*".join(re.escape(c) for c in alias) + r"(?![a-z0-9])"
        if re.search(pattern, masked):
            requested.add(model)
            masked = re.sub(pattern, " ", masked)
    # Brand / product tokens alone cannot make an unrelated question relevant.
    masked = re.sub(r"(?<![a-z0-9])(?:dji|mic|mini(?:2s?|3)?)(?![a-z0-9])", " ", masked)
    masked = masked.replace("大疆", " ")
    return requested, masked


def search(data, query, model=None, limit=3):
    named_models, scoring_query = query_models(query)
    if model is not None:
        model = resolve_model(model)
        selected_models = {model}
    else:
        selected_models = named_models or MODELS
        if len(named_models) == 1:
            model = next(iter(named_models))
    candidates = [(table, row) for table in ("facts", "compatibility", "scenarios")
                  for row in data.get(table, []) if selected_models & set(row.get("models", []))]
    queries = expand_query(scoring_query)
    bags = [Counter(tokens(searchable(r))) for _, r in candidates]
    df = Counter(t for bag in bags for t in bag)
    average = sum(sum(b.values()) for b in bags) / max(1, len(bags)) or 1
    registries = {t: index(data.get(t, [])) for t in ("sources", "facts", "compatibility")}

    def enrich(table, row, score):
        out = dict(row, score=round(score, 3))
        evidence = []
        if table == "scenarios":
            for key, registry in (("fact_ids", "facts"), ("compatibility_ids", "compatibility")):
                evidence.extend(registries[registry][fid] for fid in row.get(key, []) if fid in registries[registry])
            out["evidence"] = evidence
        else:
            evidence = [row]
        refs = [ref for item in evidence for ref in item.get("source_refs", []) if isinstance(ref, dict)]
        out["sources"] = [{**registries["sources"][ref["source_id"]], "locator": ref.get("locator", "")}
                          for ref in refs if ref.get("source_id") in registries["sources"]]
        return out

    found = {"facts": [], "compatibility": [], "scenarios": []}
    unresolved = []
    for (table, row), bag in zip(candidates, bags):
        score = 0.0
        length = sum(bag.values())
        for word in queries & bag.keys():
            idf = math.log(1 + (len(bags) - df[word] + 0.5) / (df[word] + 0.5))
            tf = bag[word]
            score += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * length / average))
        if not score:
            continue
        if normalize(query) in normalize(row.get("question", row.get("statement", ""))):
            score += 5
        result = enrich(table, row, score)
        scene_unverified = table == "scenarios" and (not result.get("evidence") or any(
            e.get("status") != "verified" or not set(e.get("models", [])) & set(row.get("models", [])) & selected_models
            for e in result.get("evidence", [])) or
            len(result.get("evidence", [])) != len(row.get("fact_ids", [])) + len(row.get("compatibility_ids", [])))
        if scene_unverified:
            result.update(status="pending", gap_reason="场景证据缺失、尚未核实或不属于所选型号，暂不作为已核验答案。")
        if scene_unverified or (table != "scenarios" and row.get("status") != "verified"):
            unresolved.append(result)
        else:
            found[table].append(result)
    for rows in (*found.values(), unresolved):
        rows.sort(key=lambda r: (-r["score"], r["id"]))
        del rows[limit:]
    return {"query": query, "model": model, "selected_models": sorted(selected_models), "results": found, "unresolved": unresolved,
            "message": "检索结果保留核验日期；写作引用前按实际断言复核当前来源。" if any(found.values())
            else "没有找到相关的已核验记录；不要用其他型号或推测补全答案。"}


def render_search(result):
    selection = ", ".join(result["selected_models"]) if len(result["selected_models"]) < len(MODELS) else "全系列（每条单独标明型号）"
    lines = [f"# Mic 知识检索：{result['query']}", "", f"型号筛选：{selection}", "", result["message"]]
    groups = [("产品事实", result["results"]["facts"]), ("连接兼容", result["results"]["compatibility"]),
              ("场景问答（编辑归纳）", result["results"]["scenarios"]), ("相关待核事项（不能作肯定答案）", result["unresolved"])]
    for title, rows in groups:
        if not rows:
            continue
        lines += ["", f"## {title}"]
        for row in rows:
            lines += ["", f"### {row['id']} · {', '.join(row['models'])}", "", row.get("statement", row.get("question", ""))]
            if "answer" in row:
                lines += ["", row["answer"]]
            if row.get("conditions"):
                lines.append("条件：" + "；".join(row["conditions"]))
            if row.get("limitations"):
                lines.append("限制：" + "；".join(row["limitations"]))
            if row.get("support"):
                lines.append("兼容结论：" + row["support"])
            if row.get("gap_reason"):
                lines.append("待核原因：" + row["gap_reason"])
            if row.get("evidence"):
                lines.append("依据条目：" + "、".join(e["id"] for e in row["evidence"]))
                for e in row["evidence"]:
                    if e.get("conditions"):
                        lines.append(f"{e['id']} 条件：" + "；".join(e["conditions"]))
            if row.get("checked_at"):
                lines.append(f"状态：{row['status']}；核验：{row['checked_at']}")
            seen = set()
            for src in row["sources"]:
                key = (src["id"], src["locator"])
                if key in seen:
                    continue
                seen.add(key)
                lines.append(f"来源：[{src['title']}]({src['url']}) · {src['locator']} · {src['region']} · {src['checked_at']}")
    return "\n\n".join(lines) + "\n"


def render_audit(result):
    lines = ["# Mic 知识库审计", "", f"结构：{'通过' if result['ok'] else '未通过'}；错误 {result['errors']}；提示 {result['warnings']}", "", result["audit_scope"], "", "| 型号 | 事实 | 已核验 | 待核／冲突 | 兼容 | 场景 |", "|---|---:|---:|---:|---:|---:|"]
    for row in result["coverage"]:
        states = row["statuses"]
        lines.append(f"| {row['model']} | {row['facts']} | {states.get('verified', 0)} | {states.get('pending', 0) + states.get('conflict', 0)} | {row['compatibility']} | {row['scenarios']} |")
    lines += ["", f"待核／冲突记录：{len(result['gaps'])}"]
    for item in result["issues"]:
        lines.append(f"- {item['severity']}: {item['code']} @ {item['at']} {item.get('detail', '')}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="知识库目录（默认使用脚本所在库）")
    sub = parser.add_subparsers(dest="command", required=True)
    finder = sub.add_parser("search", help="按中文问题检索，不修改文件或联网")
    finder.add_argument("query")
    finder.add_argument("--model")
    finder.add_argument("--limit", type=int, default=3, help="每类最多返回条数")
    finder.add_argument("--format", choices=("markdown", "json"), default="markdown")
    checker = sub.add_parser("audit", help="检查本地结构、来源定位和覆盖情况")
    checker.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    data, issues = load(args.root)
    if args.command == "audit":
        result = audit(data, issues, args.root)
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render_audit(result), end="\n")
        return 0 if result["ok"] else 1
    if args.limit < 1:
        parser.error("--limit 必须大于零")
    if not args.query.strip():
        parser.error("检索问题不能为空")
    structural = audit(data, issues, args.root)
    if not structural["ok"]:
        print(json.dumps({"error": "知识库结构检查失败；先运行 audit", "issues": structural["issues"]}, ensure_ascii=False), file=sys.stderr)
        return 1
    try:
        result = search(data, args.query, args.model, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render_search(result), end="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
