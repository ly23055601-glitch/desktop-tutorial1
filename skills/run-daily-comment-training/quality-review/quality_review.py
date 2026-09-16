#!/usr/bin/env python3
"""Validate and score a ``training_cw5`` writing quality review.

This module deliberately does not read or mutate a training ledger.  A review is
an independent, versioned artifact which can be referenced by an existing
ledger.  Product-specific fact checks remain upstream; this tool checks the
review contract and applies the common scoring/decision rules.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping


PROFILE = "training_cw5"
COVERAGES = {"basic", "deep", "risk_deep"}
DECISIONS = {"retain", "revise", "block"}
USER_ACCEPTANCE = {"pending", "accepted", "changes_requested"}
RECHECK_STATES = {"pending", "passed", "failed"}
SEVERITIES = {"blocker", "major", "minor", "info"}

# Keep this list stable: issue codes are used for longitudinal writer reports.
ISSUE_CODES = {
    "fact_boundary",
    "model_mismatch",
    "post_misread",
    "evidence_insufficient",
    "weak_product_interest",
    "reply_parent_mismatch",
    "weak_discussion",
    "repetition",
    "template_cluster",
    "marketing_tone",
    "ai_style",
    "unsupported_question",
    "platform_voice",
    "comparison_overclaim",
}

DIMENSION_LIMITS = {"quality_base": 60, "expression": 25, "teaching": 15}


class ReviewError(ValueError):
    """Raised for an invalid quality-review artifact."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewError(message)


def _text(value: Any, field: str, *, required: bool = True) -> str:
    if not isinstance(value, str):
        raise ReviewError(f"{field} 必须是字符串")
    if required and not value.strip():
        raise ReviewError(f"{field} 不能为空")
    return value


def _score(value: Any, field: str, maximum: int) -> int:
    # bool is an int subclass but is not a valid score.
    _require(type(value) is int, f"{field} 必须是整数")
    _require(0 <= value <= maximum, f"{field} 必须在 0–{maximum} 之间")
    return value


