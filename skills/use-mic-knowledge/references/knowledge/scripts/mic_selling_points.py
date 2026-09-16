#!/usr/bin/env python3
"""Retrieve evidence-backed editorial selling points without promoting user-value hypotheses to facts."""
from __future__ import annotations
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mic_product", ROOT / "scripts/mic_knowledge.py")
product = importlib.util.module_from_spec(spec)
spec.loader.exec_module(product)
LABEL = "卖点是依据产品事实整理的用途价值；角色适配与收益为编辑归纳，不是用户研究、实测效果或购买保证。"


def load(root=ROOT):
    tables = {"cards": [], "reviews": []}
    errors = []
    for table, names in (("cards", ("basic.jsonl", "mic_3.jsonl", "mic_mini_2s.jsonl")),
                         ("reviews", ("reviews_basic.jsonl", "reviews_mic_3.jsonl", "reviews_mini2s.jsonl"))):
        for name in names:
            path = root / "selling_points" / name
            try:
                for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if line.strip():
                        try:
                            row = json.loads(line)
                            if not isinstance(row, dict):
                                raise ValueError("expected object")
                            tables[table].append(row)
                        except ValueError as exc:
                            errors.append(f"{name}:{line_number}: {exc}")
            except (OSError, UnicodeError) as exc:
                errors.append(str(exc))
    return tables, errors


def registries(data):
    return {r["id"]: r for r in data["facts"] + data["compatibility"]}, product.index(data["sources"])


def ineligible(card, facts, reviews):
    reasons = []
    referenced = [reviews.get(i, {}) for i in card.get("review_ids", [])]
    for fid in card.get("fact_ids", []):
        fact = facts.get(fid)
        if not fact or fact.get("status") != "verified":
            reasons.append(f"{fid} 缺失或尚未核验")
        elif not set(card["models"]).issubset(fact.get("models", [])):
            reasons.append(f"{fid} 不属于本卡型号")
        checks = [r for r in referenced if fid in r.get("fact_ids", [])]
        if not checks or any(r.get("result") != "consistent" for r in checks):
            reasons.append(f"{fid} 缺少一致的卖点来源复核")
    return reasons


def audit(tables, errors, data, audience_ids):
    errors, unavailable = list(errors), []
    facts, sources = registries(data)
    ids = set()
    for table, rows in tables.items():
        for row in rows:
            key = row.get("id")
            if not isinstance(key, str) or not key or key in ids:
                errors.append(f"invalid/duplicate {table} id: {key}")
            elif key in facts or key in sources:
                errors.append(f"id collides with product record: {key}")
            else:
                ids.add(key)
            scalar = ("component", "title", "trigger", "user_value") if table == "cards" else ("source_id", "url", "locator", "checked_at", "note")
            arrays = ("models", "fact_ids", "audience_ids", "conditions", "limitations", "expression_angles", "review_ids", "keywords") if table == "cards" else ("fact_ids",)
            for field in scalar:
                if not isinstance(row.get(field), str) or not row[field].strip():
                    errors.append(f"{key}: invalid {field}")
            for field in arrays:
                if not product.text_list(row.get(field)) or not row[field]:
                    errors.append(f"{key}: invalid {field}")
    if errors:
        return {"ok": False, "errors": errors, "unavailable": []}
    reviews = product.index(tables["reviews"])
    for row in tables["reviews"]:
        key = row["id"]
        if row["source_id"] not in sources or not product.official_url(row["url"]):
            errors.append(f"{key}: missing or nonofficial source")
        if not product.valid_date(row["checked_at"]) or row.get("result") not in ("consistent", "unresolved"):
            errors.append(f"{key}: invalid review date/result")
        for fid in row["fact_ids"]:
            if fid not in facts:
                errors.append(f"{key}: missing fact {fid}")
            elif row["source_id"] not in {r["source_id"] for r in facts[fid]["source_refs"]}:
                errors.append(f"{key}: source not registered for {fid}")
    for card in tables["cards"]:
        key = card["id"]
        if card.get("kind") != "editorial_synthesis" or not set(card["models"]).issubset(product.MODELS):
            errors.append(f"{key}: invalid model/kind")
        for field, registry in (("fact_ids", facts), ("audience_ids", audience_ids), ("review_ids", reviews)):
            for ref in card[field]:
                if ref not in registry:
                    errors.append(f"{key}: missing {field} {ref}")
        reasons = ineligible(card, facts, reviews)
        if reasons:
            unavailable.append({"id": key, "reasons": reasons})
    counts = Counter(model for card in tables["cards"] for model in card["models"])
    if set(counts) != product.MODELS:
        errors.append("selling point coverage must include all six models")
    return {"ok": not errors, "cards": len(tables["cards"]), "reviews": len(tables["reviews"]),
            "models": dict(sorted(counts.items())), "errors": errors, "unavailable": unavailable, "label": LABEL}


