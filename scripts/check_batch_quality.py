#!/usr/bin/env python3
"""Run the machine portion of the controller's final batch review.

The checker deliberately reports candidates for human semantic review instead of
claiming that a similarity score proves that two comments are duplicates.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalise(text: str) -> str:
    text = re.sub(r"\s+", "", text).lower()
    return re.sub(r"[，。！？、；：,.!?;:'\"“”‘’()（）\[\]【】]", "", text)


def comments_from_markdown(text: str) -> list[tuple[str, str]]:
    """Return visible numbered comments and indented replies from a draft."""
    records: list[tuple[str, str]] = []
    current_main = 0
    reply_index = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        main = re.match(r"^(\d+)\.\s+(.+)$", line)
        reply = re.match(r"^-\s+(.+)$", line)
        if main:
            current_main = int(main.group(1))
            reply_index = 0
            records.append((str(current_main), main.group(2).strip()))
        elif reply and current_main:
            reply_index += 1
            records.append((f"{current_main}.{reply_index}", reply.group(1).strip()))
    return records


def task_value(task: dict[str, Any], *names: str) -> Any:
    for name in names:
        if task.get(name) not in (None, ""):
            return task[name]
    return None


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path, help="batch.json created from examples/batch.template.json")
    parser.add_argument("--output", type=Path, help="write the JSON report to this path")
    args = parser.parse_args()

    batch_path = args.batch.resolve()
    try:
        batch = load_json(batch_path)
    except Exception as exc:  # pragma: no cover - command-line diagnostic
        print(f"cannot read batch JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(batch, dict):
        print("batch JSON must be an object", file=sys.stderr)
        return 2

    errors: list[str] = []
    tasks = batch.get("tasks", [])
    if not isinstance(tasks, list):
        errors.append("tasks must be an array")
        tasks = []
    records: list[dict[str, Any]] = []
    task_reports: list[dict[str, Any]] = []
    for index, raw_task in enumerate(tasks, 1):
        if not isinstance(raw_task, dict):
            errors.append(f"tasks[{index}] must be an object")
            continue
        task_id = str(task_value(raw_task, "link_id", "id", "task_id", "material_id") or f"task-{index}")
        draft_ref = task_value(raw_task, "draft_path", "draft_ref", "draft")
        state_ref = task_value(raw_task, "state_path", "training_state_ref", "state_ref", "training_state")
        report: dict[str, Any] = {"link_id": task_id, "draft": None, "state": None, "comments": 0}
        if not draft_ref:
            errors.append(f"{task_id}: missing draft_path")
        else:
            draft_path = (batch_path.parent / str(draft_ref)).resolve()
            if not draft_path.is_file():
                errors.append(f"{task_id}: draft not found: {draft_ref}")
            else:
                try:
                    draft_text = draft_path.read_text(encoding="utf-8-sig")
                    comments = comments_from_markdown(draft_text)
                    report["draft"] = {"path": str(draft_ref), "sha256": fingerprint(draft_path)}
                    report["comments"] = len(comments)
                    records.extend({"link_id": task_id, "comment_id": cid, "text": text} for cid, text in comments)
                except Exception as exc:
                    errors.append(f"{task_id}: cannot read draft: {exc}")
        if not state_ref:
            errors.append(f"{task_id}: missing state_path")
        else:
            state_path = (batch_path.parent / str(state_ref)).resolve()
            if not state_path.is_file():
                errors.append(f"{task_id}: state not found: {state_ref}")
            else:
                try:
                    state = load_json(state_path)
                    if not isinstance(state, dict):
                        errors.append(f"{task_id}: state must be an object")
                    report["state"] = {"path": str(state_ref), "sha256": fingerprint(state_path)}
                except Exception as exc:
                    errors.append(f"{task_id}: cannot read state: {exc}")
        task_reports.append(report)

    duplicate_candidates: list[dict[str, Any]] = []
    for i, left in enumerate(records):
        left_norm = normalise(left["text"])
        if not left_norm:
            continue
        for right in records[i + 1 :]:
            right_norm = normalise(right["text"])
            if not right_norm:
                continue
            ratio = difflib.SequenceMatcher(None, left_norm, right_norm).ratio()
            if left_norm == right_norm or ratio >= 0.84:
                duplicate_candidates.append(
                    {
                        "left": {k: left[k] for k in ("link_id", "comment_id")},
                        "right": {k: right[k] for k in ("link_id", "comment_id")},
                        "similarity": round(ratio, 4),
                        "reason": "exact_normalized_text" if left_norm == right_norm else "near_text_similarity",
                        "decision": None,
                    }
                )

    semantic = batch.get("semantic_review") or batch.get("quality", {}).get("semantic_review")
    if semantic is None:
        semantic = {"status": "pending", "reviewed_fingerprints": [], "candidate_decisions": []}
    if not isinstance(semantic, dict):
        errors.append("semantic_review must be an object")
        semantic = {"status": "pending"}
    decisions = semantic.get("candidate_decisions", [])
    reviewed = set(semantic.get("reviewed_fingerprints", []) or [])
    fingerprints = [f"{c['left']['link_id']}:{c['left']['comment_id']}|{c['right']['link_id']}:{c['right']['comment_id']}" for c in duplicate_candidates]
    recorded_review = semantic.get("status") in {"complete", "passed"} and all(fp in reviewed for fp in fingerprints)

    report = {
        "schema_version": 1,
        "batch_id": batch.get("batch_id"),
        "machine": {
            "status": "error" if errors else "ok",
            "errors": errors,
            "task_count": len(tasks),
            "comment_count": len(records),
            "duplicate_candidate_count": len(duplicate_candidates),
        },
        "tasks": task_reports,
        "duplicate_candidates": duplicate_candidates,
        "semantic_review": semantic,
        "passed_recorded_review": bool(not errors and recorded_review),
        "notes": ["Similarity candidates require contextual human review; this report does not prove a semantic duplicate."],
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
