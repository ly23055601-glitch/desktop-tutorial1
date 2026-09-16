#!/usr/bin/env python3
"""Read-only, offline lookup of the Mobile knowledge package's JSONL records."""

import argparse
import json
import sys
from pathlib import Path


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
MODELS = (
    "osmo_mobile_8p",
    "osmo_mobile_8",
    "osmo_mobile_7p",
    "osmo_mobile_7",
    "osmo_mobile_6",
    "osmo_mobile_se",
    "dji_om_5",
)
NO_MATCH = "本库未找到依据，不等于不支持"


class KnowledgeError(Exception):
    """The on-disk evidence is incomplete or cannot be read reliably."""


def jsonl_rows(pattern):
    paths = sorted(KNOWLEDGE_ROOT.glob(pattern))
    if not paths:
        raise KnowledgeError(f"未找到 {pattern}；脚本应位于知识库的 scripts/ 下")
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise KnowledgeError(f"{path}:{line_number}: JSON 无法解析：{exc.msg}") from exc
                if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                    raise KnowledgeError(f"{path}:{line_number}: 记录须有字符串 id")
                yield row, {"path": str(path.resolve()), "line": line_number}


def load_knowledge():
    records, record_locations, sources, source_locations = [], {}, {}, {}
    for pattern in ("products/*.facts.jsonl", "compatibility/*.jsonl"):
        for row, location in jsonl_rows(pattern):
            record_id = row["id"]
            if record_id in record_locations:
                raise KnowledgeError(f"事实或兼容记录 id 重复：{record_id}")
            models = row.get("models")
            if not isinstance(models, list) or not models or any(m not in MODELS for m in models):
                raise KnowledgeError(f"{record_id}: models 须使用明确的七种型号 ID")
            if row.get("status") not in ("verified", "pending", "conflict"):
                raise KnowledgeError(f"{record_id}: status 无效")
            if not isinstance(row.get("source_refs"), list):
                raise KnowledgeError(f"{record_id}: 缺少 source_refs 数组")
            if pattern.startswith("compatibility/") and models != [row.get("gimbal_model")]:
                raise KnowledgeError(f"{record_id}: 兼容记录的 models 与 gimbal_model 不一致")
            records.append(row)
            record_locations[record_id] = location
    for row, location in jsonl_rows("sources/*.jsonl"):
        if row["id"] in sources:
            raise KnowledgeError(f"官方来源 id 重复：{row['id']}")
        sources[row["id"]] = row
        source_locations[row["id"]] = location
    return records, record_locations, sources, source_locations


