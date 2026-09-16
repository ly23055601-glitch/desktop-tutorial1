#!/usr/bin/env python3
"""Aggregate CW5 quality reviews without changing the daily KPI ledger.

The collector deliberately accepts a small, versioned ``quality-review.json``
record rather than reading drafts or the existing ledger.  This keeps the
quality layer additive: a review can be re-run for a new draft version while
the original review remains an immutable input to an earlier summary.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Iterable


PROFILE = "training_cw5"
COVERAGES = ("basic", "deep", "risk_deep")
DECISIONS = ("retain", "revise", "block")
DIMENSIONS = ("quality_base", "expression", "teaching", "total")
ISSUE_CODES = (
    "fact_boundary", "model_mismatch", "post_misread", "evidence_insufficient",
    "weak_product_interest", "reply_parent_mismatch", "weak_discussion",
    "repetition", "template_cluster", "marketing_tone", "ai_style",
    "unsupported_question", "platform_voice", "comparison_overclaim",
)
SEVERITIES = ("blocker", "major", "minor", "info")
MISSING = "unknown"


def _first(record: dict[str, Any], *keys: str, default: str = MISSING) -> str:
    """Read a non-empty string from a record, including its metadata object."""
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    task = record.get("task") if isinstance(record.get("task"), dict) else {}
    for key in keys:
        for source in (record, metadata, task):
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return default


def _number(value: Any, default: float | int | None = None) -> float | int | None:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return value
    return default


def _ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": numerator / denominator if denominator else None,
    }


def _average(values: Iterable[float | int]) -> float | None:
    values = list(values)
    return sum(values) / len(values) if values else None


def normalize_review(record: dict[str, Any], source: str = "<memory>") -> dict[str, Any]:
    """Normalize one quality-review object for aggregation.

    Unknown optional dimensions are retained as ``None``.  Missing identity
    fields are grouped under ``unknown`` so one incomplete review never makes
    the rest of a batch disappear.
    """
    if not isinstance(record, dict):
        raise ValueError(f"{source}: review must be a JSON object")
    profile = _first(record, "profile", "quality_profile", default="")
    if profile != PROFILE:
        raise ValueError(f"{source}: unsupported profile {profile!r}; expected {PROFILE!r}")
    coverage = _first(record, "coverage", "review_coverage", default="")
    if coverage not in COVERAGES:
        raise ValueError(f"{source}: coverage must be one of {', '.join(COVERAGES)}")
    decision = _first(record, "decision", "verdict", default="")
    # Human-readable independent-review verdicts are accepted as aliases.
    decision = {"retained": "retain", "retain_author_draft": "retain", "preserve_all": "retain", "revise_after_review": "revise", "blocked": "block"}.get(decision, decision)
    if decision not in DECISIONS:
        raise ValueError(f"{source}: decision must be one of {', '.join(DECISIONS)}")

    dimensions = record.get("dimensions") if isinstance(record.get("dimensions"), dict) else {}
    values: dict[str, float | int | None] = {}
    for key in DIMENSIONS:
        value = _number(dimensions.get(key), _number(record.get(key)))
        if value is not None and value < 0:
            raise ValueError(f"{source}: dimension {key!r} cannot be negative")
        values[key] = value
    if values["total"] is None:
        known = [values[key] for key in DIMENSIONS[:3] if values[key] is not None]
        values["total"] = sum(known) if len(known) == 3 else None

    raw_issues = record.get("issues", [])
    if raw_issues is None:
        raw_issues = []
    if not isinstance(raw_issues, list):
        raise ValueError(f"{source}: issues must be an array")
    issues = []
    for number, issue in enumerate(raw_issues, 1):
        if not isinstance(issue, dict):
            raise ValueError(f"{source}: issues[{number}] must be an object")
        code = issue.get("code")
        if not isinstance(code, str) or not code.strip():
            raise ValueError(f"{source}: issues[{number}] missing code")
        if code not in ISSUE_CODES:
            raise ValueError(f"{source}: issues[{number}] has invalid code {code!r}")
        severity = issue.get("severity", "minor")
        if severity not in SEVERITIES:
            raise ValueError(f"{source}: issues[{number}] has invalid severity {severity!r}")
        issues.append({"code": code.strip(), "severity": severity})

    revision_count = _number(record.get("revision_count"), _number((record.get("revision") or {}).get("count") if isinstance(record.get("revision"), dict) else None, 0))
    if not isinstance(revision_count, int) or revision_count < 0:
        raise ValueError(f"{source}: revision_count must be a non-negative integer")
    score = _number(record.get("quality_score"), values["total"])
    if score is not None and score < 0:
        raise ValueError(f"{source}: quality_score cannot be negative")
    task_ref = _first(record, "task_ref", "task", default=MISSING)
    batch_ref = _first(record, "batch_ref", "batch", default=MISSING)
    # Core CW5 artifacts use the compact ``B001/T053`` task reference and do
    # not repeat batch_ref.  Derive that parent identity without guessing from
    # a filesystem path; date-prefixed refs naturally retain their date.
    if batch_ref == MISSING and task_ref != MISSING and "/" in task_ref:
        batch_ref = task_ref.rsplit("/", 1)[0]
    return {
        "source": source,
        "task_ref": task_ref,
        "batch_ref": batch_ref,
        "writer": _first(record, "writer", "writer_id", "writer_ref", "author", default=MISSING),
        "product": _first(record, "product", "product_line", "product_code", default=MISSING),
        "platform": _first(record, "platform", "channel", default=MISSING),
        "coverage": coverage,
        "decision": decision,
        "dimensions": values,
        "score": score,
        "issues": issues,
        "revision_count": revision_count,
        "teaching_complete": record.get("teaching_complete") is True,
        "user_acceptance": _first(record, "user_acceptance", default="pending"),
        "draft_sha256": _first(record, "draft_sha256", default=""),
    }


def _group(records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    """Build a stable group profile used by writer/product/platform/batch."""
    count = len(records)
    decisions = {item: sum(row["decision"] == item for row in records) for item in DECISIONS}
    coverages = {item: sum(row["coverage"] == item for row in records) for item in COVERAGES}
    dimensions = {
        item: _average(row["dimensions"][item] for row in records if row["dimensions"][item] is not None)
        for item in DIMENSIONS
    }
    issue_codes = Counter(issue["code"] for row in records for issue in row["issues"])
    severity_counts = Counter(issue["severity"] for row in records for issue in row["issues"])
    return {
        "count": count,
        "decision_counts": decisions,
        "coverage_counts": coverages,
        "deep_review_coverage": _ratio(sum(row["coverage"] in {"deep", "risk_deep"} for row in records), count),
        "teaching_complete": _ratio(sum(row["teaching_complete"] for row in records), count),
        "user_acceptance_counts": dict(sorted(Counter(row["user_acceptance"] for row in records).items())),
        "average_score": _average(row["score"] for row in records if row["score"] is not None),
        "average_dimensions": dimensions,
        "issue_count": sum(len(row["issues"]) for row in records),
        "issue_codes": dict(sorted(issue_codes.items())),
        "severity_counts": dict(sorted(severity_counts.items())),
        "revision_count": {
            "total": sum(row["revision_count"] for row in records),
            "average": _average(row["revision_count"] for row in records),
            "with_revisions": sum(row["revision_count"] > 0 for row in records),
        },
    }


def summarize(records: Iterable[dict[str, Any]], *, sources: list[str] | None = None) -> dict[str, Any]:
    """Return a batch summary and writer profile from review records."""
    def already_normalized(row: dict[str, Any]) -> bool:
        return (
            isinstance(row, dict) and isinstance(row.get("source"), str)
            and isinstance(row.get("task_ref"), str) and isinstance(row.get("dimensions"), dict)
            and isinstance(row.get("issues"), list)
            and all(isinstance(issue, dict) and isinstance(issue.get("code"), str) and issue.get("severity") in SEVERITIES for issue in row["issues"])
        )
    normalized = [row if already_normalized(row) else normalize_review(row, f"record[{index}]") for index, row in enumerate(records, 1)]
    def keyed(field: str) -> dict[str, Any]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in normalized:
            grouped.setdefault(row[field], []).append(row)
        return {name: _group(grouped[name], field) for name in sorted(grouped)}

    issue_codes = Counter(issue["code"] for row in normalized for issue in row["issues"])
    severity_counts = Counter(issue["severity"] for row in normalized for issue in row["issues"])
    summary = {
        "schema_version": 1,
        "quality_profile": PROFILE,
        "input_count": len(normalized),
        "sources": sources or [],
        "coverage": {
            "basic": sum(row["coverage"] == "basic" for row in normalized),
            "deep": sum(row["coverage"] == "deep" for row in normalized),
            "risk_deep": sum(row["coverage"] == "risk_deep" for row in normalized),
            "deep_review_coverage": _ratio(sum(row["coverage"] in {"deep", "risk_deep"} for row in normalized), len(normalized)),
        },
        "totals": _group(normalized, "all") if normalized else _group([], "all"),
        "by_writer": keyed("writer"),
        "by_product": keyed("product"),
        "by_platform": keyed("platform"),
        "by_batch": keyed("batch_ref"),
        "issue_codes": dict(sorted(issue_codes.items())),
        "severity_counts": dict(sorted(severity_counts.items())),
        "records": [
            {
                "task_ref": row["task_ref"], "batch_ref": row["batch_ref"],
                "writer": row["writer"], "product": row["product"], "platform": row["platform"],
                "coverage": row["coverage"], "decision": row["decision"], "score": row["score"],
                "revision_count": row["revision_count"], "issue_codes": [issue["code"] for issue in row["issues"]],
            }
            for row in normalized
        ],
    }
    return summary


def _json_files(inputs: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(path.rglob("quality-review.json")))
            paths.extend(sorted(path.rglob("*.quality-review.json")))
        elif path.is_file():
            paths.append(path)
        else:
            raise ValueError(f"input does not exist: {raw}")
    return list(dict.fromkeys(paths))


def load_inputs(inputs: Iterable[str]) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    sources: list[str] = []
    for path in _json_files(inputs):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"{path}: cannot read JSON: {exc}") from exc
        candidates = payload if isinstance(payload, list) else [payload]
        for index, candidate in enumerate(candidates, 1):
            if not isinstance(candidate, dict):
                raise ValueError(f"{path}[{index}]: review must be an object")
            normalized = normalize_review(candidate, f"{path}[{index}]")
            records.append(normalized)
            sources.append(str(path))
    return records, sources


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate training_cw5 quality-review.json files")
    parser.add_argument("inputs", nargs="+", help="quality-review JSON files or directories")
    parser.add_argument("--output", "-o", type=Path, help="write JSON summary to a file; stdout by default")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    args = parser.parse_args(argv)
    try:
        records, sources = load_inputs(args.inputs)
        report = summarize(records, sources=sources)
    except ValueError as exc:
        print(f"quality-summary: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
