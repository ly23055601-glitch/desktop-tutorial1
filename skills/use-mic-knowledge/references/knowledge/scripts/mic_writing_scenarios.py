#!/usr/bin/env python3
"""Detailed editorial scenarios for Mic training selection; not evidence of real posts or experiences."""
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
spec = importlib.util.spec_from_file_location("scenario_selling", ROOT / "scripts/mic_selling_points.py")
selling = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selling)
product = selling.product
FILES = ("creator_learning.jsonl", "people_memories.jsonl", "business_team.jsonl")
FAMILIES = ("创作与学习", "交流与生活记录", "商业与团队协作")
MODEL_NAMES = {"mic": "DJI Mic", "mic_2": "DJI Mic 2", "mic_3": "DJI Mic 3",
               "mic_mini": "DJI Mic Mini", "mic_mini_2": "DJI Mic Mini 2", "mic_mini_2s": "DJI Mic Mini 2S"}
LABEL = "场景、用途与选材方向为编辑推演；心理为待验证假设。并非已采集原帖、实际用户经历或已验收设备组合。"
STATES = {"kind": "editorial_synthesis", "psychology_status": "editorial_hypothesis", "review_status": "pending_user_calibration"}
# Everyday task wording supplements the technical search vocabulary.
SCENE_QUERY_EQUIVALENTS = {
    "四人": ("我们四个", "咱们四个", "四位嘉宾", "四名成员"),
    "读书会": ("聊书", "共读"),
    "手作": ("修模型", "组装模型", "拼模型", "手工制作", "装零件"),
    "双手": ("两只手", "两手"),
    "复用": ("旧麦", "旧 Mini", "旧Mini", "继续搭", "继续用", "接着用", "沿用现有"),
    "增加嘉宾": ("多一个朋友", "多一位朋友", "增加一人", "多了一位搭档", "加一个人", "临时加人"),
    "分声道": ("分开剪", "分别剪", "每人一轨", "每人一个音轨", "各自一轨"),
    "家人": ("家里人", "家里老人", "父母", "长辈"),
    "口述史": ("讲从前", "讲过去", "聊往事", "讲老照片"),
}


def load(root=ROOT):
    rows, errors = [], []
    for name in FILES:
        try:
            for n, line in enumerate((root / "writing_scenarios" / name).read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise ValueError("record must be object")
                    rows.append(row)
                except ValueError as exc:
                    errors.append(f"{name}:{n}: {exc}")
        except (OSError, UnicodeError) as exc:
            errors.append(str(exc))
    return rows, errors


def blocked(route, points, facts, reviews):
    reasons = []
    for sid in route["selling_point_ids"]:
        card = points.get(sid)
        if not card:
            reasons.append(f"卖点缺失：{sid}")
        elif route["model"] not in card["models"]:
            reasons.append(f"{sid} 不属于 {route['model']}")
        else:
            reasons.extend(f"{sid}: {reason}" for reason in selling.ineligible(card, facts, reviews))
    return reasons


def audit(rows, errors, selling_data, product_data, audiences):
    errors, ids, unavailable = list(errors), set(), []
    scalar = ("title", "family", "scene_moment", "user_task", "non_fit")
    arrays = ("audience_ids", "motives", "tensions", "post_cues", "variation_axes", "keywords")
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"MIC-WS\d{3}", key) or key in ids:
            errors.append(f"invalid/duplicate id: {key}")
        else:
            ids.add(key)
        for field in scalar:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{key}: invalid {field}")
        for field in arrays:
            if not product.text_list(row.get(field)) or not row[field]:
                errors.append(f"{key}: invalid {field}")
        for field, expected in STATES.items():
            if row.get(field) != expected:
                errors.append(f"{key}: {field} must be {expected}")
        for field, strings, lists in (("routes", ("model", "setup"), ("selling_point_ids", "conditions", "limitations")),
                                     ("angles", ("focus", "detail"), ())):
            nested = row.get(field)
            if not isinstance(nested, list) or not nested:
                errors.append(f"{key}: invalid {field}")
                continue
            for item in nested:
                if not isinstance(item, dict):
                    errors.append(f"{key}: {field} item must be object")
                    continue
                for name in strings:
                    if not isinstance(item.get(name), str) or not item[name].strip():
                        errors.append(f"{key}: invalid {field}.{name}")
                for name in lists:
                    if not product.text_list(item.get(name)) or not item[name]:
                        errors.append(f"{key}: invalid {field}.{name}")
    if not rows:
        errors.append("empty writing scenario library")
    if errors:
        return {"ok": False, "errors": errors, "unavailable_routes": []}
    points = product.index(selling_data["cards"])
    facts, _ = selling.registries(product_data)
    reviews = product.index(selling_data["reviews"])
    for row in rows:
        if row["family"] not in FAMILIES:
            errors.append(f"{row['id']}: unknown family")
        for aid in row["audience_ids"]:
            if aid not in audiences:
                errors.append(f"{row['id']}: missing audience {aid}")
        models = []
        for route in row["routes"]:
            model = route["model"]
            if model not in product.MODELS or model in models:
                errors.append(f"{row['id']}: unknown/duplicate route model {model}")
            models.append(model)
            for sid in route["selling_point_ids"]:
                if sid not in points:
                    errors.append(f"{row['id']}: missing selling point {sid}")
            reasons = blocked(route, points, facts, reviews)
            if reasons:
                unavailable.append({"id": row["id"], "model": model, "reasons": reasons})
    return {"ok": not errors, "cards": len(rows), "routes": sum(len(r["routes"]) for r in rows),
            "families": dict(Counter(r["family"] for r in rows)),
            "models": dict(Counter(route["model"] for r in rows for route in r["routes"])),
            "errors": errors, "unavailable_routes": unavailable, "label": LABEL}


