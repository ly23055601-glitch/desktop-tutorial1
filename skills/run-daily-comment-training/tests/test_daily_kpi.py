"""Offline counting/contract tests. All artifacts stay inside TemporaryDirectory."""

import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "daily_kpi.py"
SPEC = importlib.util.spec_from_file_location("daily_kpi", SCRIPT)
kpi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kpi)


class DailyKpiTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def batch(self, day="2026-09-07", batch="B001"):
        return {"schema_version": 1, "date": day, "batch_id": batch, "started_at": f"{day}T10:00:00+08:00", "inputs": [], "sources": [], "tasks": [], "external_blocks": []}

    def folder(self, batch):
        folder = self.root / batch["date"] / batch["batch_id"]
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def file(self, batch, relative):
        path = self.folder(batch) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("offline fixture; not real evidence", encoding="utf-8")
        return relative

    def delivery(self, batch, task_id, version=1, minute=10, reviewed=True, mains=3, replies=2):
        prefix = f"{task_id}/v{version}"
        result = {"delivered_at": f"{batch['date']}T10:{minute:02d}:00+08:00", "draft_ref": self.file(batch, f"{prefix}/comments.md"), "training_state_ref": self.file(batch, f"{prefix}/training-state.json"), "main_comments": mains, "replies": replies, "review": {key: reviewed for key in kpi.REVIEW_KEYS}, "independent_review_ref": None}
        result["review"]["self_check_ref"] = self.file(batch, f"{prefix}/review.md")
        if version > 1:
            result["feedback_ids"] = []
        return result

    def add_task(self, batch, code="op", material="douyin:123", delivered=True, required=True):
        task_id = f"T{len(batch['tasks']) + 1:03d}"
        task = {"id": task_id, "product_code": code, "material_id": material, "status": "delivered" if delivered else "pending", "conclusion": None, "first_delivery": self.delivery(batch, task_id) if delivered else None, "revisions": [], "user_feedback": [], "hard_errors": []}
        batch["tasks"].append(task)
        ref = f"{batch['date']}/{batch['batch_id']}/{task_id}"
        batch["inputs"].append({"original_index": str(len(batch["inputs"]) + 1), "product_code": code, "material_id": material, "task_ref": ref})
        if not any(source["material_id"] == material for source in batch["sources"]):
            batch["sources"].append({"material_id": material, "url": "https://example.invalid/post?xsec_token=SECRET_SENTINEL", "read_required": required, "status": "qualified" if required else "provided", "evidence_ref": self.file(batch, f"evidence/{len(batch['sources'])}.json"), "verified_at": f"{batch['date']}T10:05:00+08:00" if required else None, "reason": None})
        return task

    def feedback(self, batch, task, outcome, minute=15, target="first_draft", revision_number=None):
        event = {"id": f"F{len(task['user_feedback']) + 1:03d}", "at": f"{batch['date']}T10:{minute:02d}:00+08:00", "target": target, "outcome": outcome, "source_ref": "user-message:fixture", "note": "fictional test feedback"}
        if revision_number is not None:
            event["revision_number"] = revision_number
        task["user_feedback"].append(event)
        return event

    def save(self, batch):
        path = self.folder(batch) / "ledger.json"
        path.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def test_code_link_input_defaults_and_no_user_acceptance_from_checks(self):
        batch = self.batch()
        task = self.add_task(batch)
        task["first_delivery"]["independent_review_ref"] = self.file(batch, "T001/v1/independent-review.md")
        self.save(batch)
        data = kpi.report(self.root)["daily"]
        self.assertEqual((data["input_tasks"], data["delivered_tasks"]), (1, 1))
        self.assertEqual(data["semantic_review_coverage"]["value"], 1)
        self.assertEqual(data["independent_review_coverage"]["value"], 1)
        self.assertIsNone(data["first_draft_acceptance"]["value"])
        self.assertEqual(data["pending_first_draft_review"], 1)

    def test_mixed_products_short_long_link_aliases_share_one_read(self):
        batch = self.batch()
        self.add_task(batch, "op")
        self.add_task(batch, "dm")
        for original in list(batch["inputs"]):
            alias = copy.deepcopy(original)
            alias["original_index"] = str(len(batch["inputs"]) + 1)
            batch["inputs"].append(alias)
        self.save(batch)
        result = kpi.report(self.root)
        self.assertEqual(result["daily"]["input_tasks"], 2)
        self.assertEqual(result["daily"]["reading_success"], {"numerator": 1, "denominator": 1, "value": 1})
        self.assertEqual(result["daily"]["production"]["main_comments"], 6)
        self.assertNotIn("SECRET_SENTINEL", json.dumps(result))

    def test_partial_read_failure_and_supplied_material_denominators(self):
        batch = self.batch()
        self.add_task(batch)
        blocked = self.add_task(batch, material="xhs:456", delivered=False)
        blocked.update(status="blocked", conclusion="原帖受访问限制，未取得证据")
        batch["sources"][-1].update(status="blocked", evidence_ref=None, verified_at=None, reason="访问限制")
        self.add_task(batch, material="provided:notes", required=False)
        self.save(batch)
        data = kpi.report(self.root)["daily"]
        self.assertEqual(data["input_closure"]["value"], 1)
        self.assertEqual(data["draft_completion"]["value"], 2 / 3)
        self.assertEqual(data["reading_success"]["value"], 1 / 2)
        self.assertEqual(len(data["blockers"]), 1)

    def test_delivery_with_only_blocked_or_pending_source_is_rejected(self):
        batch = self.batch()
        self.add_task(batch, material="xhs:456")
        for status in ("blocked", "pending"):
            with self.subTest(source_status=status):
                batch["sources"][0].update(status=status, evidence_ref=None, verified_at=None, reason="访问限制" if status == "blocked" else None)
                self.save(batch)
                with self.assertRaisesRegex(ValueError, "2026-09-07/B001/T001.*已登记实交但无当日可用来源"):
                    kpi.report(self.root)
                process = subprocess.run([sys.executable, str(SCRIPT), str(self.root), "--json"], capture_output=True, text=True)
                self.assertEqual(process.returncode, 2)
                self.assertIn("xhs:456", process.stderr)
                self.assertEqual(process.stdout, "")

    def test_supplied_replacement_allows_delivery_without_hiding_read_failure(self):
        batch = self.batch()
        self.add_task(batch, material="xhs:456")
        batch["sources"][0].update(status="blocked", evidence_ref=None, verified_at=None, reason="访问限制")
        batch["sources"].append({"material_id": "xhs:456", "read_required": False, "status": "provided", "evidence_ref": self.file(batch, "evidence/user-provided-material.md"), "verified_at": None, "reason": "用户提供充足替代材料"})
        self.save(batch)
        data = kpi.report(self.root)["daily"]
        self.assertEqual(data["draft_completion"], {"numerator": 1, "denominator": 1, "value": 1})
        self.assertEqual(data["reading_success"], {"numerator": 0, "denominator": 1, "value": 0})
        self.assertEqual(data["production"]["main_comments"], 3)

    def test_append_batch_and_revisions_do_not_inflate_new_production(self):
        first = self.batch()
        task = self.add_task(first)
        feedback = self.feedback(first, task, "changes_requested")
        revision = self.delivery(first, task["id"], version=2, minute=20, reviewed=False, mains=4, replies=5)
        revision["feedback_ids"] = [feedback["id"]]
        task["revisions"].append(revision)
        self.save(first)
        second = self.batch(batch="B002")
        second["inputs"].append(copy.deepcopy(first["inputs"][0]))
        self.add_task(second, "dm", "douyin:new")
        self.save(second)
        data = kpi.report(self.root)["daily"]
        self.assertEqual(data["input_tasks"], 2)
        self.assertEqual(data["production"], {"main_comments": 6, "replies": 4})
        self.assertEqual(data["current_production"], {"main_comments": 7, "replies": 7})
        self.assertEqual(data["user_feedback_revision_rounds"], 1)
        self.assertEqual(data["semantic_review_coverage"]["value"], 1 / 2)

    def test_partial_acceptance_keeps_first_rejection_after_revision_passes(self):
        batch = self.batch()
        first = self.add_task(batch)
        second = self.add_task(batch, "dm")
        self.add_task(batch, "ow")
        self.feedback(batch, first, "accepted")
        initial = self.feedback(batch, second, "changes_requested")
        revision = self.delivery(batch, second["id"], version=2, minute=20)
        revision["feedback_ids"] = [initial["id"]]
        second["revisions"].append(revision)
        self.feedback(batch, second, "accepted", minute=30, target="revision", revision_number=1)
        self.save(batch)
        data = kpi.report(self.root)["daily"]
        self.assertEqual(data["first_draft_acceptance"]["value"], 1 / 2)
        self.assertEqual(data["first_draft_review_coverage"]["value"], 2 / 3)
        self.assertEqual(data["current_user_acceptance"]["accepted"], 2)
        self.assertEqual(data["pending_first_draft_review"], 1)

    def test_neutral_review_then_unchanged_acceptance_counts(self):
        batch = self.batch()
        task = self.add_task(batch)
        self.feedback(batch, task, "reviewed", minute=15)
        self.feedback(batch, task, "accepted", minute=20)
        self.save(batch)
        self.assertEqual(kpi.report(self.root)["daily"]["first_draft_acceptance"]["value"], 1)

    def test_first_decision_cannot_be_replaced_by_later_first_target_acceptance(self):
        batch = self.batch()
        task = self.add_task(batch)
        self.feedback(batch, task, "changes_requested", minute=15)
        self.feedback(batch, task, "accepted", minute=20)
        self.save(batch)
        self.assertEqual(kpi.report(self.root)["daily"]["first_draft_acceptance"]["value"], 0)

    def test_old_task_revision_keeps_original_execution_day(self):
        first = self.batch()
        task = self.add_task(first)
        revision = self.delivery(first, task["id"], version=2, minute=20)
        revision["delivered_at"] = "2026-09-08T10:20:00+08:00"
        task["revisions"].append(revision)
        self.save(first)
        result = kpi.report(self.root)
        self.assertEqual(result["execution_days"], ["2026-09-07"])
        self.assertEqual(len(result["recent_execution_days"][0]["drafts"]), 2)
        second = self.batch(day="2026-09-08")
        self.add_task(second)
        second["sources"][0].update(status="reused", evidence_ref=str(self.folder(first) / first["sources"][0]["evidence_ref"]), verified_at=first["sources"][0]["verified_at"])
        self.save(second)
        result = kpi.report(self.root)
        self.assertEqual(len(result["execution_days"]), 2)
        self.assertEqual(result["daily"]["input_tasks"], 1)

    def test_empty_root_and_empty_batch_do_not_create_baseline_day(self):
        for root in (self.root, self.root / "missing"):
            result = kpi.report(root)
            self.assertEqual(result["execution_days"], [])
            self.assertIsNone(result["daily"]["input_closure"]["value"])
        self.save(self.batch())
        self.assertEqual(kpi.report(self.root)["execution_days"], [])

    def test_seven_execution_days_ignore_gaps_and_locate_recent_seven(self):
        days = ["2026-09-01", "2026-09-02", "2026-09-04", "2026-09-05", "2026-09-07", "2026-09-08", "2026-09-10", "2026-09-11"]
        for day in days:
            batch = self.batch(day=day)
            self.add_task(batch)
            self.save(batch)
        self.save(self.batch(day="2026-09-03"))
        result = kpi.report(self.root)
        self.assertEqual(result["first_seven_baseline"]["days"], days[:7])
        self.assertTrue(result["first_seven_baseline"]["ready"])
        self.assertEqual([item["date"] for item in result["recent_execution_days"]], days[-7:])
        self.assertEqual(result["first_seven_baseline"]["metrics"]["input_tasks"], 7)
        before = kpi.report(self.root, "2026-09-08")
        self.assertFalse(before["first_seven_baseline"]["ready"])
        self.assertEqual(len(before["execution_days"]), 6)

    def test_real_wall_time_block_intervals_and_hard_error_history(self):
        batch = self.batch()
        task = self.add_task(batch)
        task["hard_errors"].append({"id": "E001", "detected_at": "2026-09-07T10:06:00+08:00", "kind": "product_fact", "stage": "internal", "detail": "test model mismatch", "resolved_at": "2026-09-07T10:07:00+08:00"})
        batch["external_blocks"] = [{"started_at": "2026-09-07T10:01:00+08:00", "ended_at": "2026-09-07T10:03:00+08:00", "reason": "test wait"}, {"started_at": "2026-09-07T10:02:00+08:00", "ended_at": "2026-09-07T10:04:00+08:00", "reason": "overlapping test wait"}]
        self.save(batch)
        data = kpi.report(self.root)["daily"]
        self.assertEqual(data["timings"][0]["wall_seconds_to_first_delivery"], 600)
        self.assertEqual(data["timings"][0]["closed_external_block_seconds"], 180)
        self.assertEqual(data["hard_errors"], {"total": 1, "internal": 1, "delivered": 0, "unresolved": 0})

    def test_pending_delivery_has_null_time_and_no_invented_block_duration(self):
        batch = self.batch()
        self.add_task(batch, delivered=False)
        self.save(batch)
        timing = kpi.report(self.root)["daily"]["timings"][0]
        self.assertIsNone(timing["wall_seconds_to_first_delivery"])
        self.assertIsNone(timing["closed_external_block_seconds"])

    def test_duplicate_task_definition_rejected_instead_of_counted_twice(self):
        batch = self.batch()
        self.add_task(batch)
        self.add_task(batch)
        self.save(batch)
        with self.assertRaisesRegex(ValueError, "重复任务定义"):
            kpi.report(self.root)

    def test_versions_cannot_reuse_first_draft_or_state_even_by_symlink(self):
        batch = self.batch()
        task = self.add_task(batch)
        revision = self.delivery(batch, task["id"], version=2, minute=20)
        for key in ("draft_ref", "training_state_ref"):
            for symlink in (False, True):
                with self.subTest(key=key, symlink=symlink):
                    variant = copy.deepcopy(revision)
                    original = task["first_delivery"][key]
                    if symlink:
                        alias = self.folder(batch) / f"alias-{key}"
                        alias.symlink_to(self.folder(batch) / original)
                        variant[key] = alias.name
                    else:
                        variant[key] = original
                    task["revisions"] = [variant]
                    self.save(batch)
                    with self.assertRaisesRegex(ValueError, "不同交付版本不能复用"):
                        kpi.report(self.root)

    def test_missing_evidence_and_naive_time_are_not_silent_success(self):
        batch = self.batch()
        self.add_task(batch)
        batch["sources"][0]["evidence_ref"] = "missing.json"
        self.save(batch)
        with self.assertRaisesRegex(ValueError, "引用文件不存在"):
            kpi.report(self.root)
        batch["sources"][0]["evidence_ref"] = self.file(batch, "replacement.json")
        batch["started_at"] = "2026-09-07T10:00:00"
        self.save(batch)
        with self.assertRaisesRegex(ValueError, "缺少时区"):
            kpi.report(self.root)

    def test_cli_is_read_only_and_returns_valid_json(self):
        batch = self.batch()
        self.add_task(batch)
        self.save(batch)
        before = {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        process = subprocess.run([sys.executable, str(SCRIPT), str(self.root), "--date", batch["date"], "--json"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(process.stdout)["selected_date"], batch["date"])
        after = {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        text_output = io.StringIO()
        with contextlib.redirect_stdout(text_output):
            kpi.print_text(kpi.report(self.root))
        self.assertIn("暂无数据", text_output.getvalue())

    def test_output_groups_size_boundaries(self):
        for count in (0, 1, 10, 11, 20, 23, 25):
            with self.subTest(input_count=count):
                batch = self.batch()
                for number in range(count):
                    self.add_task(batch, material=f"douyin:{number}")
                self.save(batch)
                result = kpi.report(self.root, batch["date"])
                groups = result["output_groups"]
                self.assertEqual([group["input_count"] for group in groups], [min(10, count - start) for start in range(0, count, 10)])
                self.assertEqual([group["group_ref"].rsplit("/", 1)[1] for group in groups], [f"G{number + 1:03d}" for number in range((count + 9) // 10)])
                self.assertEqual([(group["input_start"], group["input_end"]) for group in groups], [(start + 1, min(start + 10, count)) for start in range(0, count, 10)])
                self.assertEqual([item["position"] for group in groups for item in group["items"]], list(range(1, count + 1)))
                self.assertEqual(result["daily"]["input_tasks"], count)
                self.assertEqual(result["daily"]["reading_success"]["denominator"], count)

    def test_output_groups_keep_mixed_product_order_and_deduplicate_reads(self):
        batch = self.batch()
        codes = ["op", "dm", "ow", "oq", "om", "dm", "op", "oq", "ow", "om", "dm"]
        for number, code in enumerate(codes):
            self.add_task(batch, code=code, material="douyin:shared" if number in (0, 10) else f"douyin:{number}")
            batch["inputs"][-1]["original_index"] = f"用户序号{number % 5 + 1}"
        self.save(batch)
        result = kpi.report(self.root)
        items = [item for group in result["output_groups"] for item in group["items"]]
        self.assertEqual([item["product_code"] for item in items], codes)
        self.assertEqual([item["original_index"] for item in items], [entry["original_index"] for entry in batch["inputs"]])
        self.assertEqual(result["output_groups"][1]["items"][0]["position"], 11)
        self.assertEqual(result["daily"]["input_tasks"], 11)
        self.assertEqual(result["daily"]["reading_success"], {"numerator": 10, "denominator": 10, "value": 1})

    def test_output_groups_failures_and_duplicates_keep_their_slots(self):
        batch = self.batch()
        for number in range(10):
            self.add_task(batch, material=f"douyin:{number}", delivered=number != 9)
        batch["tasks"][9].update(status="blocked", conclusion="读取受限")
        batch["sources"][9].update(status="blocked", evidence_ref=None, verified_at=None, reason="读取受限")
        for original in (batch["inputs"][0], batch["inputs"][9]):
            alias = copy.deepcopy(original)
            alias["original_index"] = str(len(batch["inputs"]) + 1)
            alias["url"] = "https://example.invalid/?xsec_token=SECRET_SENTINEL"
            batch["inputs"].append(alias)
        self.save(batch)
        result = kpi.report(self.root)
        groups = result["output_groups"]
        self.assertEqual([group["input_count"] for group in groups], [10, 2])
        self.assertEqual(groups[0]["items"][9]["task_status"], "blocked")
        self.assertEqual(groups[1]["items"][0]["first_occurrence"], {"group_ref": groups[0]["group_ref"], "position": 1})
        self.assertEqual(groups[1]["items"][1]["first_occurrence"], {"group_ref": groups[0]["group_ref"], "position": 10})
        self.assertNotIn("draft_ref", groups[1]["items"][1])
        self.assertEqual(result["daily"]["input_tasks"], 10)
        self.assertEqual(result["daily"]["reading_success"]["value"], 9 / 10)
        self.assertEqual(result["daily"]["production"]["main_comments"], 27)
        self.assertNotIn("SECRET_SENTINEL", json.dumps(result))

    def test_new_batch_starts_new_group_without_filling_prior_tail(self):
        first = self.batch()
        for number in range(11):
            self.add_task(first, material=f"douyin:{number}")
        self.save(first)
        before = kpi.report(self.root)["output_groups"]
        second = self.batch(batch="B002")
        second["inputs"].append(copy.deepcopy(first["inputs"][0]))
        self.add_task(second, material="douyin:new1")
        self.add_task(second, material="douyin:new2")
        self.save(second)
        result = kpi.report(self.root)
        self.assertEqual(result["output_groups"][:2], before)
        self.assertEqual([group["input_count"] for group in result["output_groups"]], [10, 1, 3])
        last = result["output_groups"][2]
        self.assertEqual(last["group_ref"], "2026-09-07/B002/G001")
        self.assertEqual(last["items"][0]["first_occurrence"], {"group_ref": "2026-09-07/B001/G001", "position": 1})
        self.assertEqual(result["daily"]["input_tasks"], 13)
        self.assertEqual(result["daily"]["reading_success"]["denominator"], 13)

    def test_duplicate_only_request_can_show_groups_without_new_execution_day(self):
        first = self.batch()
        task = self.add_task(first)
        revision = self.delivery(first, task["id"], version=2, minute=20)
        task["revisions"].append(revision)
        self.save(first)
        second = self.batch(day="2026-09-08")
        second["inputs"].append(copy.deepcopy(first["inputs"][0]))
        self.save(second)
        default = kpi.report(self.root)
        self.assertEqual(default["selected_date"], "2026-09-07")
        selected = kpi.report(self.root, "2026-09-08")
        self.assertEqual(selected["execution_days"], ["2026-09-07"])
        self.assertEqual(selected["daily"]["input_tasks"], 0)
        self.assertEqual(selected["daily"]["production"]["main_comments"], 0)
        self.assertEqual(len(selected["output_groups"]), 1)
        item = selected["output_groups"][0]["items"][0]
        self.assertEqual(item["task_ref"], "2026-09-07/B001/T001")
        self.assertEqual(item["draft_ref"], str((self.folder(first) / revision["draft_ref"]).resolve()))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            kpi.print_text(selected)
        self.assertIn("输出组 2026-09-08/B001/G001：输入位置 1–1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