def string_values(value):
    """Match original string values, without regex, aliases or JSON escaping."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from string_values(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from string_values(item)


def source_file(relative_path, source_id):
    if not isinstance(relative_path, str) or not relative_path:
        raise KnowledgeError(f"{source_id}: 来源文件路径必须是非空字符串")
    relative = Path(relative_path)
    absolute = (KNOWLEDGE_ROOT / relative).resolve()
    if relative.is_absolute() or not absolute.is_relative_to(KNOWLEDGE_ROOT):
        raise KnowledgeError(f"{source_id}: 来源文件必须位于知识库内：{relative_path}")
    return {
        "relative_path": relative_path,
        "absolute_path": str(absolute),
        "exists": absolute.is_file(),
    }


def run_query(args):
    records, locations, sources, source_locations = load_knowledge()
    matched = []
    for record in records:
        if args.model and args.model not in record["models"]:
            continue
        if args.record_id is not None and record["id"] != args.record_id:
            continue
        if args.keyword and not any(
            keyword in value
            for value in string_values(record)
            for keyword in args.keyword
        ):
            continue
        matched.append(record)

    # A supplied model remains in scope even when its keyword/id has no match.
    # Without --model, derive scope only from exact models of matched records.
    gap_models = [args.model] if args.model else [
        model for model in MODELS if any(model in row["models"] for row in matched)
    ]
    model_gaps = [
        row for row in records
        if row["status"] in ("pending", "conflict")
        and any(model in row["models"] for model in gap_models)
    ]
    included = {row["id"]: row for row in matched + model_gaps}
    source_ids = set()
    for row in included.values():
        for reference in row["source_refs"]:
            if not isinstance(reference, dict) or not isinstance(reference.get("source_id"), str):
                raise KnowledgeError(f"{row['id']}: 来源引用格式无效")
            source_id = reference["source_id"]
            if source_id not in sources:
                raise KnowledgeError(f"{row['id']}: 未找到来源 {source_id}")
            source_ids.add(source_id)

    selected_sources, files, warnings = [], {}, []
    for source_id in sorted(source_ids):
        source = sources[source_id]
        selected_sources.append(source)  # Preserve the original source row verbatim.
        paths = {"local_path": source_file(source.get("local_path"), source_id)}
        if source.get("snapshot_path"):
            paths["snapshot_path"] = source_file(source["snapshot_path"], source_id)
        if source.get("visual_paths"):
            if not isinstance(source["visual_paths"], list):
                raise KnowledgeError(f"{source_id}: visual_paths 必须是数组")
            paths["visual_paths"] = [source_file(p, source_id) for p in source["visual_paths"]]
        for value in paths.values():
            for file_info in value if isinstance(value, list) else [value]:
                if not file_info["exists"]:
                    warnings.append(f"证据文件缺失：{source_id} → {file_info['absolute_path']}")
        files[source_id] = paths

    if not args.model and not matched:
        warnings.append("未指定精确型号且无命中，无法确定应返回哪些型号的待核或冲突项。")
    return {
        "knowledge_root": str(KNOWLEDGE_ROOT),
        "query": {"model": args.model, "id": args.record_id, "keywords": args.keyword},
        "message": (
            f"命中 {len(matched)} 条。请同时阅读 model_gaps；pending/conflict 不作肯定能力依据。"
            if matched else NO_MATCH
        ),
        "matched_count": len(matched),
        "matched": matched,
        "gap_models": gap_models,
        "model_gaps": model_gaps,
        "sources": selected_sources,
        "source_files": files,
        "record_locations": {key: locations[key] for key in included},
        "source_locations": {key: source_locations[key] for key in sorted(source_ids)},
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "离线、只读检索 Mobile 产品事实及兼容 JSONL。"
            "保留完整原记录、官方来源与绝对文件路径；不默认只筛 verified。"
        ),
        epilog=(
            "至少提供一个查询条件。型号、ID、关键词三组条件按 AND 组合；"
            "重复 --keyword 按 OR 组合。关键词对记录全部字符串值作区分大小写的字面子串匹配，"
            "不使用正则或别名。--model 单独使用返回该型号全部事实/兼容记录。"
            "model_gaps 始终包括所选型号的全部 pending/conflict，不受 ID/关键词筛选；"
            "未指定型号时，仅从命中记录的明确型号确定范围。"
            "原件/快照路径见 source_files；source_locations/record_locations 提供 JSONL 行位置。"
            "本工具不联网、不写文件，不检索人群或场景资料，也不重新校验证据哈希。"
            "正常查询（含无命中）退出码0，知识数据错误1，参数错误2。"
        ),
    )
    parser.add_argument("--model", choices=MODELS, help="精确型号 ID；不接受 OM、8、Mobile 等模糊简称")
    parser.add_argument("--id", dest="record_id", help="完整事实/兼容记录 ID，区分大小写，精确匹配")
    parser.add_argument("--keyword", action="append", default=[], metavar="TEXT", help="字面子串，可重复；多个词满足其一即可")
    args = parser.parse_args()
    if not (args.model or args.record_id is not None or args.keyword):
        parser.error("空查询会返回过多资料；请提供 --model、--id 或 --keyword")
    if args.record_id is not None and not args.record_id.strip():
        parser.error("--id 不能为空")
    if any(not keyword.strip() for keyword in args.keyword):
        parser.error("--keyword 不能为空或仅含空白")
    try:
        result = run_query(args)
    except (KnowledgeError, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc), "knowledge_root": str(KNOWLEDGE_ROOT)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