def search(rows, selling_data, product_data, audiences, query="", model=None, family=None, limit=3, selling_point=None):
    named, content = product.query_models(query)
    selected = {product.resolve_model(model)} if model else (named or product.MODELS)
    content = re.sub(r"使用场景|场景|培训文案|文案|帮我|推荐|有哪些|有什么|展开|发散", " ", content)
    # Look for task phrases before model words are removed: "旧 Mini" still means reuse,
    # while it does not resolve the ambiguous bare product name to a model.
    task_concepts = [term for term, aliases in SCENE_QUERY_EQUIVALENTS.items()
                     if term.casefold() in query.casefold()
                     or any(alias.casefold() in query.casefold() for alias in aliases)]
    expanded = content + " " + " ".join(task_concepts)
    words = product.expand_query(expanded)
    direct_words = set(product.tokens(expanded)) & words
    related_words = words - direct_words
    points = product.index(selling_data["cards"])
    if selling_point is not None and selling_point not in points:
        raise ValueError(f"未知卖点编号：{selling_point}")
    facts, sources = selling.registries(product_data)
    reviews = product.index(selling_data["reviews"])
    found, unresolved = [], []
    for row in rows:
        if family and row["family"] != family:
            continue
        routes = [route for route in row["routes"] if route["model"] in selected
                  and (not selling_point or selling_point in route["selling_point_ids"])]
        if not routes:
            continue
        headline = " ".join([row["title"], row["family"]] + row["keywords"])
        body = " ".join([row["scene_moment"], row["user_task"]] + row["motives"] + row["tensions"] + row["post_cues"]
                        + [angle["focus"] + " " + angle["detail"] for angle in row["angles"]]
                        + [audiences[aid]["role"] for aid in row["audience_ids"] if aid in audiences])
        headline_words, body_words = set(product.tokens(headline)), set(product.tokens(body))
        # Task wording outranks broad technical associations such as people vs. receivers.
        score = (4 * len(direct_words & headline_words) + len(direct_words & body_words)
                 + 0.25 * len(related_words & headline_words))
        # A concrete task concept in the heading beats incidental words such as
        # "电脑" or "声音" when the library contains many neighboring workflows.
        score += 6 * sum(term in headline for term in task_concepts)
        if row["id"].lower() in query.lower():
            score += 100
        if words and not score:
            continue
        valid, unverified = [], []
        for route in routes:
            reasons = blocked(route, points, facts, reviews)
            if reasons:
                unverified.append(dict(route, unavailable_reasons=reasons))
                continue
            selected_points = [points[sid] for sid in route["selling_point_ids"]]
            fact_ids = sorted({fid for point in selected_points for fid in point["fact_ids"]})
            review_ids = sorted({rid for point in selected_points for rid in point["review_ids"]})
            evidence = [facts[fid] for fid in fact_ids]
            refs = sorted({(ref["source_id"], ref["locator"]) for fact in evidence for ref in fact["source_refs"]})
            valid.append(dict(route, selling_points=selected_points, evidence=evidence,
                              reviews=[reviews[rid] for rid in review_ids],
                              sources=[{"id": sid, "title": sources[sid]["title"], "url": sources[sid]["url"],
                                        "locator": locator, "checked_at": sources[sid]["checked_at"]} for sid, locator in refs]))
        if valid:
            found.append(dict(row, score=score, routes=valid, models=[r["model"] for r in valid]))
        if unverified:
            unresolved.append(dict(row, score=score, routes=unverified, models=[r["model"] for r in unverified]))
    for group in (found, unresolved):
        group.sort(key=lambda r: (-r["score"], r["id"]))
        del group[limit:]
    return {"query": query, "selected_models": sorted(selected), "family": family, "selling_point": selling_point,
            "label": LABEL, "results": found, "unresolved": unresolved,
            "message": "按原帖取相关关注点；卡片字段不要求写进同一句或同一帖。" if found else "没有匹配的可用场景路线；保留空结果，不借其他型号补写。"}


