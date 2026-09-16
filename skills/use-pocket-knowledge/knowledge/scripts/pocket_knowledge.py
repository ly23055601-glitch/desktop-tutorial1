#!/usr/bin/env python3
"""Read-only Pocket knowledge retrieval and provenance/coverage audit (stdlib)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import parse_qs, urlsplit

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MODELS = {"pocket_1", "pocket_2", "pocket_3", "pocket_4", "pocket_4p", "unknown"}
PLATFORMS = {"douyin", "xiaohongshu", "bilibili"}
PRIMARY_MODELS = {"pocket_4", "pocket_4p"}
MODEL_TARGETS = {"pocket_4": 75, "pocket_4p": 75}
TABLES = {"sources": "sources/official.jsonl", "facts": "products/facts.jsonl",
          "voice": "voice/cards.jsonl", "records": "voice/records.jsonl",
          "scenarios": "scenarios/cards.jsonl", "works": "corpus/works.jsonl",
    "comments": "corpus/comments.jsonl", "comparisons": "comparisons/cards.jsonl"}
REQUIRED = {"sources", "facts", "voice", "records", "scenarios", "works"}
TEXT_METRICS_VERSION = "textual-content-v1"

# Explicit platform placeholders seen in the C1 training export, plus the
# requested [赞R]/[doge] examples. Unknown bracketed text is kept conservatively;
# neither a trailing R nor brackets alone prove that text is an emoji token.
KNOWN_EMOTE_PLACEHOLDERS = frozenset(token.casefold() for token in (
    "赞R", "大笑R", "失望R", "笑哭R", "捂脸R", "害羞R", "石化R", "萌萌哒R",
    "派对R", "拔草R", "自拍R", "飞吻R", "偷笑R", "暗中观察R", "皱眉R", "色色R",
    "哭惹R", "点赞R", "买爆R", "呃R", "doge", "得意R", "哇R", "黑薯问号R", "红色心形R",
))


def has_textual_content(value):
    """Conservative discussion-count check, never a source/admission check.

    Remove only reviewed emote placeholders and Unicode keycap sequences, then
    require a Unicode letter or number. Single characters, numbers and mixed
    text remain. This does not read an image or infer an emoji's visual content.
    """
    if not isinstance(value, str):
        return False
    residual = re.sub(r"\[([^\[\]\n]+)\]", lambda match: "" if match[1].casefold() in KNOWN_EMOTE_PLACEHOLDERS else match[0], value)
    residual = re.sub(r"[#*0-9]\ufe0f?\u20e3", "", residual)
    return any(unicodedata.category(character)[0] in {"L", "N"} for character in residual)


def model_id(value):
    raw = str(value or "unknown").lower().strip()
    if raw in MODELS:
        return raw
    if raw in {"初代", "一代", "pocket初代", "pocket一代"}:
        return "pocket_1"
    raw = re.sub(r"[\s_-]", "", raw)
    raw = re.sub(r"^(?:大疆|dji)", "", raw)
    raw = re.sub(r"^(?:osmo)?pocket|^op|^p(?=[1-4])", "", raw)
    return {"1": "pocket_1", "2": "pocket_2", "3": "pocket_3", "4": "pocket_4", "4p": "pocket_4p"}.get(raw, "unknown")


def sampling_order(pair):
    identifier, work = pair
    value = work.get("input_order", work.get("inputOrder"))
    try:
        order = int(value)
    except (TypeError, ValueError):
        order = float("inf")
    return order, identifier


def load(root):
    data, issues = {}, []
    for table, relative in TABLES.items():
        path = root / relative
        data[table] = []
        if not path.is_file():
            if table in REQUIRED:
                issues.append({"severity": "warning", "code": "missing_table", "at": relative})
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ValueError("JSONL record must be an object")
                data[table].append(item)
            except (json.JSONDecodeError, ValueError) as exc:
                issues.append({"severity": "error", "code": "invalid_jsonl", "at": f"{relative}:{number}", "detail": str(exc)})
    return data, issues


def index(items, key="id"):
    return {item.get(key): item for item in items if item.get(key)}


@lru_cache(maxsize=8)
def _read_package_map(path, mtime_ns, size):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def package_map(root):
    path = root / "package-map.json"
    if not path.is_file():
        return None
    stat = path.stat()
    return _read_package_map(str(path.resolve()), stat.st_mtime_ns, stat.st_size)


def source_path(root, value):
    """Resolve archived provenance through a bundle map without changing raw bytes."""
    if not isinstance(value, str) or not value.strip():
        return None
    bundle = package_map(root)
    if bundle is not None:
        relative = bundle.get("aliases", {}).get(value, value)
        path = Path(relative)
        if path.is_absolute():
            return None
        resolved = (root / path).resolve()
        # A packaged source never falls back to the original project or cwd.
        return resolved if resolved.is_relative_to(root.resolve()) else None
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    local = root / path
    if local.exists():
        return local
    project = root.parent.parent / path
    return project if project.exists() else local


def valid_date(value):
    try:
        return date.fromisoformat(value) <= date.today()
    except (TypeError, ValueError):
        return False


def official_url(value):
    try:
        parsed = urlsplit(value)
        host = parsed.hostname or ""
        return parsed.scheme == "https" and (host == "dji.com" or host.endswith(".dji.com") or host == "dl.djicdn.com") and not parsed.username
    except (TypeError, ValueError):
        return False


def source_identity(value):
    if not official_url(value):
        return ""
    parsed = urlsplit(value)
    key = parsed.hostname + parsed.path.rstrip("/").lower()
    if parsed.hostname == "repair.dji.com":
        key += "?customId=" + ",".join(parse_qs(parsed.query).get("customId", []))
    return key


def evidence_ids(card):
    return [ref if isinstance(ref, str) else ref.get("record_id", ref.get("id"))
            for ref in card.get("evidence_refs", []) if isinstance(ref, (str, dict))]


def get_registry(root):
    bundle = package_map(root)
    path = (source_path(root, bundle.get("claim_registry")) if bundle is not None else
            root.parent.parent / ".agents/skills/write-pocket-seeding-comments/references/product-claims.json")
    if path is None:
        return {}
    if not path.is_file():
        return {}
    registry = json.loads(path.read_text(encoding="utf-8"))
    return {**registry.get("claims", {}), **registry.get("lh13", {}).get("claims", {})}


def get_project_scope(root):
    path = root / "corpus/collection-plan.json"
    fallback = {"profile": "historical_150", "status": "sampling_plan", "scale_target_status": "active"}
    if not path.is_file():
        return fallback
    plan = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict):
        raise ValueError("collection-plan must be an object")
    scope = plan.get("current_scope", fallback)
    if not isinstance(scope, dict) or scope.get("profile") not in {"current_library", "historical_150"}:
        raise ValueError("collection-plan.current_scope requires a known profile")
    return {**scope, "source_path": str(path)}


def audit(root, data, initial_issues=()):
    issues = list(initial_issues)
    def issue(severity, code, at, **details):
        issues.append({"severity": severity, "code": code, "at": at, **details})
    try:
        project_scope = get_project_scope(root)
    except (OSError, ValueError, TypeError) as exc:
        issue("error", "project_scope_invalid", "corpus/collection-plan.json", detail=str(exc))
        project_scope = {"profile": "unknown", "status": "invalid", "scale_target_status": "unknown"}
    for table, items in data.items():
        key = "source_id" if table == "sources" else "work_id" if table == "works" else "id"
        counts = Counter(item.get(key) for item in items)
        for identifier, count in counts.items():
            if not identifier or count > 1:
                issue("error", "missing_or_duplicate_id", table, id=identifier, count=count)
    sources, facts = index(data["sources"], "source_id"), index(data["facts"])
    works = index(data["works"], "work_id")
    records = index(data["records"] + data["comments"])
    for identifier, count in Counter(r.get("id") for r in data["records"] + data["comments"]).items():
        if identifier and count > 1:
            issue("error", "duplicate_comment_across_tables", identifier)
    voices = index(data["voice"])
    registry = get_registry(root)
    for identifier, src in sources.items():
        if not official_url(src.get("url")):
            issue("error", "not_official_https", identifier)
        if not valid_date(src.get("checked_at")):
            issue("error", "invalid_checked_date", identifier)
        for field in ("title", "excerpt", "locator", "read_scope"):
            if not src.get(field):
                issue("error", "source_context_missing", identifier, field=field)
    for identifier, fact in facts.items():
        models = fact.get("models", [])
        if not models or any(m not in MODELS - {"unknown"} for m in models):
            issue("error", "fact_model_invalid", identifier)
        if fact.get("status") not in {"verified", "pending"}:
            issue("error", "fact_status_invalid", identifier)
        refs = fact.get("source_refs", [])
        if fact.get("status") == "verified" and (not refs or not valid_date(fact.get("checked_at"))):
            issue("error", "verified_fact_missing_provenance", identifier)
        for ref in refs:
            src = sources.get(ref.get("source_id")) if isinstance(ref, dict) else None
            if not src:
                issue("error", "fact_source_missing", identifier)
                continue
            if not ref.get("locator") or not ref.get("quote"):
                issue("error", "fact_quote_or_locator_missing", identifier)
            elif ref["quote"] not in src.get("excerpt", ""):
                issue("error", "fact_quote_not_in_source_excerpt", identifier, source_id=src["source_id"])
            if not set(models).issubset(set(src.get("model_ids", []))):
                issue("error", "fact_source_model_mismatch", identifier, source_id=src["source_id"])
        claim_id = fact.get("claim_id")
        if claim_id and registry:
            claim = registry.get(claim_id)
            if not claim or not set(models).issubset(set(claim.get("models", []))):
                issue("error", "claim_mapping_invalid", identifier, claim_id=claim_id)
            elif not {source_identity(sources[r["source_id"]]["url"]) for r in refs if isinstance(r, dict) and r.get("source_id") in sources}.intersection({source_identity(u) for u in claim.get("official_sources", [])}):
                issue("error", "claim_source_mapping_missing", identifier, claim_id=claim_id)
    for identifier, record in records.items():
        if record.get("split") not in {"legacy", "train", "holdout"}:
            issue("error", "record_split_invalid", identifier)
        if record.get("model_id", "unknown") not in MODELS:
            issue("error", "record_model_invalid", identifier)
        path = source_path(root, record.get("source_path"))
        if not path or not path.is_file() or not record.get("source_locator"):
            issue("error", "record_source_missing", identifier)
        non_text = record.get("text_status") == "absent_in_export" and bool(record.get("limitations"))
        if (not record.get("text") and not non_text) or not record.get("work_id"):
            issue("error", "record_context_missing", identifier)
        work = works.get(record.get("work_id"))
        if record.get("split") in {"train", "holdout"} and not work:
            issue("error", "record_work_missing", identifier)
        if work and record.get("split") != work.get("split"):
            issue("error", "work_record_split_mismatch", identifier)
        parent_id = record.get("parent_id")
        if record.get("thread_role") == "reply" and not parent_id:
            issue("warning", "reply_parent_unavailable", identifier)
        if parent_id:
            parent = records.get(parent_id)
            if parent_id == identifier:
                issue("error", "reply_self_parent", identifier)
            elif not parent:
                issue("warning", "reply_parent_unavailable", identifier, parent_id=parent_id)
            elif parent.get("work_id") != record.get("work_id"):
                issue("error", "reply_parent_wrong_work", identifier)
            elif (parent.get("root_id") or parent.get("id")) != record.get("root_id"):
                issue("error", "reply_root_mismatch", identifier)
        chain_seen, cursor = set(), identifier
        while cursor in records:
            if cursor in chain_seen:
                issue("error", "reply_parent_cycle", identifier)
                break
            chain_seen.add(cursor)
            cursor = records[cursor].get("parent_id")
    for identifier, card in voices.items():
        references = evidence_ids(card)
        linked = [records[r] for r in references if r in records]
        if not references or len(linked) != len(references):
            issue("error", "voice_evidence_missing", identifier)
        actual = {r["work_id"] for r in linked if r.get("work_id")}
        if set(card.get("work_ids", [])) != actual:
            issue("error", "voice_work_references_inconsistent", identifier, evidence_works=sorted(actual))
        if card.get("status") not in {"pattern", "case"}:
            issue("error", "voice_status_invalid", identifier)
        if card.get("status") == "pattern" and len(actual) < 3:
            issue("error", "pattern_needs_three_independent_works", identifier)
        if any(r.get("split") == "holdout" or works.get(r.get("work_id"), {}).get("split") == "holdout" for r in linked):
            issue("error", "holdout_leaked_into_voice_card", identifier)
    for scenario in data["scenarios"]:
        for field, table in (("product_fact_ids", facts), ("voice_card_ids", voices)):
            for ref in scenario.get(field, []):
                if ref not in table:
                    issue("error", "scenario_reference_missing", scenario.get("id"), field=field, reference=ref)
        if scenario.get("basis") not in {"evidence", "editorial_hypothesis"}:
            issue("error", "scenario_basis_invalid", scenario.get("id"))
        if scenario.get("basis") == "evidence" and not scenario.get("voice_card_ids"):
            issue("error", "scenario_no_user_evidence", scenario.get("id"))
    eligible, excluded, excluded_details = [], Counter(), []
    author_counts = Counter()
    seen_urls = set()
    sourced_text_records = {identifier for identifier, r in records.items()
                            if r.get("material_kind", "comment") == "comment" and r.get("text") and r.get("source_locator") and source_path(root, r.get("source_path"))
                            and source_path(root, r.get("source_path")).is_file()}
    commented_works = {records[r]["work_id"] for r in sourced_text_records if records[r].get("work_id")}
    sourced_discussion_records = {identifier for identifier in sourced_text_records if has_textual_content(records[identifier].get("text"))}
    for identifier, work in sorted(works.items(), key=sampling_order):
        reason = None
        path = source_path(root, work.get("source_path"))
        if work.get("sampling_status") == "excluded" and work.get("sampling_exclusion_reason"): reason = "sampling_excluded"
        elif work.get("split") == "legacy": reason = "legacy"
        elif work.get("split") not in {"train", "holdout"}: reason = "invalid_split"
        elif work.get("status") != "success": reason = work.get("status", "missing_status")
        elif work.get("platform") not in PLATFORMS: reason = "invalid_platform"
        elif not work.get("author_id"): reason = "missing_author"
        elif work.get("model_id") not in MODELS - {"unknown"} or not work.get("model_basis"): reason = "unconfirmed_model"
        elif work.get("model_id") not in PRIMARY_MODELS: reason = "historical_model_reference"
        elif not work.get("canonical_url") or not work.get("read_scope") or not valid_date(str(work.get("collected_at", ""))[:10]): reason = "missing_read_evidence"
        elif not path or not path.is_file(): reason = "missing_source_file"
        elif identifier not in commented_works: reason = "missing_comment_context"
        author = (work.get("platform"), work.get("author_id"))
        if not reason and work.get("canonical_url") in seen_urls: reason = "duplicate_work_url"
        if not reason and author_counts[author] >= 2: reason = "author_over_two"
        if reason:
            excluded[reason] += 1
            detail = {"work_id": identifier, "reason": reason, "platform": work.get("platform"), "split": work.get("split")}
            if reason == "sampling_excluded":
                detail["sampling_exclusion_reason"] = work["sampling_exclusion_reason"]
            excluded_details.append(detail)
        else:
            author_counts[author] += 1
            seen_urls.add(work.get("canonical_url"))
            eligible.append(work)
    eligible_ids = {w["work_id"] for w in eligible}
    eligible_nonempty = {identifier for identifier in sourced_text_records if records[identifier].get("work_id") in eligible_ids}
    eligible_textual = eligible_nonempty & sourced_discussion_records
    mains = {r["id"] for r in records.values() if r.get("work_id") in eligible_ids and r.get("id") in sourced_discussion_records and r.get("thread_role") in {None, "root"} and not r.get("parent_id") and r.get("root_id") in {None, r.get("id")}}
    replied_roots = {r.get("root_id") for r in records.values()
                     if r.get("work_id") in eligible_ids and r.get("id") in sourced_discussion_records and r.get("parent_id") in sourced_discussion_records and r.get("parent_id") != r.get("id")
                     and records[r["parent_id"]].get("work_id") == r.get("work_id")
                     and r.get("root_id") in mains}
    by_platform = Counter(w["platform"] for w in eligible)
    by_model = Counter(w["model_id"] for w in eligible)
    by_split = Counter(w["split"] for w in eligible)
    by_platform_split = {platform: dict(Counter(w["split"] for w in eligible if w["platform"] == platform)) for platform in sorted(PLATFORMS)}
    complete = (all(by_platform[p] >= 50 for p in PLATFORMS) and
                all(by_model[m] >= n for m, n in MODEL_TARGETS.items()) and
                all(by_platform_split[p].get("train", 0) >= 40 and by_platform_split[p].get("holdout", 0) >= 10 for p in PLATFORMS) and
                by_split["train"] >= 120 and by_split["holdout"] >= 30 and len(mains) >= 450 and len(replied_roots) >= 150)
    errors = sum(i["severity"] == "error" for i in issues)
    primary_facts = [f for f in facts.values() if PRIMARY_MODELS.intersection(f.get("models", []))]
    scale_cancelled = project_scope.get("scale_target_status") == "cancelled_by_user"
    retained_exports = project_scope.get("retained_unreviewed_exports", [])
    retained_rows = sum(item.get("row_count", 0) for item in retained_exports if isinstance(item, dict) and isinstance(item.get("row_count"), int) and item["row_count"] >= 0)
    material_available = any(f.get("status") == "verified" for f in facts.values()) or bool(records)
    current_status = "integrity_review_required" if errors else "usable_with_documented_gaps" if material_available else "no_material_available"
    return {"integrity_ok": errors == 0, "corpus_target_complete": complete and errors == 0, "text_metrics_version": TEXT_METRICS_VERSION,
            "project_scope": project_scope,
            "current_library": {"status": current_status, "material_available": material_available, "integrity_ok": errors == 0,
                                "historical_scale_targets_required": not scale_cancelled and project_scope.get("profile") == "historical_150",
                                "retained_unreviewed_exports": retained_exports,
                                "retained_rows_basis": "collection-plan metadata only; these attachment rows are not loaded into corpus counts, retrieval or expression learning",
                                "evaluation_status": "not_assessed_by_this_audit", "collection_status_source": "corpus/run-state.json; actual capture states are not changed by this audit"},
            "historical_target": {"profile": "historical_150", "status": "cancelled_by_user" if scale_cancelled else "active",
                                  "met": complete and errors == 0, "applies_to_current_scope": not scale_cancelled,
                                  "compatibility_fields": ["corpus_target_complete", "targets"],
                                  "note": "历史采样配额是否达到，不代表当前资料库交付或对照验收是否完成"},
            "counts": {"official_sources": len(sources), "verified_facts": sum(f.get("status") == "verified" for f in facts.values()),
                       "pending_facts": sum(f.get("status") == "pending" for f in facts.values()),
                       "primary_verified_facts": sum(f.get("status") == "verified" for f in primary_facts),
                       "primary_pending_facts": sum(f.get("status") == "pending" for f in primary_facts),
                       "per_primary_model_verified": {model: sum(f.get("status") == "verified" and model in f.get("models", []) for f in primary_facts) for model in sorted(PRIMARY_MODELS)},
                       "voice_patterns": sum(c.get("status") == "pattern" for c in voices.values()),
                       "voice_cases": sum(c.get("status") == "case" for c in voices.values()), "legacy_comment_records": sum(r.get("split") == "legacy" and r.get("material_kind", "comment") == "comment" for r in records.values()),
                       "ingested_comment_records": sum(r.get("material_kind", "comment") == "comment" for r in data["comments"]),
                       "retained_unreviewed_comment_rows": retained_rows,
                       "eligible_new_works": len(eligible), "by_platform": dict(by_platform), "by_model": dict(by_model), "by_split": dict(by_split), "by_platform_split": by_platform_split,
                       "exported_nonempty_text_count": len(eligible_nonempty), "textual_content_comment_count": len(eligible_textual), "non_textual_nonempty_comment_count": len(eligible_nonempty - eligible_textual),
                       "main_discussions": len(mains), "discussions_with_verified_parent_reply": len(replied_roots), "excluded_works": dict(excluded)},
            "targets": {"works": 150, "per_platform": 50, "per_model": MODEL_TARGETS, "train": 120, "holdout": 30, "main_discussions": 450, "discussions_with_verified_parent_reply": 150},
            "eligible_work_ids": sorted(eligible_ids), "excluded_work_details": excluded_details,
            "issues": issues,
            "limitations": ["结构与引用检查不能证明来源正文真实或语义结论成立", "主款事实按唯一ID计数；分型号计数可共享同一事实，不能把per_primary_model_verified相加当作主款唯一总数", "历史种子不计150篇；holdout不进入常规检索和表达规律归纳", "缺失直接父句的回复不计入父句明确的讨论", "450组主评只计material_kind缺省或明确为comment的记录，帖子原话不补成评论", "文字讨论及其文字父句排除已知纯表情占位符和无字母数字的符号串；未知方括号内容保守保留。原记录与采集成功状态不变，不代表已读取图片。非空/文字/纯表情计数仅涵盖合格作品的有来源评论"]}


def tokens(query):
    result = set(re.findall(r"[a-z0-9]+", query.lower()))
    for part in re.findall(r"[\u4e00-\u9fff]+", query):
        result.add(part)
        result.update(part[i:i+2] for i in range(len(part)-1))
    return result


def relevance(item, terms):
    raw = json.dumps(item, ensure_ascii=False).lower()
    return sum((3 if len(t) > 2 else 1) for t in terms if t in raw)


FACT_TOPIC_FIELDS = {"title": 6, "fact": 4, "tags": 5, "conditions": 1, "uses": 2}
FACT_RELATED_TERMS = (
    {"导出", "传输", "拷贝", "转存", "传素材"},
    {"收纳", "拆装", "安装", "拆卸", "装卸", "拆下", "取下", "移除"},
    {"收音", "麦克风", "无线麦", "录音"},
    {"人物", "人像"},
)
FACT_LOW_INFORMATION_TERMS = {"拍摄", "相机", "功能", "模式", "使用", "设备", "产品", "支持", "相关", "官方", "视频", "效果", "问题", "操作", "素材"}
# These are technical contexts, not query-to-fact or scenario templates.
FACT_SPECIAL_CONTEXTS = (
    {"网络摄像头", "webcam", "会议", "电脑"},
    {"慢动作", "慢放", "慢镜", "升格", "帧", "fps"},
    {"格式化", "恢复", "报错", "故障", "损坏", "误删", "耗电", "不识别", "异常"},
    {"旧代", "转接头", "转接器", "换机", "升级"},
)


def fact_concepts(terms):
    remaining = set(terms)
    concepts = []
    for related in FACT_RELATED_TERMS:
        direct = remaining & related
        if direct:
            # A family contributes once per field, so listing synonyms cannot inflate it.
            concepts.append({term: 1 if term in direct else 0.65 for term in related})
            remaining -= related
    concepts.extend({term: 0.05 if term in FACT_LOW_INFORMATION_TERMS else 3 if len(term) > 2 else 1}
                    for term in sorted(remaining))
    return concepts


def fact_topic_scores(item, terms):
    """One score per query topic; provenance and non-inferences are excluded."""
    concepts = fact_concepts(terms)
    scores = [0.0] * len(concepts)
    specific_match = False
    for field, weight in FACT_TOPIC_FIELDS.items():
        value = item.get(field, "")
        if field == "conditions" and isinstance(value, list):
            value = [clause for condition in value for clause in re.split(r"[；;]", str(condition))
                     if not any(marker in clause for marker in ("不等于", "不证明", "不能推断"))]
        raw = json.dumps(value, ensure_ascii=False).lower()
        matches = [max((value for term, value in concept.items() if term in raw), default=0) for concept in concepts]
        scores = [score + weight * match for score, match in zip(scores, matches)]
        specific_match = specific_match or any(value > 0.05 for value in matches)
    # A specific need must match something beyond generic words such as 拍摄.
    return scores if specific_match or set(terms).issubset(FACT_LOW_INFORMATION_TERMS) else [0.0] * len(concepts)


def fact_relevance(item, terms):
    return sum(fact_topic_scores(item, terms))


def without_filtered_model(query, model):
    if not model:
        return query
    generation = model.removeprefix("pocket_")
    alias = rf"(?<![a-z0-9])(?:(?:大疆\s*|dji\s*)?(?:osmo\s*)?pocket[\s_-]*{generation}|p[\s_-]*{generation})(?![a-z0-9])"
    return re.sub(alias, " ", query, flags=re.IGNORECASE)


def fact_unasked_context(item, query):
    scope = json.dumps({key: item.get(key) for key in ("title", "tags")}, ensure_ascii=False).lower()
    return any(any(term in scope for term in context) and not any(term in query.lower() for term in context)
               for context in FACT_SPECIAL_CONTEXTS)


def rank_facts(items, terms, query, limit, model):
    exact = [item for item in items if item.get("id") == query.strip()]
    if exact:
        return exact
    scores = [(item, fact_topic_scores(item, terms)) for item in items]
    width = len(fact_concepts(terms))
    rarity = [1 + math.log((len(items) + 1) / (1 + sum(values[i] > 0 for _, values in scores))) for i in range(width)]
    candidates = []
    for item, values in scores:
        unasked_scope = fact_unasked_context(item, query)
        values = [value * rare * (0.5 if unasked_scope else 1) for value, rare in zip(values, rarity)]
        if sum(values) > 0:
            candidates.append((item, values))
    ordinary = [pair for pair in candidates if not fact_unasked_context(pair[0], query)]
    if ordinary:
        candidates = ordinary
    selected, covered = [], set()
    while candidates and len(selected) < limit:
        def priority(pair):
            item, values = pair
            primary = not model and bool(PRIMARY_MODELS.intersection(item.get("models", [])))
            # Once a topic is represented, favor another requested topic over repeats.
            score = sum(value * (0.35 if i in covered else 1) for i, value in enumerate(values))
            return -primary, -score, -sum(values), item.get("id", "")
        winner = min(candidates, key=priority)
        candidates.remove(winner)
        selected.append(winner[0])
        covered.update(i for i, value in enumerate(winner[1]) if value > 0)
    return selected


def comparison_material(root, card, records, works):
    """Resolve comparison learning sources without loading unrelated JSONL rows.

    Optional post-only references need an actual JSONL text locator and matching
    work identity. A work metadata entry by itself is not a quotation source.
    Holdout material never enters this learning section, even during an explicit
    holdout search elsewhere in the library.
    """
    if card.get("status") not in {"case", "pattern", "candidate"}:
        return None
    refs = card.get("evidence_ids", [])
    source_refs = card.get("source_refs", [])
    if not isinstance(refs, list) or not isinstance(source_refs, list) or not (refs or source_refs):
        return None
    linked, resolved_refs, work_ids = {}, [], set()

    def safe_work(wid):
        work = works.get(wid)
        return work if work and work.get("split") != "holdout" else None

    def add_record(identifier):
        record = records.get(identifier)
        if not record or record.get("split") == "holdout" or not safe_work(record.get("work_id")) or not record.get("text"):
            return None
        path = source_path(root, record.get("source_path"))
        if not path or not path.is_file() or not record.get("source_locator"):
            return None
        linked[identifier] = {**record, "resolved_source_path": str(path)}
        work_ids.add(record["work_id"])
        return record

    for identifier in refs:
        if not isinstance(identifier, str) or not add_record(identifier):
            return None
    for ref in source_refs:
        if not isinstance(ref, dict) or ref.get("split") == "holdout":
            return None
        record = add_record(ref["evidence_id"]) if ref.get("evidence_id") else None
        if ref.get("evidence_id") and not record:
            return None
        wid = ref.get("work_id") or (record or {}).get("work_id")
        if not safe_work(wid) or (record and record.get("work_id") != wid):
            return None
        path = source_path(root, ref.get("source_path"))
        locator, quote = ref.get("source_locator"), ref.get("quote")
        if not path or not path.is_file() or not locator or not isinstance(quote, str) or not quote:
            return None
        if ref.get("source_sha256") and hashlib.sha256(path.read_bytes()).hexdigest() != ref["source_sha256"]:
            return None
        if isinstance(locator, dict) and isinstance(locator.get("line"), int) and locator["line"] > 0 and path.suffix == ".jsonl":
            target = None
            with path.open(encoding="utf-8") as handle:
                for number, raw in enumerate(handle, 1):
                    if number == locator["line"]:
                        try:
                            target = json.loads(raw)
                        except ValueError:
                            return None
                        break
            if not isinstance(target, dict) or target.get("work_id") != wid or target.get("split") == "holdout":
                return None
            if not record and (target.get("comment_id") or not (target.get("kind") == "posts" or target.get("material_kind") in {"public_post", "post"})):
                return None
            pointer = locator.get("json_pointer", "/text")
            if pointer not in {"/text", "/title", "/post_fields/post_text", "/post_fields/post_title"}:
                return None
            value = target
            for part in pointer.strip("/").split("/"):
                value = value.get(part) if isinstance(value, dict) else None
            if not isinstance(value, str) or quote not in value:
                return None
            if record and target.get("comment_id") and target["comment_id"] != record.get("comment_id"):
                return None
        else:
            # XLSX/text source locators can only reuse an already admitted record
            # with the identical locator, never attach a quote to work metadata.
            if not record or path != source_path(root, record.get("source_path")) or locator != record.get("source_locator") or quote not in record["text"]:
                return None
            value = record["text"]
        start, end = ref.get("quote_char_start"), ref.get("quote_char_end")
        if start is not None or end is not None:
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start or value[start:end] != quote:
                return None
        resolved_refs.append({**ref, "work_id": wid, "resolved_source_path": str(path), "material_kind": (record or {}).get("material_kind", "public_post")})
        work_ids.add(wid)
    if card.get("status") == "pattern" and len(work_ids) < 3:
        return None
    return {"records": list(linked.values()), "sources": resolved_refs, "work_ids": work_ids}


def retrieve(root, data, query, model=None, platform=None, limit=3, include_holdout=False, competitor=None):
    facts = index(data["facts"])
    sources = index(data["sources"], "source_id")
    works = index(data["works"], "work_id")
    records = index(data["records"] + data["comments"])
    registry = get_registry(root)
    topic_query = query if query.strip() in facts else without_filtered_model(query, model)
    terms = tokens(topic_query)
    def allowed_record(r):
        if not include_holdout and (r.get("split") == "holdout" or works.get(r.get("work_id"), {}).get("split") == "holdout"):
            return False
        if platform and r.get("platform") != platform: return False
        if model and r.get("model_id", "unknown") not in {model, "unknown"}: return False
        return True
    eligible_voice = []
    for card in data["voice"]:
        refs = evidence_ids(card)
        linked = [records[r] for r in refs if r in records]
        if not linked or len(linked) != len(refs) or any(not r.get("text") for r in linked): continue
        if not include_holdout and any(r.get("split") == "holdout" or works.get(r.get("work_id"), {}).get("split") == "holdout" for r in linked): continue
        if not any(allowed_record(r) for r in linked): continue
        if card.get("status") == "pattern" and len({r.get("work_id") for r in linked}) < 3: continue
        selected = dict(card)
        matching = [r for r in linked if allowed_record(r)]
        selected["evidence_scope"] = {"all_work_count": len({r.get("work_id") for r in linked}),
                                      "matched_work_count": len({r.get("work_id") for r in matching}),
                                      "notice": "平台/型号筛选例句不把跨作品语言观察变成本型号的人群规律"}
        samples, sampled_works = [], set()
        for r in matching:
            if r.get("work_id") not in sampled_works:
                samples.append(r)
                sampled_works.add(r.get("work_id"))
        samples = (samples + [r for r in matching if r not in samples])[:3]
        selected["matched_records"] = []
        for r in samples:
            item = {k: r.get(k) for k in ("id", "work_id", "platform", "model_id", "text", "parent_id", "source_path", "source_locator", "split", "limitations")}
            resolved = source_path(root, r.get("source_path"))
            item["resolved_source_path"] = str(resolved) if resolved else None
            item["material_kind"] = r.get("material_kind", "comment")
            item.update({k: r[k] for k in ("source_kind", "speaker_scope", "thread_role") if k in r})
            parent = records.get(r.get("parent_id"))
            if (item["material_kind"] == "comment" and parent and parent.get("material_kind", "comment") == "comment"
                    and parent.get("work_id") == r.get("work_id") and allowed_record(parent)):
                item["parent_text"] = parent.get("text")
                item["parent_source_locator"] = parent.get("source_locator")
                parent_path = source_path(root, parent.get("source_path"))
                item["parent_resolved_source_path"] = str(parent_path) if parent_path else None
            else:
                item["parent_text"] = None
            selected["matched_records"].append(item)
        eligible_voice.append(selected)
    available_voice_ids = {c["id"] for c in eligible_voice}
    eligible_facts, pending = [], []
    for fact in data["facts"]:
        if model and model not in fact.get("models", []): continue
        if fact.get("status") == "pending":
            pending.append(fact)
            continue
        if fact.get("status") != "verified" or not valid_date(fact.get("checked_at")): continue
        refs = fact.get("source_refs", [])
        if not refs or any(ref.get("source_id") not in sources for ref in refs): continue
        if any(not ref.get("quote") or not ref.get("locator") or ref["quote"] not in sources[ref["source_id"]].get("excerpt", "") for ref in refs): continue
        if any(not official_url(sources[ref["source_id"]].get("url")) or not valid_date(sources[ref["source_id"]].get("checked_at")) or not set(fact.get("models", [])).issubset(set(sources[ref["source_id"]].get("model_ids", []))) for ref in refs): continue
        item = dict(fact)
        item["sources"] = [{"source_id": ref["source_id"], "url": sources[ref["source_id"]]["url"], "locator": ref.get("locator"), "checked_at": sources[ref["source_id"]].get("checked_at")} for ref in refs]
        claim = registry.get(fact.get("claim_id"))
        mapped = bool(claim and set(fact.get("models", [])).issubset(set(claim.get("models", []))) and
                      {source_identity(source["url"]) for source in item["sources"]}.intersection({source_identity(u) for u in claim.get("official_sources", [])}))
        legacy_gate = "已登记claim，绑定product_facts原句" if mapped else "知识卡未映射可用claim，需登记claim与必要回归后绑定product_facts原句"
        item["writing_gate"] = "CW2：写正文前复核当前官网，将实际证据登记为product来源并绑定product_fact断言；LH13专项审查：" + legacy_gate
        eligible_facts.append(item)
    fact_ids = {f["id"] for f in eligible_facts}
    eligible_scenarios = []
    for card in data["scenarios"]:
        if model and card.get("product_fact_ids") and not fact_ids.intersection(card["product_fact_ids"]): continue
        if card.get("voice_card_ids") and not available_voice_ids.intersection(card["voice_card_ids"]): continue
        selected = dict(card)
        selected["available_product_fact_ids"] = sorted(fact_ids.intersection(card.get("product_fact_ids", [])))
        selected["available_voice_card_ids"] = sorted(available_voice_ids.intersection(card.get("voice_card_ids", [])))
        eligible_scenarios.append(selected)
    def top(items, related_ids=(), scorer=relevance):
        scored = [(scorer(item, terms) + (5 if item.get("id") in related_ids else 0), item) for item in items]
        def priority(item):
            item_models = set(item.get("models", [])) | {r.get("model_id") for r in item.get("matched_records", [])}
            return bool(not model and item_models & PRIMARY_MODELS)
        return [item for score, item in sorted(scored, key=lambda pair: (-priority(pair[1]), -pair[0], pair[1].get("id", ""))) if score > 0][:limit]
    selected_scenarios = top(eligible_scenarios)
    related_voice = {identifier for scenario in selected_scenarios for identifier in scenario.get("available_voice_card_ids", [])}
    selected_facts = rank_facts(eligible_facts, terms, topic_query, limit, model)
    selected_fact_ids = {fact["id"] for fact in selected_facts}
    follow_up = []
    focused_scenarios = [scenario for scenario in selected_scenarios if relevance({key: scenario.get(key) for key in ("title", "scene", "need", "tags")}, terms) > 0]
    if focused_scenarios:
        scenario = focused_scenarios[0]
        for connection in scenario.get("product_connections", []):
            identifier = connection.get("fact_id")
            if identifier in fact_ids and identifier not in selected_fact_ids:
                fact = next(fact for fact in eligible_facts if fact["id"] == identifier)
                if fact_unasked_context(fact, topic_query):
                    continue
                follow_up.append({"scenario_id": scenario["id"], "fact_id": identifier, "title": fact.get("title"),
                                  "purpose": connection.get("purpose"), "query": identifier,
                                  "notice": "相关场景的补检索引；需单独读卡核对条件，不代表完整教程"})
                break
    result = {"query": query, "model": model, "default_model_focus": sorted(PRIMARY_MODELS), "platform": platform, "holdout_included": include_holdout,
            "facts": selected_facts, "scenarios": selected_scenarios, "voice": top(eligible_voice, related_voice), "follow_up": follow_up,
            "pending_gaps": [{"id": f["id"], "title": f.get("title"), "status": "pending", "not_infer": f.get("not_infer", [])} for f in rank_facts(pending, terms, topic_query, limit, model)],
            "boundaries": ["先用当前帖子证据判断开口理由；知识卡不是当前帖的拍摄、型号或因果证据", "第三方过去经历不能改写成评论角色本人经历", "作品作者原话不是评论或楼中楼父句，不计450组主评讨论", "editorial_hypothesis为编辑推想，case为个案；不能写成人群共识", "检索未覆盖的问题须拆成具体子问题补检，可用完整事实ID查卡；不能用相邻模式或场景workflow拼成完整教程", "检索无结果须保留缺口，不能猜测补齐"]}
    if data.get("comparisons") or competitor is not None:
        comparison_terms = tokens(topic_query) | (tokens(competitor) if competitor else set())
        normalize = lambda value: re.sub(r"[\s_-]+", "", value).casefold()
        wanted = normalize(competitor) if competitor else None
        candidates = []
        for card in data.get("comparisons", []):
            if model and model not in card.get("models", []):
                continue
            rivals = card.get("competitors", [])
            if wanted and not any(isinstance(rival, str) and wanted in normalize(rival) for rival in rivals):
                continue
            try:
                material = comparison_material(root, card, records, works)
            except (OSError, ValueError, TypeError):
                # Missing/unreadable optional research sources remain a gap;
                # they must not take down otherwise usable product retrieval.
                continue
            if not material:
                continue
            matching = {wid for wid in material["work_ids"] if not platform or works[wid].get("platform") == platform}
            if not matching:
                continue
            topic = {k: card.get(k) for k in ("id", "title", "models", "competitors", "scene", "concerns", "analysis", "tags")}
            score = relevance(topic, comparison_terms)
            if not score:
                continue
            selected = dict(card)
            selected["matched_records"] = [{k: record.get(k) for k in ("id", "work_id", "platform", "model_id", "text", "parent_id", "source_path", "source_locator", "resolved_source_path", "split", "material_kind")}
                                           for record in material["records"] if record["work_id"] in matching][:3]
            for record in selected["matched_records"]:
                parent = records.get(record.get("parent_id"))
                parent_source = source_path(root, (parent or {}).get("source_path"))
                record["parent_text"] = parent.get("text") if parent and parent.get("work_id") == record["work_id"] and parent.get("split") != "holdout" and parent_source and parent_source.is_file() else None
            selected["matched_sources"] = [ref for ref in material["sources"] if ref["work_id"] in matching][:3]
            selected["evidence_scope"] = {"all_work_count": len(material["work_ids"]), "matched_work_count": len(matching),
                                           "notice": "讨论表达与分析，不是产品实测结论；筛选不把个案变成人群规律，留出材料不参与专题学习"}
            selected["product_fact_status"] = "not_verified_by_discussion"
            candidates.append((score, selected))
        result["comparisons"] = [card for _, card in sorted(candidates, key=lambda pair: (-pair[0], pair[1].get("id", "")))][:limit]
        if competitor is not None:
            result["competitor"] = competitor
    return result


def render_markdown(result, mode):
    if mode == "audit":
        current_scope = result["project_scope"].get("profile") == "current_library"
        status_labels = {"usable_with_documented_gaps": "可用（保留已记录缺口）", "integrity_review_required": "需修复引用结构错误", "no_material_available": "尚无材料"}
        summary = f"\n引用结构：{'通过' if result['integrity_ok'] else '存在错误'}"
        if current_scope:
            summary += f"；当前资料库：{status_labels[result['current_library']['status']]}。150篇/30篇验收规模已由用户取消，保留为历史计划。"
        else:
            summary += f"；历史150篇采样目标：{'达到' if result['corpus_target_complete'] else '未达到'}"
        lines = ["# Pocket 知识库检查与覆盖", summary, "\n对照验收独立记录；本检查不生成验收通过结论。", "\n```json", json.dumps(result["counts"], ensure_ascii=False, indent=2), "```"]
        if result["counts"]["retained_unreviewed_comment_rows"]:
            lines.append(f"\n已入库评论 {result['counts']['ingested_comment_records']} 条；另存未整理附件 {result['counts']['retained_unreviewed_comment_rows']} 条（采集台账元数据，不计有效样本、讨论或表达学习）。")
        if result.get("target_check", {}).get("error"):
            lines.append("\n" + result["target_check"]["message"])
        lines.append("\n主款事实按唯一ID计数；同一事实可同时适用4和4P，分型号数量不能相加当作主款唯一总数")
        lines.append("\n计入作品ID：" + ("、".join(result["eligible_work_ids"]) or "无"))
        if result["excluded_work_details"]:
            lines.append("\n排除明细（仅ID与原因）：")
            for detail in result["excluded_work_details"]:
                extra = f"：{detail['sampling_exclusion_reason']}" if detail.get("sampling_exclusion_reason") else ""
                lines.append(f"- {detail['work_id']} · {detail['platform']} · {detail['split']} · {detail['reason']}{extra}")
        lines += [f"- {i['severity']} · {i['code']} · {i['at']}" for i in result["issues"]]
        return "\n".join(lines)
    lines = [f"# 当前帖写作参考：{result['query']}"]
    sections = [("facts", "产品知识"), ("scenarios", "场景与过程"), ("voice", "表达与接话")]
    if "comparisons" in result:
        sections.append(("comparisons", "竞品比较表达（公共个案与观察）"))
    sections.append(("pending_gaps", "待核缺口"))
    for section, name in sections:
        lines += [f"\n## {name}"]
        if not result[section]: lines.append("无匹配证据")
        for item in result[section]:
            lines.append(f"\n### {item['id']} · {item.get('title', '')}")
            for field in ("fact", "conditions", "uses", "not_infer", "scene", "need", "workflow", "basis", "situation", "experience_level", "stance", "expression_purpose", "mechanism", "status", "transferable", "not_transferable", "evidence_scope", "writing_gate", "competitors", "concerns", "analysis", "boundaries"):
                value = item.get(field)
                if value: lines.append(f"- {field}：{json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value}")
            for source in item.get("sources", []): lines.append(f"- 来源 [{source['source_id']}]({source['url']}) · {source['locator']} · {source['checked_at']}")
            for record in item.get("matched_records", []):
                kind = record.get("material_kind", "comment")
                label = "作品作者原话" if kind in {"public_post", "post"} else "评论原话" if kind == "comment" else "语料原话"
                parent_note = f"父句ID：{record['parent_id']}；" if kind == "comment" else ""
                lines.append(f"- {label} {record['id']} / {record['work_id']} / {record['split']}：{record['text']}（{parent_note}{record.get('resolved_source_path') or record['source_path']} · {record['source_locator']}）")
                if kind == "comment" and record.get("parent_text"): lines.append(f"- 直接父句 {record['parent_id']}：{record['parent_text']}")
            for ref in item.get("matched_sources", []):
                quoted = "" if ref.get("evidence_id") in {r["id"] for r in item.get("matched_records", [])} else f"：{ref['quote']}"
                lines.append(f"- 证据 {ref.get('evidence_id') or ref['work_id']}{quoted}（{ref['resolved_source_path']} · {ref['source_locator']}）")
    if result.get("follow_up"):
        lines.append("\n## 可按需补检")
        for item in result["follow_up"]:
            lines.append(f"- {item['fact_id']} · {item['title']}：{item.get('purpose', '')}。用完整事实ID再次search；{item['notice']}")
    lines += ["\n## 使用边界", *[f"- {b}" for b in result["boundaries"]]]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="knowledge/pocket目录")
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="按当前帖需求检索；不生成评论正文")
    search.add_argument("query")
    search.add_argument("--model", help="例如 pocket_3、Pocket3、p3")
    search.add_argument("--platform", choices=sorted(PLATFORMS))
    search.add_argument("--competitor", help="仅筛选竞品表达专题，例如 手机、微单、Pocket4P；其他栏目沿用原检索")
    search.add_argument("--limit", type=int, default=3, help="每类最大条数，1至10")
    search.add_argument("--include-holdout", action="store_true", help="仅限验收阶段；显式读取留出材料")
    search.add_argument("--format", choices=["json", "markdown"], default="markdown")
    check = sub.add_parser("audit", help="引用校验及真实覆盖统计，默认只输出不改文件")
    check.add_argument("--format", choices=["json", "markdown"], default="markdown")
    check.add_argument("--require-target", action="store_true", help="显式要求采样配额；用户取消规模后须同时使用--historical-target")
    check.add_argument("--historical-target", action="store_true", help="仅回看历史150/120/30等采样配额，不作为当前资料库完成标准")
    resolve = sub.add_parser("resolve-source", help="将归档来源路径解析为当前资料包内路径；不读取社媒原链")
    resolve.add_argument("path")
    args = parser.parse_args(argv)
    if args.command == "resolve-source":
        path = source_path(args.root.resolve(), args.path)
        exists = bool(path and path.is_file())
        print(json.dumps({"original_path": args.path, "resolved_path": str(path) if path else None, "exists": exists}, ensure_ascii=False))
        return 0 if exists else 1
    data, issues = load(args.root.resolve())
    if args.command == "audit":
        result = audit(args.root.resolve(), data, issues)
        cancelled = result["historical_target"]["status"] == "cancelled_by_user"
        result["target_check"] = {"requested": args.require_target, "profile": "historical_150" if args.historical_target else result["project_scope"].get("profile"), "enforced": args.require_target and (not cancelled or args.historical_target)}
        status = 1 if not result["integrity_ok"] or (result["target_check"]["enforced"] and not result["corpus_target_complete"]) else 0
        if args.require_target and cancelled and not args.historical_target:
            result["target_check"].update(error="target_cancelled_by_user", message="用户已取消150篇/30篇验收的规模目标；当前按现有资料库整理。若要显式核对历史计划，请同时使用--historical-target。")
            status = 2 if result["integrity_ok"] else 1
    else:
        if not 1 <= args.limit <= 10: parser.error("--limit须在1至10之间")
        model = model_id(args.model) if args.model else None
        if args.model and model == "unknown": parser.error("无法确认--model，使用pocket_1/2/3/4/4p")
        if any(i["severity"] == "error" for i in issues):
            print(json.dumps({"error": "知识库JSONL无效，请先运行audit", "issues": issues}, ensure_ascii=False), file=sys.stderr)
            return 1
        result = retrieve(args.root.resolve(), data, args.query, model, args.platform, args.limit, args.include_holdout, args.competitor)
        status = 0
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(result, args.command))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
