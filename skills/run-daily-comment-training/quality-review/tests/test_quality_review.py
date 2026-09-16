import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "quality_review.py"
spec = importlib.util.spec_from_file_location("quality_review", SCRIPT)
quality_review = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(quality_review)


class QualityReviewTest(unittest.TestCase):
    def review(self, **changes):
        value = {
            "task_ref": "B001/T053",
            "draft_ref": "v1/comments.md",
            "draft_sha256": "a" * 64,
            "profile": "training_cw5",
            "coverage": "basic",
            "dimensions": {"quality_base": 55, "expression": 24, "teaching": 14},
            "issues": [],
            "teaching_complete": True,
            "user_acceptance": "pending",
        }
        value.update(changes)
        return value

    def test_high_score_retains(self):
        result = quality_review.score_review(self.review())
        self.assertEqual(result["score"]["total"], 93)
        self.assertEqual(result["quality_score"], 93)
        self.assertEqual(result["quality_issue_codes"], [])
        self.assertEqual(result["decision"], "retain")

    def test_blocker_caps_and_blocks_even_with_perfect_dimensions(self):
        issue = {"issue_id": "QC-001", "code": "model_mismatch", "severity": "blocker", "observation": "型号写错", "action": "按证据改写"}
        result = quality_review.score_review(self.review(dimensions={"quality_base": 60, "expression": 25, "teaching": 15}, issues=[issue]))
        self.assertEqual(result["score"]["total"], 59)
        self.assertEqual(result["decision"], "block")

    def test_major_caps_and_low_score_revises(self):
        issue = {"issue_id": "QC-001", "code": "marketing_tone", "severity": "major", "observation": "营销腔", "action": "改为消费者表达"}
        result = quality_review.score_review(self.review(issues=[issue]))
        self.assertEqual(result["score"]["total"], 79)
        self.assertEqual(result["decision"], "revise")

    def test_teaching_incomplete_requires_revision(self):
        result = quality_review.score_review(self.review(teaching_complete=False))
        self.assertEqual(result["decision"], "revise")

    def test_invalid_issue_code_and_duplicate_id_are_rejected(self):
        issue = {"issue_id": "QC-001", "code": "made_up", "severity": "minor", "observation": "x", "action": "y"}
        with self.assertRaises(quality_review.ReviewError):
            quality_review.score_review(self.review(issues=[issue]))
        issue["code"] = "ai_style"
        with self.assertRaises(quality_review.ReviewError):
            quality_review.score_review(self.review(issues=[issue, dict(issue)]))

    def test_stale_input_decision_is_rejected(self):
        with self.assertRaisesRegex(quality_review.ReviewError, "decision 与规则不一致"):
            quality_review.score_review(self.review(decision="revise"))

    def test_cli_outputs_json_and_markdown_and_can_check_draft_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "comments.md"
            draft.write_text("draft", encoding="utf-8")
            review = self.review(draft_sha256=hashlib.sha256(b"draft").hexdigest())
            source = root / "review.json"
            output = root / "quality-review.json"
            markdown = root / "quality-review.md"
            source.write_text(json.dumps(review), encoding="utf-8")
            process = subprocess.run([sys.executable, str(SCRIPT), str(source), "--draft", str(draft), "--output-json", str(output), "--output-md", str(markdown)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(output.read_text())["decision"], "retain")
            self.assertIn("文案质检报告", markdown.read_text())


if __name__ == "__main__":
    unittest.main()