def validate_review(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a review and return a detached, JSON-safe copy.

    ``decision`` and the total score are derived by :func:`score_review`, so
    callers may omit them in a draft input.  When present, decision is checked
    against the derived value to prevent stale review artifacts.
    """

    _require(isinstance(payload, Mapping), "质检内容必须是 JSON 对象")
    data = dict(payload)
    _text(data.get("task_ref"), "task_ref")
    _text(data.get("draft_ref"), "draft_ref")
    digest = _text(data.get("draft_sha256"), "draft_sha256")
    _require(len(digest) == 64 and all(c in "0123456789abcdefABCDEF" for c in digest), "draft_sha256 必须是 64 位十六进制哈希")
    _require(data.get("profile") == PROFILE, f"profile 必须为 {PROFILE}")
    _require(data.get("coverage") in COVERAGES, "coverage 必须为 basic、deep 或 risk_deep")
    # Reviewer metadata is optional for a draft, but if supplied it must remain
    # explicit so automated and independent passes cannot be conflated.
    for field in ("reviewer", "reviewed_at"):
        if field in data and data[field] is not None:
            _text(data[field], field)

    dimensions = data.get("dimensions")
    _require(isinstance(dimensions, Mapping), "dimensions 必须是对象")
    clean_dimensions: dict[str, int] = {}
    for name, maximum in DIMENSION_LIMITS.items():
        clean_dimensions[name] = _score(dimensions.get(name), f"dimensions.{name}", maximum)
    data["dimensions"] = clean_dimensions

    issues = data.get("issues", [])
    _require(isinstance(issues, list), "issues 必须是数组")
    seen: set[str] = set()
    clean_issues = []
    for index, issue in enumerate(issues, 1):
        _require(isinstance(issue, Mapping), f"issues[{index}] 必须是对象")
        issue = dict(issue)
        issue_id = _text(issue.get("issue_id"), f"issues[{index}].issue_id")
        _require(issue_id not in seen, f"问题 ID 重复：{issue_id}")
        seen.add(issue_id)
        code = issue.get("code")
        _require(code in ISSUE_CODES, f"问题码无效：{code}")
        severity = issue.get("severity")
        _require(severity in SEVERITIES, f"严重度无效：{severity}")
        _text(issue.get("observation"), f"issues[{index}].observation")
        _text(issue.get("action"), f"issues[{index}].action")
        evidence_refs = issue.get("evidence_refs", [])
        _require(isinstance(evidence_refs, list) and all(isinstance(x, str) and x.strip() for x in evidence_refs), f"issues[{index}].evidence_refs 必须是字符串数组")
        recheck = issue.get("recheck_status", "pending")
        _require(recheck in RECHECK_STATES, f"复检状态无效：{recheck}")
        location = issue.get("location")
        if location is not None:
            _require(isinstance(location, Mapping), f"issues[{index}].location 必须是对象")
        if "rewrite" in issue and issue["rewrite"] is not None:
            _text(issue["rewrite"], f"issues[{index}].rewrite", required=False)
        issue["issue_id"] = issue_id
        issue["evidence_refs"] = list(evidence_refs)
        issue["recheck_status"] = recheck
        clean_issues.append(issue)
    data["issues"] = clean_issues

    teaching_complete = data.get("teaching_complete", True)
    _require(type(teaching_complete) is bool, "teaching_complete 必须是布尔值")
    data["teaching_complete"] = teaching_complete
    acceptance = data.get("user_acceptance", "pending")
    _require(acceptance in USER_ACCEPTANCE, "user_acceptance 无效")
    data["user_acceptance"] = acceptance
    if "decision" in data:
        _require(data["decision"] in DECISIONS, "decision 无效")
    return data


def score_review(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a validated review with derived score, decision and diagnostics."""

    data = validate_review(payload)
    dimensions = data["dimensions"]
    raw_total = sum(dimensions.values())
    severities = Counter(issue["severity"] for issue in data["issues"])
    caps: list[dict[str, Any]] = []
    total = raw_total
    if severities["blocker"]:
        total = min(total, 59)
        caps.append({"reason": "blocker", "cap": 59})
    elif severities["major"]:
        total = min(total, 79)
        caps.append({"reason": "major", "cap": 79})

    if severities["blocker"]:
        decision = "block"
    elif total < 90 or not data["teaching_complete"]:
        decision = "revise"
    else:
        decision = "retain"
    if "decision" in payload and payload["decision"] != decision:
        raise ReviewError(f"decision 与规则不一致：输入 {payload['decision']}，应为 {decision}")
    data["dimensions"] = {**dimensions, "total": total}
    data["score"] = {"raw_total": raw_total, "total": total, "caps": caps}
    data["quality_score"] = total
    data["quality_issue_codes"] = sorted({issue["code"] for issue in data["issues"]})
    data["decision"] = decision
    data["severity_counts"] = {key: severities.get(key, 0) for key in sorted(SEVERITIES)}
    data["quality_profile"] = PROFILE
    return data


def format_markdown(review: Mapping[str, Any]) -> str:
    """Render a compact human-readable report."""

    dimensions = review["dimensions"]
    score = review["score"]
    lines = [
        "# 文案质检报告",
        "",
        f"- 任务：`{review['task_ref']}`",
        f"- 稿件：`{review['draft_ref']}`",
        f"- 质检档位：`{review['coverage']}`",
        f"- 结论：**{review['decision']}**",
        f"- 得分：**{score['total']}/100**（原始 {score['raw_total']}）",
        "",
        "## 维度得分",
        "",
        f"- 基础：{dimensions['quality_base']}/60",
        f"- 表达：{dimensions['expression']}/25",
        f"- 教学：{dimensions['teaching']}/15",
    ]
    if score["caps"]:
        lines.extend(["", "封顶：" + "、".join(f"{item['reason']} ≤ {item['cap']}" for item in score["caps"])])
    lines.extend(["", "## 问题", ""])
    issues = review.get("issues", [])
    if not issues:
        lines.append("未记录问题。")
    else:
        for issue in issues:
            lines.append(f"- **{issue['issue_id']}** `{issue['severity']}` `{issue['code']}`：{issue['observation']}；处理：{issue['action']}")
    lines.extend(["", f"教学完整：`{str(review['teaching_complete']).lower()}`；用户验收：`{review['user_acceptance']}`", ""])
    return "\n".join(lines)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and score a training_cw5 quality review JSON")
    parser.add_argument("review", type=Path, help="quality-review JSON")
    parser.add_argument("--output-json", type=Path, help="write scored JSON to this path")
    parser.add_argument("--output-md", type=Path, help="write Markdown report to this path")
    parser.add_argument("--draft", type=Path, help="optional draft file whose SHA256 must match draft_sha256")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.review.read_text(encoding="utf-8"))
        if args.draft:
            expected = payload.get("draft_sha256")
            actual = _sha256(args.draft)
            if expected != actual:
                raise ReviewError(f"draft_sha256 不匹配：声明 {expected}，实际 {actual}")
        result = score_review(payload)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output_json:
            args.output_json.parent.mkdir(parents=True, exist_ok=True)
            args.output_json.write_text(encoded, encoding="utf-8")
        if args.output_md:
            args.output_md.parent.mkdir(parents=True, exist_ok=True)
            args.output_md.write_text(format_markdown(result), encoding="utf-8")
        if not args.output_json and not args.output_md:
            sys.stdout.write(encoded)
        return 0
    except (OSError, json.JSONDecodeError, ReviewError, TypeError) as exc:
        print(f"quality-review: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
