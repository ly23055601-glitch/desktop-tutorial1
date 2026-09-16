#!/usr/bin/env python3
"""Build a read-only Pocket knowledge brief from the canonical retrieval tables."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def sibling(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = sibling("pocket_knowledge")
materials = sibling("pocket_materials")
SECTION_TITLES = {"facts": "产品事实", "needs": "处境与需求", "voice": "真实表达与承接",
                  "comparisons": "竞品与代际比较个案", "selling": "卖点与使用价值（编辑解释）",
                  "detailed_scenes": "详细场景（待验证假设）"}


def read_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def stopped_sources(root):
    """Read only stop metadata, never the stopped attachments themselves."""
    state = read_json(root / "corpus/run-state.json", {})
    plan = read_json(root / "corpus/collection-plan.json", {})
    entries = [(b, "corpus/") for b in state.get("batches", [])
               if b.get("stopped_by_user") or b.get("status") in {"stopped_by_user", "partial_saved_unreviewed_user_stop"}]
    entries += [(b, "") for b in plan.get("current_scope", {}).get("retained_unreviewed_exports", [])]
    paths, hashes = set(), set()
    for item, prefix in entries:
        for key in ("source_sha256", "normalized_sha256"):
            if item.get(key):
                hashes.add(item[key])
        for key in ("source_path", "raw_path", "export_path", "original_export_path", "normalized_path"):
            value = item.get(key)
            if not isinstance(value, str):
                continue
            for candidate in (value, prefix + value if not Path(value).is_absolute() else value):
                resolved = core.source_path(root, candidate)
                if resolved:
                    paths.add(str(resolved.resolve()))
    return paths, hashes


def candidate_models(record, works):
    """Use discussion candidates as bounds, never as proof of ownership."""
    def declared(item):
        values = []
        for key in ("model_candidates", "discussion_model_candidates"):
            value = item.get(key, [])
            values.extend(value if isinstance(value, list) else [value])
        return {core.model_id(value) for value in values} - {"unknown"}

    candidates = declared(record)
    if core.model_id(record.get("model_id")) == "unknown" and not candidates:
        work = works.get(record.get("work_id"), {})
        candidates = declared(work)
        if not candidates:
            candidates = {core.model_id(record.get("work_model_id")), core.model_id(work.get("model_id"))} - {"unknown"}
    return candidates


def safe_tables(root, data, gaps):
    """Add source-presence/stop gates without rewriting either search engine."""
    data = {key: list(rows) for key, rows in data.items()}
    works = {w["work_id"]: w for w in data["works"]}
    blocked_paths, blocked_hashes = stopped_sources(root)

    def blocked(item):
        if not isinstance(item, dict):
            return False
        if item.get("split") == "holdout" or item.get("included_in_learning") is False:
            return True
        if item.get("status") in {"stopped_by_user", "partial_saved_unreviewed_user_stop"}:
            return True
        for key, value in item.items():
            if key.endswith("sha256") and isinstance(value, str) and value in blocked_hashes:
                return True
            if key in {"source_path", "raw_path", "normalized_path", "original_export", "original_export_path", "original_file"}:
                path = core.source_path(root, value)
                if path and str(path.resolve()) in blocked_paths:
                    return True
            if isinstance(value, dict) and blocked(value):
                return True
            if isinstance(value, list) and any(blocked(v) for v in value if isinstance(v, dict)):
                return True
        return False

    blocked_work_ids = {wid for wid, work in works.items() if blocked(work)}
    data["works"] = [work for wid, work in works.items() if wid not in blocked_work_ids]

    def source_present(item):
        if blocked(item):
            return False
        path = core.source_path(root, item.get("source_path"))
        locator = item.get("source_locator") or item.get("json_pointer")
        return bool(path and path.is_file() and locator)

    def work_allowed(wid, legacy=False):
        work = works.get(wid)
        # Historical records retain their original work IDs outside the newer
        # candidate table; absence is permissible only for explicit legacy rows.
        return wid not in blocked_work_ids and (bool(work) or bool(not work and legacy and wid))

    for table in ("records", "comments"):
        before = len(data[table])
        data[table] = [r for r in data[table] if source_present(r) and r.get("text")
                       and work_allowed(r.get("work_id"), r.get("split") == "legacy")]
        if before != len(data[table]):
            gaps.append({"code": "excluded_unavailable_or_protected_records", "table": table,
                         "count": before - len(data[table])})
    records = {r["id"]: r for key in ("records", "comments") for r in data[key]}
    record_ids = set(records)
    data["voice"] = [c for c in data["voice"] if not blocked(c) and core.evidence_ids(c)
                     and set(core.evidence_ids(c)) <= record_ids
                     and (c.get("status") != "pattern" or len({records[i]["work_id"] for i in core.evidence_ids(c)}) >= 3)]
    voice_ids = {v["id"] for v in data["voice"]}

    # Reuse the core fact gate for all downstream references, including material
    # cards whose facts might not rank in the short initial query.
    fact_view = {key: [] for key in core.TABLES}
    fact_view["sources"] = data["sources"]
    valid_fact_ids = set()
    for fact in data["facts"]:
        fact_view["facts"] = [fact]
        if fact.get("id") and core.retrieve(root, fact_view, fact["id"], limit=1)["facts"]:
            valid_fact_ids.add(fact["id"])
    data["facts"] = [f for f in data["facts"] if f.get("id") in valid_fact_ids or f.get("status") == "pending"]

    def safe_need(card):
        if blocked(card) or not set(card.get("product_fact_ids", [])) <= valid_fact_ids:
            return False
        if not set(card.get("voice_card_ids", [])) <= voice_ids:
            return False
        if any(not work_allowed(wid, card.get("split") == "legacy") for wid in card.get("evidence_work_ids", [])):
            return False
        refs = card.get("source_post_locators", [])
        if any(not source_present(ref) or not work_allowed(ref.get("work_id"), card.get("split") == "legacy") for ref in refs):
            return False
        return bool(card.get("voice_card_ids") or refs or card.get("basis") == "editorial_hypothesis")

    data["scenarios"] = [c for c in data["scenarios"] if safe_need(c)]
    data["comparisons"] = [c for c in data.get("comparisons", []) if not blocked(c)]
    return data


def retrieval_view(data, model, query, known_ids):
    """Keep complete evidence while narrowing this query's matching records.

    The core engine's local allowed_record gate accepts only the selected model
    or unknown. A private transient scope makes conflicting candidates fail
    that gate without deleting evidence needed for pattern/work-count checks.
    Original model IDs are restored in all returned records, never persisted.
    Comparison cards keep their full opposing viewpoints and own model scope.
    """
    view = {key: list(rows) for key, rows in data.items()}
    if model and model != "unknown":
        works = {work["work_id"]: work for work in data["works"]}
        for table in ("records", "comments"):
            view[table] = [{**record, "model_id": "__brief_model_scope_mismatch__"}
                           if candidate_models(record, works) and model not in candidate_models(record, works) else record
                           for record in data[table]]
    for table in ("scenarios", "voice", "comparisons"):
        if query in known_ids[table]:
            # Recognize exact intent even when its card failed a protection
            # gate: rejection must not substitute a similarly named card.
            view[table] = [card for card in view[table] if card["id"] == query]
    return view


def catalog_paths(root, query, competitor, limit, skills_root, gaps):
    catalog = read_json(root / "library.json")
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1:
        raise ValueError("library.json requires schema_version 1")

    def document(entry):
        if not isinstance(entry, str) or not entry or Path(entry).is_absolute():
            gaps.append({"code": "invalid_document_path", "entry": entry})
            return None
        path = (root / entry).resolve()
        if not path.is_relative_to(root) or any(part in {"holdout", "evaluation", "_provenance"} for part in Path(entry).parts):
            gaps.append({"code": "protected_or_external_document", "entry": entry})
            return None
        if not path.is_file():
            gaps.append({"code": "missing_document", "entry": entry})
            return None
        return {"entry": entry, "resolved_path": str(path), "body_read": False}

    terms = core.tokens(query + " " + (competitor or ""))
    ranked = []
    for item in catalog.get("domains", []):
        score = core.relevance({k: item.get(k) for k in ("id", "title", "tags")}, terms)
        if score:
            ranked.append((score, item))
    docs = []
    for _, item in sorted(ranked, key=lambda x: (-x[0], x[1]["id"])):
        reference = document(item.get("entry"))
        if reference:
            docs.append({**{k: item.get(k) for k in ("id", "title", "kind")}, **reference})
        if len(docs) == limit:
            break
    context = document(catalog.get("context_entry"))
    skills_root = Path(skills_root) if skills_root else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
    routes = []
    for item in catalog.get("routes", []):
        name = item.get("skill")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            gaps.append({"code": "invalid_skill_name", "route_id": item.get("id")})
            continue
        path = (skills_root / name / "SKILL.md").absolute()
        routes.append({**{k: item.get(k) for k in ("id", "title", "skill", "scope")},
                       "resolved_path": str(path), "available": path.is_file(), "body_read": False})
    return docs, context, routes


def material_data(root, data, gaps):
    selected = {key: data[key] for key in ("facts", "sources", "voice")}
    for key in ("selling", "scene"):
        path = root / materials.TABLES[key]
        try:
            selected[key] = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            selected[key] = [c for c in selected[key] if c.get("split") != "holdout"
                             and c.get("status") not in {"stopped_by_user", "partial_saved_unreviewed_user_stop"}
                             and c.get("included_in_learning") is not False]
        except (OSError, ValueError) as exc:
            selected[key] = []
            gaps.append({"code": "material_table_unavailable", "table": key, "detail": str(exc)})
    # Removing a bad selling card may invalidate a scene that references it.
    for _ in range(2):
        check = materials.audit(selected)
        bad_ids = {issue.get("id") for issue in check["issues"]}
        if not bad_ids:
            break
        gaps.append({"code": "excluded_invalid_materials", "ids": sorted(str(x) for x in bad_ids)})
        for key in ("selling", "scene"):
            selected[key] = [c for c in selected[key] if c.get("id") not in bad_ids]
    return selected


def cited_facts(root, data, layers, model):
    """Resolve every selected card's fact references, independent of rank limit."""
    cited_by = {}
    for key in ("needs", "comparisons", "selling", "detailed_scenes"):
        for card in layers[key]:
            for identifier in card.get("fact_ids", card.get("available_product_fact_ids", [])):
                cited_by.setdefault(identifier, [])
                if card["id"] not in cited_by[identifier]:
                    cited_by[identifier].append(card["id"])
    view = {key: [] for key in core.TABLES}
    view.update(facts=data["facts"], sources=data["sources"])
    resolved = []
    for identifier, cards in cited_by.items():
        matches = core.retrieve(root, view, identifier, model=model, limit=1)["facts"]
        for fact in matches:
            if fact["id"] == identifier:
                resolved.append({**{k: v for k, v in fact.items() if k != "writing_gate"}, "referenced_by": cards})
    return resolved


