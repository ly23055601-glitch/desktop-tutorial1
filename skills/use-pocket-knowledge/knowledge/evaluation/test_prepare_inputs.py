"""Isolated synthetic fixtures only; never opens real holdout content."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("prepare_inputs", Path(__file__).with_name("prepare_inputs.py"))
prep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prep)


class Fixture:
    def __init__(self, directory, count=10):
        self.root = Path(directory) / "project/knowledge/pocket"
        self.corpus = self.root / "corpus"
        (self.corpus / "normalized").mkdir(parents=True)
        (self.corpus / "raw").mkdir()
        (self.root / "evaluation").mkdir()
        (self.root / "evaluation/README.md").write_text("Synthetic evaluation protocol", encoding="utf-8")
        skill = self.root.parent.parent / ".agents/skills/write-pocket-seeding-comments/MODULE.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(prep.RULE_VERSION, encoding="utf-8")
        # These must never be read, even by the default metadata operation.
        for name in ("voice", "products", "scenarios"):
            (self.root / name).mkdir()
            (self.root / name / "cards.jsonl").write_text("INVALID TRAINING JSON", encoding="utf-8")
        self.raw = self.corpus / "raw/synthetic-fixture-source.bin"
        self.raw.write_bytes(b"SYNTHETIC FIXTURE ONLY: not an actual social export")
        self.rawsha = prep.digest(self.raw.read_bytes())
        self.posts, self.comments, self.works, self.ledger = [], [], [], []
        self.add("train-work", "xiaohongshu", 1, split="train", author="train-author")
        order = 2
        for platform in prep.PLATFORMS:
            for n in range(count):
                self.add(f"{platform}-holdout-{n}", platform, order)
                order += 1
        self.flush()

    def add(self, wid, platform, order, split="holdout", author=None, excluded=False, reserve=False):
        rownum = len(self.posts) + 2
        columns = {"post_title": {"header": "TITLE", "column": "D"},
                   "post_text": {"header": "BODY", "column": "E"},
                   "captured_at": {"header": "CAPTURED", "column": "N"}}
        post = {"kind": "posts", "work_id": wid, "platform": platform, "split": split,
                "inputOrder": order, "ledger_match": "matched", "source_path": str(self.raw),
                "source_sha256": self.rawsha, "source_locator": {"sheet": "Fixture", "row": rownum},
                "source_columns": columns, "title": f"{split.upper()}_TITLE_SENTINEL_{wid}",
                "text": f"{split.upper()}_BODY_SENTINEL_{wid}", "author_id": author or wid + "-author",
                "collected_at": "2000-01-01T12:00:00", "created_at": "2000-01-01T11:00:00",
                "read_scope": "exported_post_text_only; no_media_review"}
        self.posts.append(post)
        work = {"work_id": wid, "platform": platform, "input_order": order, "split": split,
                "status": "success", "author_id": post["author_id"], "model_id": "pocket_4",
                "model_basis": {"scope": "discussion_context_only"},
                "canonical_url": f"https://example.test/{wid}", "source_path": str(self.raw),
                "source_locator": post["source_locator"], "post_source_sha256": self.rawsha,
                "collected_at": post["collected_at"], "read_scope": ["post_text", "comment_text"]}
        if excluded:
            work.update(sampling_status="excluded", sampling_exclusion_reason="explicit_metadata_exclusion")
        self.works.append(work)
        entry = {"workId": wid, "platform": platform, "inputOrder": order, "split": split,
                 "post_evidence": {"source_path": str(self.raw), "source_locator": post["source_locator"],
                                   "source_sha256": self.rawsha, "normalized_path": "normalized/posts.jsonl"}}
        if reserve:
            entry["input_set_id"] = "synthetic-reserve"
        self.ledger.append(entry)
        for num, role in enumerate(("root", "reply", "reply")):
            cid = f"{platform}:{wid}-comment-{num}"
            root = f"{platform}:{wid}-comment-0"
            record = {"id": cid, "kind": "comments", "comment_id": cid.split(":", 1)[1],
                      "work_id": wid, "platform": platform, "split": split, "material_kind": "comment",
                      "text": f"{split.upper()}_COMMENT_SENTINEL_{cid}" if num != 2 else None,
                      "text_status": "available" if num != 2 else "absent_in_export",
                      "parent_id": root if num == 1 else f"{platform}:missing-parent" if num == 2 else None,
                      "root_id": root if num else None, "thread_role": role,
                      "parent_basis": "exported_reference_id" if num else "not_provided",
                      "source_path": str(self.raw), "source_sha256": self.rawsha,
                      "source_locator": {"sheet": "Comments", "row": len(self.comments) + 2},
                      "source_columns": {"text": {"header": "TEXT", "column": "C"},
                                         "comment_id": {"header": "ID", "column": "B"},
                                         "root_comment_id": {"header": "ROOT", "column": "D"},
                                         "referenced_comment_id": {"header": "PARENT", "column": "E"},
                                         "captured_at": {"header": "CAPTURED", "column": "F"}},
                      "collected_at": "2000-01-01T12:00:00", "image_urls": ["https://example.test/image"] if num == 2 else [],
                      "limitations": ["synthetic test record; media not read"]}
            self.comments.append(record)

    def flush(self):
        def jsonl(path, rows):
            path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        jsonl(self.corpus / "normalized/posts.jsonl", self.posts)
        normalized = self.corpus / "normalized/comments.jsonl"
        jsonl(normalized, self.comments)
        normsha = prep.digest(normalized.read_bytes())
        records = copy.deepcopy(self.comments)
        for line, r in enumerate(records, 1):
            r["source_occurrences"] = [{"source_path": str(self.raw), "source_sha256": self.rawsha,
                                         "source_locator": r["source_locator"], "normalized_path": str(normalized),
                                         "normalized_sha256": normsha, "normalized_line": line, "batch_id": "fixture"}]
        jsonl(self.corpus / "comments.jsonl", records)
        jsonl(self.corpus / "works.jsonl", self.works)
        jsonl(self.corpus / "input-ledger.jsonl", self.ledger)
        (self.corpus / "run-state.json").write_text(json.dumps({"startedAt": "2000-01-01", "runStatus": "fixture",
                                                               "completeInputCount": len(self.works)}), encoding="utf-8")

    def output(self, name="test-run"):
        return self.root / "evaluation/frozen" / name


class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_default_is_metadata_only_and_no_training_tables(self):
        f = Fixture(self.tmp.name)
        before = {p: p.read_bytes() for p in f.corpus.rglob("*") if p.is_file()}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = prep.main(["--root", str(f.root)])
        self.assertEqual(status, 0)
        self.assertNotIn("SENTINEL", out.getvalue())
        report = json.loads(out.getvalue())
        self.assertEqual(report["selected_count"], 30)
        self.assertTrue(report["apply_allowed"])
        self.assertFalse((f.root / "evaluation/frozen").exists())
        self.assertEqual(before, {p: p.read_bytes() for p in f.corpus.rglob("*") if p.is_file()})

    def test_insufficient_refuses_without_creating_destination(self):
        f = Fixture(self.tmp.name, count=9)
        plan = prep.prepare(f.root)
        self.assertEqual(plan["report"]["selected_count"], 27)
        with self.assertRaisesRegex(prep.PrepareError, "freeze_refused"):
            prep.freeze(plan, f.output())
        self.assertFalse(f.output().parent.exists())

    def test_freeze_exact_files_shared_arms_all_comment_rows(self):
        f = Fixture(self.tmp.name)
        plan = prep.prepare(f.root)
        result = prep.freeze(plan, f.output())
        self.assertEqual(result["selected_count"], 30)
        manifest = json.loads((f.output() / "manifest.json").read_text())
        self.assertEqual(manifest["arms"]["baseline"], manifest["arms"]["enriched"])
        self.assertEqual(len(list((f.output() / "inputs").iterdir())), 60)
        for ref in manifest["inputs"]:
            for item in ref["files"].values():
                raw = (f.output() / item["path"]).read_bytes()
                self.assertEqual(prep.digest(raw), item["sha256"])
                self.assertNotIn(b"TRAIN_BODY_SENTINEL", raw)
            pack = json.loads((f.output() / ref["files"]["json"]["path"]).read_text())
            self.assertEqual(len(pack["comments"]), 3)
            self.assertEqual(pack["comments"][1]["parent_resolution"], "explicit_record_same_work")
            self.assertEqual(pack["comments"][2]["parent_resolution"], "explicit_id_without_parent_record")
            self.assertIsNone(pack["comments"][2]["text"])
            self.assertFalse(pack["media_read"])
            self.assertEqual(pack["knowledge_or_training_card_references"], [])
        with self.assertRaisesRegex(prep.PrepareError, "destination_exists"):
            prep.freeze(plan, f.output())

    def test_global_author_cap_input_order_and_metadata_reserve(self):
        f = Fixture(self.tmp.name)
        first = next(w for w in f.works if w["platform"] == "xiaohongshu" and w["split"] == "holdout")
        first["sampling_status"] = "excluded"
        first["sampling_exclusion_reason"] = "metadata_only_exclusion"
        f.add("reserve-z", "xiaohongshu", 1000, author="train-author", reserve=True)
        f.add("reserve-a", "xiaohongshu", 1001, author="train-author", reserve=True)
        f.flush()
        report = prep.prepare(f.root)["report"]
        rows = {r["work_id"]: r for r in report["candidates"]}
        self.assertEqual(report["selected_count"], 30)
        self.assertTrue(rows["reserve-z"]["selected"])
        self.assertEqual(rows["reserve-a"]["not_selected_reason"], "author_over_two")
        self.assertEqual(rows[first["work_id"]]["not_selected_reason"], "sampling_excluded")

    def test_hash_change_and_split_mismatch_refuse(self):
        f = Fixture(self.tmp.name)
        plan = prep.prepare(f.root)
        f.raw.write_bytes(b"changed source")
        with self.assertRaisesRegex(prep.PrepareError, "source_changed_during_build"):
            prep.freeze(plan, f.output())
        self.assertFalse(f.output().parent.exists())
        f.raw.write_bytes(b"SYNTHETIC FIXTURE ONLY: not an actual social export")
        f.posts[1]["split"] = "train"
        f.flush()
        report = prep.prepare(f.root)["report"]
        self.assertEqual(report["selected_count"], 29)
        self.assertFalse(report["apply_allowed"])
        self.assertIn("post_split_or_source_kind_mismatch", {r["not_selected_reason"] for r in report["candidates"]})


if __name__ == "__main__":
    unittest.main()
