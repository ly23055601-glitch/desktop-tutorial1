#!/usr/bin/env python3
"""Portable, read-only Mic product and editorial audience retrieval."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "references/knowledge"
spec = importlib.util.spec_from_file_location("mic_knowledge", KNOWLEDGE / "scripts/mic_knowledge.py")
product = importlib.util.module_from_spec(spec)
spec.loader.exec_module(product)
selling_spec = importlib.util.spec_from_file_location("mic_selling_points", KNOWLEDGE / "scripts/mic_selling_points.py")
selling = importlib.util.module_from_spec(selling_spec)
selling_spec.loader.exec_module(selling)
scenes_spec = importlib.util.spec_from_file_location("mic_writing_scenarios", KNOWLEDGE / "scripts/mic_writing_scenarios.py")
scenes = importlib.util.module_from_spec(scenes_spec)
scenes_spec.loader.exec_module(scenes)

LABEL = "编辑推演的潜在人群与心理假设；无用户调研证据，待用户校准。"
STATES = {"status": "editorial_hypothesis", "evidence_status": "not_user_research",
          "origin": "assistant_synthesis_from_thread_discussion", "review_status": "pending_user_calibration"}
LIST_FIELDS = ("aliases", "tags", "motives", "tensions", "behavior_signals",
               "expression_directions", "counterexamples", "scenario_ids")


def audience_load():
    rows, errors = [], []
    try:
        for n, line in enumerate((KNOWLEDGE / "audience/cards.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("record must be object")
                rows.append(row)
            except ValueError as exc:
                errors.append(f"audience:{n}: {exc}")
    except (OSError, UnicodeError) as exc:
        errors.append(str(exc))
    return rows, errors


def audience_audit(rows, errors, scenario_ids):
    errors = list(errors)
    ids = set()
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"MIC-A\d{3}", key):
            errors.append(f"invalid audience id: {key}")
        elif key in ids:
            errors.append(f"duplicate audience id: {key}")
        else:
            ids.add(key)
        for field in ("role", "trigger"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{key}: invalid {field}")
        for field in LIST_FIELDS:
            values = row.get(field)
            if not product.text_list(values) or not values:
                errors.append(f"{key}: invalid {field}")
        for field, value in STATES.items():
            if row.get(field) != value:
                errors.append(f"{key}: {field} must be {value}")
        refs = row.get("scenario_ids")
        if product.text_list(refs):
            for ref in refs:
                if ref not in scenario_ids:
                    errors.append(f"{key}: dangling scenario {ref}")
    if not rows:
        errors.append("empty audience table")
    return {"ok": not errors, "cards": len(rows), "label": LABEL, "errors": errors}


def integrity():
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        expected = manifest["files"]
        if not isinstance(expected, dict) or not expected:
            raise ValueError("invalid file manifest")
        errors = []
        for name, checksum in expected.items():
            path = ROOT / name
            if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
                errors.append(f"unsafe file: {name}")
            elif not path.is_file():
                errors.append(f"missing file: {name}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
                errors.append(f"changed file: {name}")
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()
                  and "__pycache__" not in p.parts and p.name not in ("manifest.json", ".DS_Store")}
        errors += [f"unlisted file: {name}" for name in sorted(actual - set(expected))]
        return {"ok": not errors, "version": manifest.get("version"), "files": len(expected), "errors": errors}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {"ok": False, "errors": [str(exc)]}


def audience_search(rows, query, limit):
    # Generic product/category words carry no role evidence by themselves.
    cleaned = re.sub(r"(?i)dji|mic|mini|大疆|产品|人群|用户|心理|表达|使用|角色", " ", query)
    qtokens = set(product.tokens(cleaned))
    scored = []
    for row in rows:
        headings = " ".join([row["role"]] + row["aliases"] + row["tags"])
        body = " ".join([row["trigger"]] + sum([row[k] for k in LIST_FIELDS if k != "scenario_ids"], []))
        score = 3 * len(qtokens & set(product.tokens(headings))) + len(qtokens & set(product.tokens(body)))
        score += sum(8 for alias in [row["id"], row["role"]] + row["aliases"] if alias.lower() in query.lower())
        if score:
            scored.append((score, row))
    result = [dict(row, score=score) for score, row in sorted(scored, key=lambda x: (-x[0], x[1]["id"]))[:limit]]
    return {"query": query, "kind": "editorial_hypothesis", "label": LABEL, "results": result,
            "message": "场景引用仅指向产品使用问题，不是心理或人群证据。" if result else "没有匹配的角色假设；可换成职业、任务或具体困扰。"}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "search":
        return product.main(argv)
    if argv and argv[0] == "selling-points":
        return selling.main(argv[1:])
    if argv and argv[0] == "scenes":
        return scenes.main(argv[1:])
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    finder = sub.add_parser("audience", help="检索待验证的人群心理假设")
    finder.add_argument("query")
    finder.add_argument("--limit", type=int, default=3)
    finder.add_argument("--format", choices=("markdown", "json"), default="markdown")
    checker = sub.add_parser("audit", help="产品结构、人群标签与包完整性；不联网")
    checker.add_argument("--format", choices=("markdown", "json"), default="markdown")
    sub.add_parser("search", help="产品检索：search 问题 [--model 型号] [--format json]")
    sub.add_parser("selling-points", help="卖点检索：selling-points [问题] [--model 型号] [--format json]")
    sub.add_parser("scenes", help="详细场景与培训选材：scenes [问题] [--model 型号] [--selling-point 卖点ID] [--family 类别] [--format json]")
    args = parser.parse_args(argv)
    data, errors = product.load(KNOWLEDGE)
    rows, audience_errors = audience_load()
    checked = audience_audit(rows, audience_errors, {r.get("id") for r in data["scenarios"]})
    if args.command == "audit":
        product_checked = product.audit(data, errors, KNOWLEDGE)
        package_checked = integrity()
        selling_tables, selling_errors = selling.load(KNOWLEDGE)
        selling_checked = (selling.audit(selling_tables, selling_errors, data, {r.get("id") for r in rows})
                           if product_checked["ok"] else {"ok": False, "errors": ["先修复底层产品结构错误"], "unavailable": []})
        scene_rows, scene_errors = scenes.load(KNOWLEDGE)
        scenes_checked = (scenes.audit(scene_rows, scene_errors, selling_tables, data, {r.get("id") for r in rows})
                          if product_checked["ok"] and selling_checked["ok"] else
                          {"ok": False, "errors": ["先修复产品或卖点结构错误"], "unavailable_routes": []})
        result = {"ok": product_checked["ok"] and checked["ok"] and package_checked["ok"] and selling_checked["ok"] and scenes_checked["ok"],
                  "product": product_checked, "audience": checked, "selling_points": selling_checked,
                  "writing_scenarios": scenes_checked, "package": package_checked}
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(product.render_audit(product_checked))
            print(f"角色心理：{checked['cards']} 张；{LABEL}")
            print(f"资料包完整性：{'通过' if package_checked['ok'] else '失败'}")
            print(f"卖点：{selling_checked.get('cards', 0)} 张；不可直接使用 {len(selling_checked['unavailable'])} 张")
            print(f"详细场景：{scenes_checked.get('cards', 0)} 张；待核路线 {len(scenes_checked['unavailable_routes'])} 条")
            for error in checked["errors"] + package_checked["errors"] + selling_checked["errors"] + scenes_checked["errors"]:
                print(f"- {error}")
        return 0 if result["ok"] else 1
    if args.limit < 1 or not args.query.strip():
        parser.error("问题不能为空，--limit 必须大于零")
    if not checked["ok"]:
        print(json.dumps(checked, ensure_ascii=False), file=sys.stderr)
        return 1
    result = audience_search(rows, args.query, args.limit)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(LABEL + "\n")
        for row in result["results"]:
            print(f"## {row['id']} · {row['role']}\n\n情境：{row['trigger']}")
            for field, label in (("motives", "可能动机"), ("tensions", "矛盾与取舍"),
                                 ("behavior_signals", "待观察行为"), ("expression_directions", "表达方向"),
                                 ("counterexamples", "反例"), ("scenario_ids", "产品场景引用")):
                print(f"\n{label}：" + "；".join(row[field]))
            print("\n状态：editorial_hypothesis / not_user_research / pending_user_calibration\n")
        print(result["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