def render_card(row, include_evidence=True):
    lines = [f"## {row['id']} · {row['title']}", "", f"类别：{row['family']}；{LABEL}", "",
             f"具体时刻：{row['scene_moment']}", "", f"要完成：{row['user_task']}", "",
             "角色线索：" + "、".join(row["audience_ids"]), "", "可能在意：" + "；".join(row["motives"]),
             "", "取舍：" + "；".join(row["tensions"]), "", "原帖可触发的线索（须实际出现）：" + "；".join(row["post_cues"])]
    for route in row["routes"]:
        lines += ["", f"### {MODEL_NAMES[route['model']]} 候选路线", "", route["setup"], "",
                  "关联卖点：" + "、".join(route["selling_point_ids"]), "",
                  "条件：" + "；".join(route["conditions"]), "", "限制：" + "；".join(route["limitations"])]
        if route.get("unavailable_reasons"):
            lines += ["", "本路线待核，不能作为肯定依据：" + "；".join(route["unavailable_reasons"])]
        if include_evidence:
            for fact in route.get("evidence", []):
                lines += ["", f"依据 {fact['id']}（{fact['component']}；核验 {fact['checked_at']}）：{fact['statement']}",
                          "依据条件／限制：" + "；".join(fact["conditions"] + fact["limitations"])]
            for source in route.get("sources", []):
                lines += [f"来源：[{source['id']}]({source['url']}) · {source['locator']} · 原核验 {source['checked_at']}"]
            for review in route.get("reviews", []):
                lines += [f"卖点复核：{review['id']} · {review['checked_at']} · {review['locator']} · {review['result']}"]
    lines += ["", "### 可取的表达关注点", ""]
    lines += [f"- **{angle['focus']}**：{angle['detail']}" for angle in row["angles"]]
    lines += ["", "不必采用该卖点的情况：" + row["non_fit"], "", "可以怎样继续变化：" + "；".join(row["variation_axes"]),
              "", "状态：editorial_synthesis / editorial_hypothesis / pending_user_calibration"]
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--model")
    parser.add_argument("--family", choices=FAMILIES)
    parser.add_argument("--selling-point", help="按准确卖点 ID 反查场景；与型号、类别和问题取交集")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("--limit 必须大于零")
    data, errors = product.load(ROOT)
    product_report = product.audit(data, errors, ROOT)
    if not product_report["ok"]:
        print(json.dumps(product_report, ensure_ascii=False), file=sys.stderr)
        return 1
    try:
        audiences = product.index([json.loads(line) for line in (ROOT / "audience/cards.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()])
        selling_data, selling_errors = selling.load(ROOT)
        selling_report = selling.audit(selling_data, selling_errors, data, audiences)
        if not selling_report["ok"]:
            print(json.dumps(selling_report, ensure_ascii=False), file=sys.stderr)
            return 1
        rows, errors = load(ROOT)
        report = audit(rows, errors, selling_data, data, audiences)
        if not report["ok"]:
            print(json.dumps(report, ensure_ascii=False), file=sys.stderr)
            return 1
        result = search(rows, selling_data, data, audiences, args.query, args.model, args.family, args.limit, args.selling_point)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Mic 场景与培训选材\n\n" + result["label"] + "\n\n" + result["message"] + "\n")
        for card in result["results"]:
            print(render_card(card))
        for card in result["unresolved"]:
            print("\n# 待核路线\n\n" + render_card(card, include_evidence=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
