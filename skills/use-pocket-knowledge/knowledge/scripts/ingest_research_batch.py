#!/usr/bin/env python3
"""Adapt verified social-helper research exports; preview unless --apply is explicit.

Contract: batch/manifest.json has batch_id and read_method="social_helper";
batch/comments.jsonl uses research-social-comments fields. Each evidence_ref is
{path: "evidence/raw/export.xlsx", sha256: "…", sheet: "Sheet1", row: 2}.
The unchanged unified ledger lives at evidence/input-ledger.jsonl. Its entries
need platform, workId/work_id, split, postsStatus, commentsStatus and
post_evidence={source_path, source_sha256, source_locator:{sheet,row}}.
Nonempty comments also require comment_evidence (or comment_sources entries)
identifying the recorded export path and SHA256; this reference needs no row.
All referenced files stay inside this batch's evidence/ directory. The recorded
XLSX is reparsed with ingest_social_exports; discovery text cannot pass this gate.

This does not collect, certify product facts, approve expression examples, change
old sampling splits, or resume old collection queues. Newly created work entries
remain research_evidence_imported_pending_review until a separate semantic review.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("research_export_parser", Path(__file__).with_name("ingest_social_exports.py"))
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)


class ResearchError(ValueError):
    """Errors contain metadata, never source quotations."""


def encoded(value, jsonl=False):
    return (("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in value)) if jsonl else
            json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(value):
    return hashlib.sha256(value).hexdigest()


def key(row):
    return (row.get("platform"), row.get("work_id", row.get("workId")), row.get("comment_id"))


def load(path, snapshots, jsonl=False, optional=False):
    content = path.read_bytes() if path.is_file() else None
    snapshots[path] = content
    if content is None:
        if optional:
            return [] if jsonl else {}
        raise ResearchError("Missing required file: " + path.name)
    try:
        value = [json.loads(line) for line in content.decode().splitlines() if line.strip()] if jsonl else json.loads(content)
    except (ValueError, UnicodeError) as exc:
        raise ResearchError("Invalid JSON: " + path.name) from exc
    if (jsonl and any(not isinstance(r, dict) for r in value)) or (not jsonl and not isinstance(value, dict)):
        raise ResearchError("Expected object records: " + path.name)
    return value


def evidence_path(batch, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ResearchError("Evidence path must be relative to the research batch")
    path = (batch / value).resolve()
    if not path.is_relative_to((batch / "evidence").resolve()) or not path.is_file():
        raise ResearchError("Evidence path is missing or outside batch/evidence")
    return path


def prepare(root, batch):
    root, batch = Path(root).resolve(), Path(batch).resolve()
    snapshots = {}
    manifest = load(batch / "manifest.json", snapshots)
    batch_id = manifest.get("batch_id")
    if not isinstance(batch_id, str) or not batch_id or manifest.get("read_method") != "social_helper":
        raise ResearchError("A named social_helper research batch is required; discovery alone is not evidence")
    incoming = load(batch / "comments.jsonl", snapshots, True)
    ledger_path = batch / "evidence/input-ledger.jsonl"
    ledger = load(ledger_path, snapshots, True)
    corpus = root / "corpus"
    comments_path, works_path = corpus / "comments.jsonl", corpus / "works.jsonl"
    comments = load(comments_path, snapshots, True, True)
    works = load(works_path, snapshots, True, True)
    historical_ledger = load(corpus / "input-ledger.jsonl", snapshots, True, True)
    legacy = load(root / "voice/records.jsonl", snapshots, True, True)
    state = load(corpus / "run-state.json", snapshots, optional=True)
    collection_plan = load(corpus / "collection-plan.json", snapshots, optional=True)
    protected = {(r.get("platform"), r.get("work_id", r.get("workId")))
                 for r in works + historical_ledger + comments + legacy if r.get("split") == "holdout"}
    stopped_hashes = set()
    stopped_paths = set()
    for old in state.get("batches", []):
        if old.get("stopped_by_user") or old.get("status") == "partial_saved_unreviewed_user_stop":
            protected.update((old.get("platform"), wid) for wid in old.get("work_ids", []))
            if old.get("source_sha256"):
                stopped_hashes.add(old["source_sha256"])
            for field in ("export_path", "normalized_path"):
                if old.get(field):
                    stopped_paths.add((corpus / old[field]).resolve())
    for old in collection_plan.get("current_scope", {}).get("retained_unreviewed_exports", []):
        for field in ("raw_path", "normalized_path"):
            if old.get(field):
                stopped_paths.add((root / old[field]).resolve())
    entries = {}
    for row in ledger:
        identity = row.get("platform"), row.get("work_id", row.get("workId"))
        if identity in entries:
            raise ResearchError("Duplicate work in unified evidence ledger")
        entries[identity] = row
    # Preflight before opening any incoming workbook, including mixed exports.
    if any(identity in protected or row.get("split") == "holdout" for identity, row in entries.items()):
        raise ResearchError("Research learning ledger includes a frozen holdout or stopped attachment work")
    if any(row.get("split") != "train" for row in ledger):
        raise ResearchError("New research learning ledger must explicitly use train")
    existing = {}
    all_ids = {}
    for row in comments + legacy:
        if all(key(row)):
            if key(row) in existing:
                raise ResearchError("Existing corpus has duplicate real comment identities")
            existing[key(row)] = row
        all_ids[row.get("id")] = row
    work_index = {(r.get("platform"), r.get("work_id")): r for r in works}
    # Existing consumers index works by raw work_id. Reject a cross-platform collision.
    work_ids = {r.get("work_id"): r.get("platform") for r in works}
    cache = {}

    def verified(ref, platform, kind):
        if not isinstance(ref, dict):
            raise ResearchError("Structured source reference is required")
        path = evidence_path(batch, ref.get("path", ref.get("source_path")))
        if path in stopped_paths:
            raise ResearchError("Stopped attachment cannot enter research learning")
        if path not in snapshots:
            snapshots[path] = path.read_bytes()
        digest = sha(snapshots[path])
        if digest in stopped_hashes:
            raise ResearchError("Stopped attachment bytes cannot be copied into research learning")
        if digest != ref.get("sha256", ref.get("source_sha256")):
            raise ResearchError("Source hash does not match the recorded export")
        locator = ref.get("source_locator", ref)
        if not isinstance(locator.get("sheet"), str) or not isinstance(locator.get("row"), int) or locator["row"] < 2:
            raise ResearchError("Original sheet and data row are required")
        cache_key = path, platform, kind
        if cache_key not in cache:
            try:
                rows, _ = EXPORT.parse_export(platform, kind, path, ledger_path)
            except Exception as exc:
                raise ResearchError("Recorded XLSX cannot be verified with the social-helper parser") from exc
            if any((r["platform"], r.get("work_id")) in protected for r in rows):
                raise ResearchError("Export contains a frozen holdout or stopped attachment work")
            cache[cache_key] = {(r["source_locator"]["sheet"], r["source_locator"]["row"]): r for r in rows}
        row = cache[cache_key].get((locator["sheet"], locator["row"]))
        if not row or row.get("normalization_status") != "parsed" or row.get("ledger_match") != "matched":
            raise ResearchError("Source row is missing, unmatched, or needs normalization review")
        return row

    counts = Counter({name: 0 for name in ("new", "existing", "content_changed", "duplicate_within_batch", "post_only_works")})
    counts["input_records"] = len(incoming)
    gaps, changed, accepted, seen = [], [], {}, {}
    new_works = {}

    def make_work(post, entry, comment_scope=None):
        return {"work_id": post["work_id"], "platform": post["platform"], "split": "train", "research_batch_id": batch_id,
                "canonical_url": post.get("canonical_url"), "author_id": post.get("author_id"), "model_id": post.get("model_id", "unknown"),
                "model_basis": {"scope": "discussion_context_only", "normalized_basis": post.get("model_basis")},
                "source_path": post["source_path"], "source_locator": post["source_locator"], "post_source_sha256": post["source_sha256"],
                "collected_at": post.get("collected_at"), "read_scope": [post["read_scope"]] + ([comment_scope] if comment_scope else []),
                "limitations": post["limitations"], "status": "research_evidence_imported_pending_review" if comment_scope else "research_posts_only_comments_empty",
                "comment_collection_status": entry.get("commentsStatus"), "input_order": entry.get("inputOrder")}
    for line, row in enumerate(incoming, 1):
        identity = key(row)
        platform, wid, cid = identity
        try:
            if platform not in EXPORT.PLATFORMS or not all(isinstance(v, str) and v for v in identity):
                raise ResearchError("Actual platform/work/comment IDs required; fallback remains research-only")
            if (platform, wid) in protected:
                raise ResearchError("Frozen holdout or stopped attachment work")
            if row.get("read_method") != "social_helper" or "op" not in row.get("product_codes", []):
                raise ResearchError("Not an op social-helper comment")
            entry = entries.get((platform, wid))
            if not entry or entry.get("postsStatus") != "success" or entry.get("commentsStatus") not in {"success", "partial"}:
                raise ResearchError("Unified ledger does not verify post and comment evidence")
            if wid in work_ids and work_ids[wid] != platform:
                raise ResearchError("Work ID collides across platforms in existing library")
            reference = row.get("evidence_ref")
            if not isinstance(reference, dict):
                raise ResearchError("Structured source reference is required")
            comment_path = evidence_path(batch, reference.get("path", reference.get("source_path")))
            registered = ([entry["comment_evidence"]] if isinstance(entry.get("comment_evidence"), dict) else []) + entry.get("comment_sources", [])
            if not any(isinstance(ref, dict) and
                       evidence_path(batch, ref.get("path", ref.get("source_path"))) == comment_path and
                       ref.get("sha256", ref.get("source_sha256")) == reference.get("sha256", reference.get("source_sha256"))
                       for ref in registered):
                raise ResearchError("Comment export is not recorded in the unified evidence ledger")
            parsed = verified(row.get("evidence_ref"), platform, "comments")
            expected_parent = parsed.get("parent_id")
            expected_root = parsed.get("root_id")
            fields = {"work_id": wid, "comment_id": cid, "text": row.get("text_raw"),
                      "parent_id": platform + ":" + row["parent_comment_id"] if row.get("parent_comment_id") else None,
                      "root_id": platform + ":" + row["root_comment_id"] if row.get("root_comment_id") not in {None, cid} else None}
            if any(parsed.get(k) != value for k, value in fields.items()):
                raise ResearchError("Research identity, text or relationship differs from original export")
            if row.get("parent_text_raw") is not None and row["parent_text_raw"] != parsed.get("referenced_comment_text"):
                raise ResearchError("Direct parent quotation differs from original export")
            post = verified(entry.get("post_evidence"), platform, "posts")
            if post.get("work_id") != wid:
                raise ResearchError("Post evidence work ID mismatch")
            signature = (parsed.get("text"), expected_parent, expected_root)
            if identity in seen and seen[identity] != signature:
                raise ResearchError("Conflicting content for one comment within the new batch")
            seen[identity] = signature
            prior = existing.get(identity)

            def raw_link(value):
                linked = all_ids.get(value)
                return linked.get("comment_id") if linked else value.split(":")[-1] if value else None

            prior_signature = (prior.get("text"), platform + ":" + raw_link(prior.get("parent_id")) if prior.get("parent_id") else None,
                               platform + ":" + raw_link(prior.get("root_id")) if prior.get("root_id") else None) if prior else None
            occurrence = {"batch_id": batch_id, "research_record_key": row.get("record_key"), "research_line": line,
                          "research_path": str(batch / "comments.jsonl"), "research_sha256": sha(snapshots[batch / "comments.jsonl"]),
                          "source_input_orders": copy.deepcopy(row.get("source_input_orders", [])),
                          "source_path": parsed["source_path"], "source_sha256": parsed["source_sha256"],
                          "source_locator": copy.deepcopy(parsed["source_locator"]), "source_columns": copy.deepcopy(parsed["source_columns"]),
                          "collected_at": row.get("collected_at"), "created_at_raw": row.get("created_at_raw"),
                          "created_at": row.get("created_at"), "like_count": row.get("like_count"),
                          "evidence_ref": copy.deepcopy(row["evidence_ref"]), "read_method": "social_helper"}
            if prior and prior_signature != signature:
                if any(tuple(item["identity"]) == identity for item in changed):
                    counts["duplicate_within_batch"] += 1
                    next(item for item in changed if tuple(item["identity"]) == identity).setdefault("additional_occurrences", []).append(occurrence)
                    continue
                changed.append({"existing_id": prior["id"], "record_key": row.get("record_key"), "identity": list(identity), "source_occurrence": occurrence,
                                "status": "content_changed_pending_review", "canonical_record_unchanged": True})
                counts["content_changed"] += 1
                continue
            if identity in accepted:
                if occurrence not in accepted[identity]["source_occurrences"]:
                    accepted[identity]["source_occurrences"].append(occurrence)
                counts["duplicate_within_batch"] += 1
                continue
            if prior:
                record = copy.deepcopy(prior)
                record.setdefault("source_occurrences", [])
                counts["existing"] += 1
            else:
                keep = ("comment_id", "work_id", "platform", "text", "text_status", "image_urls", "thread_role", "parent_basis",
                        "parent_lookup", "parent_source_locator", "referenced_comment_text", "root_comment_text", "parent_quote_source_locator",
                        "created_at", "collected_at", "comment_likes", "reported_reply_count", "read_scope", "limitations", "source_columns",
                        "source_path", "source_sha256", "source_locator", "model_id", "model_candidates")
                record = {k: copy.deepcopy(parsed[k]) for k in keep if k in parsed}
                record.update(id=":".join(identity), material_kind="comment", kind="comments", source_kind="public_comment",
                              speaker_scope="comment_author", split="train", split_basis="new_research_batch_frozen_train",
                              canonical_url=EXPORT.canonical_url(row.get("source_url")), normalization_status="parsed", ledger_match="matched",
                              model_basis={"scope": "discussion_context_only", "normalized_basis": parsed.get("model_basis"),
                                           "not_infer": "不证明持有、使用或实际拍摄设备；评论不是产品事实"}, source_occurrences=[])
                counts["new"] += 1
            if occurrence not in record["source_occurrences"]:
                record["source_occurrences"].append(occurrence)
            accepted[identity] = record
            if not prior and (platform, wid) not in work_index:
                new_works[(platform, wid)] = make_work(post, entry, parsed["read_scope"])
        except (ResearchError, TypeError, KeyError) as exc:
            gaps.append({"research_line": line, "record_key": row.get("record_key"), "identity": list(identity), "reason": str(exc)})
    # A verified post with an explicitly empty comment result is metadata only.
    # It never becomes a successful discussion or a fabricated comment record.
    incoming_works = {(r.get("platform"), r.get("work_id")) for r in incoming}
    for identity, entry in entries.items():
        if identity in work_index or identity in incoming_works or entry.get("postsStatus") != "success" or entry.get("commentsStatus") != "empty":
            continue
        try:
            post = verified(entry.get("post_evidence"), identity[0], "posts")
            if (post["platform"], post["work_id"]) != identity:
                raise ResearchError("Post evidence work ID mismatch")
            if identity[1] in work_ids and work_ids[identity[1]] != identity[0]:
                raise ResearchError("Work ID collides across platforms in existing library")
            new_works[identity] = make_work(post, entry)
            counts["post_only_works"] += 1
        except (ResearchError, TypeError, KeyError) as exc:
            gaps.append({"research_line": None, "identity": list(identity), "reason": str(exc)})
    # Use existing IDs when a parent already lives in the old corpus; otherwise a
    # three-part ID prevents identical comment IDs under different works merging.
    id_map = {identity: row["id"] for identity, row in {**existing, **accepted}.items()}
    for identity, row in accepted.items():
        if identity in existing:
            continue
        source = incoming[row["source_occurrences"][0]["research_line"] - 1]
        for dest, field in (("parent_id", "parent_comment_id"), ("root_id", "root_comment_id")):
            raw = source.get(field)
            target = identity[:2] + (raw,)
            row[dest] = id_map.get(target, ":".join(target)) if raw and not (dest == "root_id" and raw == identity[2]) else None
    # Existing legacy records stay byte-for-byte in voice/records.jsonl. Their new
    # occurrences remain in the batch adaptation file, rather than double-counting.
    current_keys = {key(row) for row in comments}
    merged_comments = [accepted.get(key(row), row) for row in comments]
    merged_comments.extend(row for identity, row in accepted.items() if identity not in existing)
    counts.update(accepted_unique=len(accepted), new_works=len(new_works), rejected=len(gaps))
    summary = {"batch_id": batch_id, "mode": "preview", "counts": dict(counts), "gaps": gaps,
               "apply_allowed": bool(accepted or new_works) and not gaps, "content_changes_need_review": bool(changed),
               "old_splits_preserved": True, "old_run_state_unchanged": True, "product_facts_written": False,
               "new_work_status": "research_evidence_imported_pending_review"}
    outputs = {comments_path: encoded(merged_comments, True), works_path: encoded(works + list(new_works.values()), True)}
    return {"summary": summary, "snapshots": snapshots, "outputs": outputs,
            "adapted_records": list(accepted.values()), "content_changes": changed,
            "legacy_existing": sum(identity not in current_keys and identity in existing for identity in accepted)}


def apply(plan):
    if not plan["summary"]["apply_allowed"]:
        raise ResearchError("No verified admission or unresolved rejected rows; apply is blocked")
    for path, before in plan["snapshots"].items():
        now = path.read_bytes() if path.is_file() else None
        if now != before:
            raise ResearchError("Input changed after preview; prepare again")
    temporary, replaced = {}, []
    try:
        for path, data in plan["outputs"].items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".research-", delete=False) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
                temporary[path] = Path(stream.name)
        for path, temporary_path in temporary.items():
            os.replace(temporary_path, path)
            replaced.append(path)
    except OSError:
        for path in reversed(replaced):
            before = plan["snapshots"][path]
            path.write_bytes(before) if before is not None else path.unlink(missing_ok=True)
        raise
    finally:
        for path in temporary.values():
            path.unlink(missing_ok=True)
    return {**plan["summary"], "mode": "applied"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--batch-dir", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, help="Optional new preview directory; never overwrite existing output")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.output_dir and args.output_dir.exists():
            raise ResearchError("Output directory exists; choose a new preview directory")
        plan = prepare(args.root, args.batch_dir)
        summary = apply(plan) if args.apply else plan["summary"]
        if args.output_dir:
            args.output_dir.mkdir(parents=True)
            (args.output_dir / "report.json").write_bytes(encoded(summary))
            (args.output_dir / "adapted-records.jsonl").write_bytes(encoded(plan["adapted_records"], True))
            (args.output_dir / "content-changes.jsonl").write_bytes(encoded(plan["content_changes"], True))
        print(json.dumps(summary, ensure_ascii=False))
        return 0 if summary["apply_allowed"] else 1
    except (ResearchError, OSError, ValueError) as exc:
        print(json.dumps({"mode": "error", "error": str(exc), "product_facts_written": False}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