def mark_unknown_expression(layers, data):
    records = {r["id"]: r for table in ("records", "comments") for r in data[table]}
    works = {work["work_id"]: work for work in data["works"]}
    for key in ("voice", "comparisons"):
        for card in layers[key]:
            for row in card.get("matched_records", []):
                original = records.get(row["id"], {})
                row["model_id"] = original.get("model_id", "unknown")
                if core.model_id(row.get("model_id")) != "unknown":
                    continue
                candidates = candidate_models(original, works)
                row["model_candidates"] = sorted(candidates)
                row["model_expression_scope"] = "candidate_context_only" if candidates else "generic_expression_only"
                row["model_notice"] = ("型号未明；候选只限定讨论语境，不证明持有、使用或原片设备。" if candidates else
                                       "型号及候选均未明；仅作通用表达参考，不能确认筛选型号的使用经历或原片设备。")


def brief(root, query, model=None, platform=None, competitor=None, limit=3, skills_root=None):
    root = Path(root).resolve()
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 10:
        raise ValueError("limit requires 1–10")
    if platform and platform not in core.PLATFORMS:
        raise ValueError("unknown platform")
    # An exact model-name query is explicit; a mixed-model question is not a
    # reason to infer the shooting device or silently choose the newer model.
    selected_model = core.model_id(model) if model is not None else None
    if selected_model is None and core.model_id(query) != "unknown":
        selected_model = core.model_id(query)
    gaps = []
    docs, context, routes = catalog_paths(root, query, competitor, limit, skills_root, gaps)
    data, issues = core.load(root)
    gaps.extend(issues)
    known_ids = {table: {card.get("id") for card in data[table]} for table in ("scenarios", "voice", "comparisons")}
    data = safe_tables(root, data, gaps)
    if selected_model == "unknown":
        gaps.append({"code": "unknown_model", "requested_model": model,
                     "notice": "型号未明；未借用 Pocket4/4P 事实或场景。可明确型号后检索。"})
        data = {key: [] for key in core.TABLES}
    if selected_model:
        data["scenarios"] = [c for c in data["scenarios"] if not c.get("target_models") or selected_model in c["target_models"]]
    view = retrieval_view(data, selected_model, query.strip(), known_ids)
    result = core.retrieve(root, view, query, model=selected_model, platform=platform, competitor=competitor, limit=limit)
    layered = {"facts": [{k: v for k, v in f.items() if k != "writing_gate"} for f in result["facts"]],
               "needs": result["scenarios"], "voice": result["voice"], "comparisons": result.get("comparisons", []),
               "selling": [], "detailed_scenes": []}
    for need in layered["needs"]:
        need["source_post_locators"] = [{**ref, "resolved_source_path": str(core.source_path(root, ref["source_path"]))}
                                         for ref in need.get("source_post_locators", [])]
    if selected_model in {None, *materials.MODELS}:
        extra = materials.search(material_data(root, data, gaps), query, model=selected_model, limit=limit)
        layered.update(selling=extra["selling"], detailed_scenes=extra["scene"])
    else:
        gaps.append({"code": "material_model_not_covered", "model": selected_model,
                     "notice": "当前卖点与详细场景库只覆盖 Pocket4/4P；旧代或未明型号不借用。"})
    mark_unknown_expression(layered, data)
    references = cited_facts(root, data, layered, selected_model)
    return {"schema_version": 1, "mode": "read_only_knowledge_brief", "query": query, "model": selected_model,
            "platform": platform, "competitor": competitor, "holdout_included": False,
            "sections": layered, "counts": {key: len(rows) for key, rows in layered.items()},
            "referenced_facts": references,
            "pending_gaps": result["pending_gaps"], "follow_up": result["follow_up"],
            "documents": docs, "context": context, "routes": routes, "gaps": gaps,
            "boundaries": ["本简报只检索既有资料，不采集、写稿、发布或修改原表。",
                           "产品事实保留型号、条件、官方来源与核验日期；进入稿件前按当前产品写作入口再核验。",
                           "公共原话、比较个案与用户明确反馈分开；第三方经历不证明产品能力，也不转为他人亲历。",
                           "卖点价值是编辑解释，详细场景是待验证假设；模式与具体操作不能靠拼接字段补齐。",
                           "未指定型号时结果保留各卡适用范围，不确认当前原帖拍摄设备；未匹配不等于不支持。",
                           "本入口检索已入库材料，检查来源存在与引用关联；原始行列、原句与哈希的完整核对由入库和独立审读验收负责。",
                           "已排除留出及停止附件；文档与外部技能仅给出当前路径，未读取正文或复制写法版本。"]}


