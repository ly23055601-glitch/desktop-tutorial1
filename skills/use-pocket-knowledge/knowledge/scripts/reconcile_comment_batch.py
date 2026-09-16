#!/usr/bin/env python3
"""Reconcile one exported comment batch offline; dry-run unless --apply is explicit.

This consumes an existing normalized export. It neither collects material nor
proves UI completion. Only the root-maintained exported/pending state permits a
write, and collection success remains separate from sampling eligibility.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit, urlunsplit

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
READY = "comments_exported_pending_reconciliation"
METRICS = ("analysis_comment_rows", "text_comment_count", "exported_nonempty_text_count", "textual_content_comment_count", "non_textual_nonempty_comment_count", "non_text_comment_count", "root_text_count", "confirmed_parent_reply_count",
           "distinct_roots_with_confirmed_replies", "missing_direct_parent_reply_count")
MODES = {"pocket_1", "pocket_2", "pocket_3", "pocket_4", "pocket_4p", "unknown"}


class ReconcileError(ValueError):
    pass


def encoded(value, jsonl=False):
    if jsonl:
        return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in value).encode()
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def digest(content):
    return hashlib.sha256(content).hexdigest()


def read_rows(path, snapshots, optional=False):
    content = path.read_bytes() if path.is_file() else None
    snapshots[path] = content
    if content is None:
        if optional:
            return []
        raise ReconcileError(f"Missing required file: {path}")
    result = []
    for line_number, line in enumerate(content.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ReconcileError(f"Invalid JSON at {path.name}:{line_number}") from exc
        if not isinstance(row, dict):
            raise ReconcileError(f"Expected object at {path.name}:{line_number}")
        result.append((line_number, row))
    return result


def unique_index(rows, key, name):
    result = {}
    for row in rows:
        identifier = row.get(key)
        if not isinstance(identifier, str) or not identifier or identifier in result:
            raise ReconcileError(f"Missing or duplicate {key} in {name}")
        result[identifier] = row
    return result


def resolve_source(root, value, corpus_relative=False):
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    candidates = [(root / "corpus" / path), root / path, root.parents[1] / path] if corpus_relative else [root / path, root.parents[1] / path, root / "corpus" / path]
    return next((p.resolve() for p in candidates if p.is_file()), candidates[0].resolve())


def add_unique(values, item):
    if item not in values:
        values.append(item)


def identity(row):
    fields = ("id", "platform", "work_id", "text", "text_status", "parent_id", "root_id", "thread_role", "author_id", "image_urls")
    return json.dumps({key: row.get(key, [] if key == "image_urls" else None) for key in fields}, ensure_ascii=False, sort_keys=True)


def has_text(row):
    return isinstance(row.get("text"), str) and bool(row["text"].strip())


def metrics(rows):
    by_id = {row["id"]: row for row in rows}
    textual = {row["id"] for row in rows if kb_module().has_textual_content(row.get("text"))}
    roots = {row["id"] for row in rows if row["id"] in textual and row.get("thread_role") == "root"
             and not row.get("parent_id") and row.get("root_id") in {None, row["id"]}}
    replies = [row for row in rows if row.get("thread_role") == "reply" and row["id"] in textual]
    confirmed = [row for row in replies if row.get("parent_id") in by_id
                 and row["parent_id"] in textual and by_id[row["parent_id"]].get("work_id") == row.get("work_id")]
    return {"analysis_comment_rows": len(rows), "text_comment_count": sum(has_text(r) for r in rows),
            "exported_nonempty_text_count": sum(has_text(r) for r in rows), "textual_content_comment_count": len(textual),
            "non_textual_nonempty_comment_count": sum(has_text(r) and r["id"] not in textual for r in rows),
            "non_text_comment_count": sum(not has_text(r) for r in rows), "root_text_count": len(roots),
            "confirmed_parent_reply_count": len(confirmed),
            "distinct_roots_with_confirmed_replies": len({r.get("root_id") for r in confirmed} & roots),
            "missing_direct_parent_reply_count": sum(r.get("parent_id") not in by_id for r in replies)}


@lru_cache(maxsize=1)
def kb_module():
    spec = importlib.util.spec_from_file_location("pocket_batch_kb", Path(__file__).with_name("pocket_knowledge.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare(root, batch_id, normalized):
    root, normalized = Path(root).resolve(), Path(normalized).resolve()
    corpus = root / "corpus"
    paths = {name: corpus / name for name in ("comments.jsonl", "works.jsonl", "input-ledger.jsonl", "run-state.json")}
    if normalized in paths.values():
        raise ReconcileError("Normalized input cannot be a destination table")
    snapshots = {}
    incoming = read_rows(normalized, snapshots)
    comments = [row for _, row in read_rows(paths["comments.jsonl"], snapshots, optional=True)]
    works = [row for _, row in read_rows(paths["works.jsonl"], snapshots)]
    ledger = [row for _, row in read_rows(paths["input-ledger.jsonl"], snapshots)]
    snapshots[paths["run-state.json"]] = paths["run-state.json"].read_bytes()
    state = json.loads(snapshots[paths["run-state.json"]])
    selected = [b for b in state.get("batches", []) if b.get("batch_id") == batch_id]
    if len(selected) != 1:
        raise ReconcileError("Batch must identify exactly one run-state entry")
    batch = selected[0]
    if batch.get("kind") not in {"comment", "comments"} and "-comments-" not in batch_id:
        raise ReconcileError("Selected batch is not a comment batch")
    work_ids = batch.get("work_ids", [])
    if not work_ids or any(not isinstance(w, str) or not w for w in work_ids) or len(set(work_ids)) != len(work_ids):
        raise ReconcileError("Batch needs unique string work_ids")
    platform = batch.get("platform")
    if platform not in {"xiaohongshu", "douyin", "bilibili"}:
        raise ReconcileError("Batch platform is unsupported")
    ledger_index = unique_index(ledger, "workId", "input-ledger")
    work_index = unique_index(works, "work_id", "works")
    existing = unique_index(comments, "id", "comments")
    for wid in work_ids:
        if wid not in ledger_index or wid not in work_index:
            raise ReconcileError("A batch work is missing from ledger or works")
        if ledger_index[wid].get("platform") != platform or work_index[wid].get("platform") != platform:
            raise ReconcileError("Batch platform disagrees with ledger or works")
        if ledger_index[wid].get("split") not in {"train", "holdout"}:
            raise ReconcileError("Batch work has no frozen train/holdout split")
        if work_index[wid].get("split") != ledger_index[wid]["split"]:
            raise ReconcileError("Works and ledger disagree on frozen split")
    expected_source = resolve_source(root, batch.get("export_path"), corpus_relative=True)
    blockers = []
    if batch.get("status") != READY:
        blockers.append("batch_not_exported_pending_reconciliation")
    if not expected_source or not expected_source.is_file():
        blockers.append("batch_raw_export_missing")
    normalized_sha = digest(snapshots[normalized])
    gaps, candidates = [], defaultdict(list)
    observed = Counter()
    export_proof = set()
    split_overrides = 0

    def gap(line, row, code):
        gaps.append({"normalized_line": line, "id": row.get("id"), "work_id": row.get("work_id"), "reason": code})

    for line, row in incoming:
        wid = row.get("work_id")
        if wid not in work_ids:
            gap(line, row, "outside_selected_batch")
            continue
        observed[wid] += 1
        if row.get("platform") != platform or row.get("ledger_match") != "matched":
            gap(line, row, "platform_or_ledger_match_unconfirmed")
            continue
        entry = ledger_index[wid]
        if row.get("inputOrder") is not None and str(row["inputOrder"]) != str(entry.get("inputOrder")):
            gap(line, row, "ledger_input_order_mismatch")
            continue
        if row.get("kind") != "comments" or row.get("material_kind", "comment") != "comment" or row.get("thread_role") == "post":
            gap(line, row, "not_a_comment")
            continue
        source = resolve_source(root, row.get("source_path"))
        locator = row.get("source_locator")
        if not source or not source.is_file() or not isinstance(locator, dict) or not locator.get("sheet") or not isinstance(locator.get("row"), int) or locator["row"] < 2:
            gap(line, row, "source_or_table_locator_missing")
            continue
        if source not in snapshots:
            snapshots[source] = source.read_bytes()
        if digest(snapshots[source]) != row.get("source_sha256"):
            gap(line, row, "raw_source_hash_mismatch")
            continue
        if expected_source and source != expected_source:
            gap(line, row, "source_does_not_match_batch_export")
            continue
        export_proof.add(wid)
        if row.get("normalization_status") != "parsed":
            gap(line, row, "normalization_needs_review")
            continue
        if not isinstance(row.get("id"), str) or not row["id"].startswith(platform + ":") or not isinstance(row.get("comment_id"), str) or row["id"] != platform + ":" + row["comment_id"]:
            gap(line, row, "comment_identity_invalid")
            continue
        if row.get("model_id", "unknown") not in MODES:
            gap(line, row, "discussion_model_invalid")
            continue
        if row.get("thread_role") not in {"root", "reply", "unknown"} or any(row.get(k) is not None and not isinstance(row[k], str) for k in ("parent_id", "root_id")):
            gap(line, row, "thread_fields_invalid")
            continue
        if (row.get("text") is not None and not isinstance(row["text"], str)) or (not has_text(row) and row.get("text_status") != "absent_in_export"):
            gap(line, row, "text_status_invalid")
            continue
        split_overrides += row.get("split") != entry["split"]
        fields = ("id", "comment_id", "work_id", "platform", "text", "text_status", "image_urls", "parent_id", "root_id", "thread_role",
                  "parent_basis", "parent_lookup", "parent_source_locator", "referenced_comment_text", "root_comment_text", "parent_quote_source_locator",
                  "author_id", "author_name", "collected_at", "created_at", "comment_likes", "reported_reply_count", "read_scope", "limitations", "source_columns")
        record = {key: copy.deepcopy(row[key]) for key in fields if key in row}
        canonical = urlsplit(str(entry.get("canonicalUrl") or ""))
        record.update({"kind": "comments", "material_kind": "comment", "source_kind": "public_comment", "speaker_scope": "comment_author",
                       "canonical_url": urlunsplit((canonical.scheme, canonical.netloc, canonical.path, "", "")),
                       "split": entry["split"], "split_basis": "frozen_ledger_match_at_reconciliation",
                       "source_path": str(source), "source_sha256": row["source_sha256"], "source_locator": copy.deepcopy(locator),
                       "model_id": row.get("model_id", "unknown"), "model_candidates": copy.deepcopy(row.get("model_candidates", [])),
                       "model_basis": {"scope": "discussion_context_only", "normalized_basis": copy.deepcopy(row.get("model_basis")),
                                       "not_infer": "不证明评论者持有、使用该型号，也不证明原片拍摄设备"},
                       "normalization_status": "parsed", "ledger_match": "matched"})
        record.setdefault("limitations", [])
        if not has_text(record):
            add_unique(record["limitations"], "评论文字为空，图片未读取，不提炼文字内容")
        occurrence = {"batch_id": batch_id, "source_path": str(source), "source_sha256": row["source_sha256"],
                      "source_locator": copy.deepcopy(locator), "collected_at": row.get("collected_at"),
                      "normalized_path": str(normalized), "normalized_sha256": normalized_sha, "normalized_line": line}
        candidates[record["id"]].append((line, record, occurrence))

    # Conflicting snapshots are review gaps, never last-row-wins updates.
    accepted = {}
    for identifier, versions in candidates.items():
        signatures = {identity(record) for _, record, _ in versions}
        prior = existing.get(identifier)
        if prior and (prior.get("material_kind", "comment") != "comment" or prior.get("split") != versions[0][1]["split"]):
            signatures.add("existing_record_context_conflict")
        if prior:
            signatures.add(identity(prior))
        if len(signatures) != 1:
            for line, record, _ in versions:
                gap(line, record, "comment_identity_conflict")
        else:
            accepted[identifier] = versions

    graph = {**existing, **{identifier: versions[0][1] for identifier, versions in accepted.items()}}
    invalid_relations = {}
    for identifier, versions in accepted.items():
        record = versions[0][1]
        parent = graph.get(record.get("parent_id"))
        if record.get("thread_role") == "root" and (record.get("parent_id") or record.get("root_id") not in {None, identifier}):
            invalid_relations[identifier] = "root_relationship_conflict"
        elif parent and (parent.get("work_id") != record["work_id"] or parent.get("material_kind", "comment") != "comment"):
            invalid_relations[identifier] = "parent_context_conflict"
        elif parent and (parent.get("root_id") or parent["id"]) != record.get("root_id"):
            invalid_relations[identifier] = "parent_root_conflict"
        seen, cursor = set(), identifier
        while cursor in graph:
            if cursor in seen:
                invalid_relations[identifier] = "parent_cycle"
                break
            seen.add(cursor)
            cursor = graph[cursor].get("parent_id")
    for identifier, reason in invalid_relations.items():
        for line, record, _ in accepted.pop(identifier):
            gap(line, record, reason)

    new_records, new_occurrences, duplicate_rows = 0, 0, 0
    batch_records = defaultdict(list)
    for identifier, versions in accepted.items():
        record = existing.get(identifier)
        if record is None:
            record = copy.deepcopy(versions[0][1])
            record["source_occurrences"] = []
            comments.append(record)
            existing[identifier] = record
            new_records += 1
            duplicate_rows += len(versions) - 1
        else:
            duplicate_rows += len(versions)
            if "source_occurrences" not in record:
                record["source_occurrences"] = [{key: copy.deepcopy(record.get(key)) for key in ("source_path", "source_sha256", "source_locator", "collected_at")}]
        for _, _, occurrence in versions:
            if occurrence not in record["source_occurrences"]:
                record["source_occurrences"].append(occurrence)
                new_occurrences += 1
        batch_records[record["work_id"]].append(record)

    work_results = []
    gap_counts = Counter(g["work_id"] for g in gaps if g.get("work_id") in work_ids)
    accepted_lines = {line for versions in accepted.values() for line, _, _ in versions}
    for wid in work_ids:
        entry, work = ledger_index[wid], work_index[wid]
        rows = batch_records[wid]
        count = metrics(rows)
        if not observed[wid]:
            reason, comment_status = "missing_export", "partial"
        elif not rows or not any(has_text(row) for row in rows):
            reason, comment_status = "no_comment_context", "partial"
        elif gap_counts[wid]:
            reason, comment_status = "comments_partial_review", "partial"
        else:
            reason, comment_status = None, "success"
        post_path = resolve_source(root, work.get("source_path"))
        post_ready = entry.get("postsStatus") == "success" and post_path and post_path.is_file() and bool(work.get("read_scope"))
        if reason is None and not post_ready:
            reason = "comments_only_posts_pending"
        outcome = reason or "success"
        entry["commentsStatus"] = comment_status
        entry["state"] = "success" if outcome == "success" else "partial"
        add_unique(entry.setdefault("comment_reconciled_batch_ids", []), batch_id)
        if wid in export_proof:
            add_unique(entry.setdefault("comment_export_attempt_batch_ids", []), batch_id)
            attempts = entry.setdefault("attempts", {})
            attempts["comments"] = max(int(attempts.get("comments", 0)), 1)
            entry.setdefault("attempt_status", {})["comments"] = "verified_export" if comment_status == "success" else "export_requires_review"
        else:
            entry.setdefault("attempt_status", {})["comments"] = "no_matching_export_evidence"
        work["status"] = outcome
        scope = {"batch_id": batch_id, "normalized_path": str(normalized), "normalized_sha256": normalized_sha,
                 "source_path": str(expected_source) if expected_source else None,
                 "read_scope": "actual_exported_comment_text_and_explicit_relationship_fields_only; no_media_review",
                 "normalized_lines": sorted(line for versions in accepted.values() for line, record, _ in versions if record["work_id"] == wid),
                 "counts": count, "rejected_rows": gap_counts[wid], "status": comment_status}
        add_unique(work.setdefault("comment_sources", []), scope)
        entry["comment_evidence"] = copy.deepcopy(scope)
        work["comment_collection_status"] = comment_status
        work["comment_reconciliation_reason"] = reason
        if rows:
            previous_scope = work.get("read_scope")
            if not isinstance(previous_scope, list):
                previous_scope = [previous_scope] if previous_scope else []
            work["read_scope"] = previous_scope
            add_unique(work["read_scope"], "exported_comment_text_and_explicit_relationship_fields; limited_to_recorded_export")
        work_results.append({"work_id": wid, "input_order": entry.get("inputOrder"), "split": entry["split"],
                             "capture_outcome": outcome, "observed_rows": observed[wid], "rejected_rows": gap_counts[wid], **count})

    # Reuse the existing quota audit, rather than equating collected material with eligibility.
    kb = kb_module()
    data, load_issues = kb.load(root)
    data["works"], data["comments"] = works, comments
    audit = kb.audit(root, data, load_issues)
    if not audit["integrity_ok"]:
        blockers.append("projected_corpus_integrity_errors")
    eligible = set(audit["eligible_work_ids"])
    excluded = {row["work_id"]: row["reason"] for row in audit["excluded_work_details"]}
    for result in work_results:
        result["quota_eligible_projected"] = result["work_id"] in eligible
        result["quota_exclusion_reason"] = excluded.get(result["work_id"])
    groups = {}
    for name, predicate in {
        "all_batch": lambda r: True, "train_only": lambda r: r["split"] == "train",
        "target_eligible_only": lambda r: r["quota_eligible_projected"],
        "train_and_target_eligible": lambda r: r["split"] == "train" and r["quota_eligible_projected"],
    }.items():
        members = [r for r in work_results if predicate(r)]
        groups[name] = {"work_count": len(members), **{key: sum(r[key] for r in members) for key in METRICS}}
    summary = {"mode": "dry_run", "batch_id": batch_id, "batch_state_before": batch.get("status"),
               "text_metrics_version": kb.TEXT_METRICS_VERSION,
               "apply_allowed": not blockers, "apply_blockers": blockers, "batch_work_count": len(work_ids),
               "normalized_rows": len(incoming), "accepted_normalized_rows": len(accepted_lines),
               "new_comment_records": new_records, "duplicate_rows": duplicate_rows, "new_source_occurrences": new_occurrences,
               "rejected_rows": len(gaps), "gap_reason_counts": dict(Counter(g["reason"] for g in gaps)),
               "split_overrides_from_ledger": split_overrides,
               "work_outcome_counts": dict(Counter(r["capture_outcome"] for r in work_results)),
               **groups["all_batch"], "groups": groups, "per_work": work_results,
               "projected_integrity_ok": audit["integrity_ok"],
               "projected_integrity_error_codes": sorted({i["code"] for i in audit["issues"] if i["severity"] == "error"}),
               "limitations": ["UI完成由root维护的批次状态提供，本工具不能自行证明", "success只表示已登记读取范围内的材料完整，不证明配额合格或媒体已读", "父句计数只使用本文件实际可入库的评论行，未知线程角色不算主评", "text_comment_count保留原非空导出口径，与exported_nonempty_text_count相同；文字主评和文字父句回复另按has_textual_content排除已知纯表情/符号，不改变采集成功或原文，也不代表已读取图片", "型号是讨论上下文，不证明评论者持有或使用", "逐帖尝试只由匹配导出佐证，提交次数保持不变"],
               "holdout_text_logged": False}
    batch["status"] = "comments_reconciled" if all(r["capture_outcome"] == "success" for r in work_results) else "comments_reconciled_with_gaps"
    accepted_ids = set(accepted)
    context_gaps = [{"id": record["id"], "work_id": record["work_id"], "parent_id": record.get("parent_id"), "normalized_line": line,
                     "reason": "missing_direct_parent_in_analyzable_export" if record.get("thread_role") == "reply" else "thread_role_unknown"}
                    for versions in accepted.values() for line, record, _ in versions
                    if (record.get("thread_role") == "reply" and record.get("parent_id") not in accepted_ids) or record.get("thread_role") == "unknown"]
    batch["reconciliation"] = {"normalized_path": str(normalized), "normalized_sha256": normalized_sha, "text_metrics_version": kb.TEXT_METRICS_VERSION,
                               "work_results": work_results, "row_gaps": gaps, "counts": {key: summary[key] for key in ("normalized_rows", "accepted_normalized_rows", "new_comment_records", "duplicate_rows", "rejected_rows")},
                               "context_gaps": context_gaps, "groups": groups, "collection_success_is_quota_success": False}
    successful = {r["work_id"] for r in work_results if r["capture_outcome"] == "success"}
    for key, additions in (("completedWorkIds", successful), ("pendingWorkIds", set(work_ids) - successful), ("failedWorkIds", set())):
        previous = state.get(key, [])
        state[key] = [wid for wid in previous if wid not in work_ids] + [wid for wid in work_ids if wid in additions]
    if state.get("activeBatch") == batch_id:
        state["activeBatch"] = None
    outputs = {paths["comments.jsonl"]: encoded(comments, True), paths["works.jsonl"]: encoded(works, True),
               paths["input-ledger.jsonl"]: encoded(ledger, True), paths["run-state.json"]: encoded(state)}
    return {"root": root, "snapshots": snapshots, "outputs": outputs, "summary": summary, "state": state, "state_path": paths["run-state.json"], "batch": batch}


def attach_report(plan, path):
    path = Path(path).resolve()
    if path in plan["snapshots"] or path in plan["outputs"]:
        raise ReconcileError("Report cannot overwrite an input or destination table")
    if not path.parent.is_dir():
        raise ReconcileError("Report parent directory must already exist")
    plan["snapshots"][path] = path.read_bytes() if path.is_file() else None
    plan["report_path"] = path
    plan["summary"]["reconciliation_report_path"] = str(path)
    plan["batch"]["reconciliation_path"] = str(path)


def apply_plan(plan):
    if not plan["summary"]["apply_allowed"]:
        raise ReconcileError("Apply refused: " + ", ".join(plan["summary"]["apply_blockers"]))
    lock = plan["root"] / "corpus" / ".comment-reconciliation.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ReconcileError("Another reconciliation lock exists; no files changed") from exc
    os.close(descriptor)
    temporary, replaced = {}, []
    try:
        for path, before in plan["snapshots"].items():
            current = path.read_bytes() if path.is_file() else None
            if current != before:
                raise ReconcileError(f"Input changed after dry-run planning: {path.name}; replan before apply")
        plan["batch"]["reconciliation"]["applied_at"] = datetime.now(timezone.utc).isoformat()
        plan["outputs"][plan["state_path"]] = encoded(plan["state"])
        if plan.get("report_path"):
            saved_report = copy.deepcopy(plan["summary"])
            saved_report["mode"] = "applied"
            saved_report["applied_at"] = plan["batch"]["reconciliation"]["applied_at"]
            plan["outputs"][plan["report_path"]] = encoded(saved_report)
        for path, content in plan["outputs"].items():
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".reconcile-", delete=False) as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
                temporary[path] = Path(stream.name)
        try:
            for path, temp in temporary.items():
                os.replace(temp, path)
                replaced.append(path)
        except OSError:
            for path in reversed(replaced):
                before = plan["snapshots"][path]
                if before is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(before)
            raise
    finally:
        for temp in temporary.values():
            temp.unlink(missing_ok=True)
        lock.unlink(missing_ok=True)
    result = copy.deepcopy(plan["summary"])
    result["mode"] = "applied"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Pocket knowledge root; defaults to this script's library")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--normalized", required=True, type=Path)
    parser.add_argument("--report", type=Path, help="Optional aggregate metadata report; written only with --apply")
    parser.add_argument("--apply", action="store_true", help="Write only a root-confirmed exported batch; default is read-only")
    args = parser.parse_args(argv)
    try:
        plan = prepare(args.root, args.batch_id, args.normalized)
        if args.report:
            attach_report(plan, args.report)
        result = apply_plan(plan) if args.apply else plan["summary"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ReconcileError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"mode": "error", "error": str(exc), "holdout_text_logged": False}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