def search(tables, data, query="", model=None, limit=6):
    named, content_query = product.query_models(query)
    selected = {product.resolve_model(model)} if model else (named or product.MODELS)
    content_query = re.sub(r"有什么|有哪些|介绍一下|卖点|产品|核心|优势|推荐|介绍|帮我", " ", content_query)
    words = product.expand_query(content_query) - {"卖点", "产品", "核心", "优势", "推荐", "介绍", "一下", "理由"}
    facts, sources = registries(data)
    reviews = product.index(tables["reviews"])
    found, unresolved = [], []
    for card in tables["cards"]:
        if not set(card["models"]) & selected:
            continue
        heading = " ".join([card["title"]] + card["keywords"])
        body = " ".join([card["trigger"], card["user_value"]] + card["expression_angles"])
        score = 3 * len(words & set(product.tokens(heading))) + len(words & set(product.tokens(body)))
        if words and not score:
            continue
        evidence = [facts[fid] for fid in card["fact_ids"] if fid in facts]
        refs = {(r["source_id"], r["locator"]) for f in evidence for r in f["source_refs"]}
        result = dict(card, score=score, evidence=evidence,
                      sources=[dict(sources[sid], locator=locator) for sid, locator in sorted(refs) if sid in sources],
                      reviews=[reviews[rid] for rid in card["review_ids"] if rid in reviews])
        reasons = ineligible(card, facts, reviews)
        if reasons:
            unresolved.append(dict(result, unavailable_reasons=reasons))
        else:
            found.append(result)
    for rows in (found, unresolved):
        rows.sort(key=lambda r: (-r["score"], r["id"]))
        del rows[limit:]
    return {"query": query, "selected_models": sorted(selected), "label": LABEL, "results": found, "unresolved": unresolved,
            "message": "按当前任务选择相关卖点，不要求凑全；原事实核验日与本次复核日分别保留。" if found else "没有可直接使用的匹配卖点；请检查型号、关键词或待核依据。"}


def render(result):
    lines = ["# Mic 卖点检索", "", result["label"], "", result["message"]]
    for card in result["results"]:
        lines += ["", f"## {card['id']} · {', '.join(card['models'])} · {card['title']}", "",
                  f"适用情境：{card['trigger']}", f"用途价值（编辑归纳）：{card['user_value']}",
                  "角色线索：" + "、".join(card["audience_ids"]), "条件：" + "；".join(card["conditions"]),
                  "限制：" + "；".join(card["limitations"]), "表达方向：" + "；".join(card["expression_angles"])]
        for fact in card["evidence"]:
            lines.append(f"依据 {fact['id']}（{fact['component']}；{fact['checked_at']}）：{fact['statement']}")
            lines.append("依据条件／限制：" + "；".join(fact["conditions"] + fact["limitations"]))
        for review in card["reviews"]:
            lines.append(f"卖点复核：[{review['source_id']}]({review['url']}) · {review['locator']} · {review['checked_at']} · {review['result']}")
    for card in result["unresolved"]:
        lines += ["", f"待核卖点 {card['id']}（不能作肯定依据）：" + "；".join(card["unavailable_reasons"])]
    return "\n\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--model")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("--limit 必须大于零")
    data, data_errors = product.load(ROOT)
    product_check = product.audit(data, data_errors, ROOT)
    if not product_check["ok"]:
        print(json.dumps(product_check, ensure_ascii=False), file=sys.stderr)
        return 1
    tables, errors = load(ROOT)
    try:
        audiences = {json.loads(line)["id"] for line in (ROOT / "audience/cards.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()}
        checked = audit(tables, errors, data, audiences)
        if not checked["ok"]:
            print(json.dumps(checked, ensure_ascii=False), file=sys.stderr)
            return 1
        result = search(tables, data, args.query, args.model, args.limit)
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