def render(result):
    def text(value):
        if isinstance(value, dict):
            return "；".join(f"{key}：{text(part)}" for key, part in value.items())
        if isinstance(value, list):
            return "；".join(text(part) for part in value)
        return str(value)

    def fact_lines(fact):
        output = [f"- **{fact['id']}｜{fact.get('title', '')}**",
                  f"  型号：{text(fact.get('models', []))}；事实核验：{fact.get('checked_at')}"]
        for field, label in (("fact", "事实"), ("conditions", "条件"), ("not_infer", "不可推断"), ("referenced_by", "引用卡片")):
            if fact.get(field):
                output.append(f"  {label}：{text(fact[field])}")
        for source in fact.get("sources", []):
            output.append(f"  [官方来源]({source['url']}) · {source.get('locator')} · 来源核验 {source.get('checked_at')}")
        return output

    lines = [f"# Pocket 知识简报：{result['query']}"]
    if result["model"]:
        lines.append(f"\n型号筛选：{result['model']}")
    for key, title in SECTION_TITLES.items():
        rows = result["sections"][key]
        lines.append(f"\n## {title}\n")
        if not rows:
            lines.append("未匹配到可用材料。")
        for row in rows:
            if key == "facts":
                lines.extend(fact_lines(row))
                continue
            lines.append(f"- **{row['id']}｜{row.get('title', '')}**")
            for field in ("need", "mechanism", "analysis", "user_value", "user_task", "model_notes", "conditions", "not_infer", "not_suitable",
                          "status", "evidence_scope", "not_transferable", "boundaries", "limitations"):
                value = row.get(field)
                if value:
                    lines.append("  " + field + "：" + text(value))
            for record in row.get("matched_records", []):
                lines.append(f"  原话 {record['id']}：{record.get('text')}；[证据]({record.get('resolved_source_path')}) · {record.get('source_locator')}")
                if record.get("parent_text"):
                    lines.append(f"  直接父句：{record['parent_text']}")
                if record.get("model_notice"):
                    lines.append("  型号边界：" + record["model_notice"])
            for ref in row.get("matched_sources", []):
                if not ref.get("evidence_id"):
                    lines.append(f"  作者原话：{ref.get('quote')}；[证据]({ref.get('resolved_source_path')}) · {ref.get('source_locator')}")
            for ref in row.get("source_post_locators", []):
                lines.append(f"  [场景来源]({ref.get('resolved_source_path')}) · {ref.get('source_locator', ref.get('json_pointer'))}")
            refs = row.get("fact_ids", row.get("available_product_fact_ids", []))
            if refs:
                lines.append("  关联事实：" + "、".join(refs))
    displayed = {fact["id"] for fact in result["sections"]["facts"]}
    references = [fact for fact in result.get("referenced_facts", []) if fact["id"] not in displayed]
    if references:
        lines.append("\n## 所选卡片引用的产品事实（按 ID 去重）\n")
        for fact in references:
            lines.extend(fact_lines(fact))
    lines.append("\n## 按需文档与当前路由\n")
    for doc in result["documents"]:
        lines.append(f"- [{doc['title']}]({doc['resolved_path']})（{doc['kind']}；正文未读）")
    if result["context"]:
        lines.append(f"- [上下文与边界]({result['context']['resolved_path']})（正文未读）")
    for route in result["routes"]:
        lines.append(f"- [{route['title']}]({route['resolved_path']})：{route['scope']}（{'当前文件可用' if route['available'] else '当前文件缺失'}；正文未读）")
    if result["pending_gaps"] or result["gaps"]:
        lines.append("\n## 待核与缺口\n")
        lines.extend("- " + json.dumps(gap, ensure_ascii=False) for gap in result["pending_gaps"] + result["gaps"])
    lines.append("\n## 适用边界\n")
    lines.extend("- " + text for text in result["boundaries"])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    command = parser.add_subparsers(dest="command", required=True).add_parser("brief")
    command.add_argument("query")
    command.add_argument("--model")
    command.add_argument("--platform", choices=sorted(core.PLATFORMS))
    command.add_argument("--competitor")
    command.add_argument("--limit", type=int, default=3)
    command.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args(argv)
    try:
        result = brief(args.root, args.query, args.model, args.platform, args.competitor, args.limit)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": "library_brief_unavailable", "detail": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
