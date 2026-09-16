import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "quality_summary.py"
spec = importlib.util.spec_from_file_location("quality_summary", SCRIPT)
quality_summary = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(quality_summary)


def review(**changes):
    value = {
        "task_ref": "2026-09-14/B001/T001",
        "batch_ref": "2026-09-14/B001",
        "writer": "writer-a",
        "product_line": "pocket",
        "platform": "xhs",
        "profile": "training_cw5",
        "coverage": "basic",
        "dimensions": {"quality_base": 55, "expression": 24, "teaching": 14, "total": 93},
        "issues": [],
        "revision_count": 0,
        "teaching_complete": True,
        "user_acceptance": "pending",
        "decision": "retain",
    }
    value.update(changes)
    return value


class QualitySummaryTest(unittest.TestCase):
    def test_groups_by_writer_product_platform_and_issue(self):
        first = review()
        second = review(
            task_ref="2026-09-14/B001/T002",
            writer="writer-b",
            product_line="mic",
            platform="douyin",
            coverage="deep",
            decision="revise",
            dimensions={"quality_base": 45, "expression": 18, "teaching": 10, "total": 73},
            issues=[{"code": "marketing_tone", "severity": "major"}],
            revision_count=1,
        )
        result = quality_summary.summarize([first, second])
        self.assertEqual(result["input_count"], 2)
        self.assertEqual(result["coverage"]["deep_review_coverage"]["value"], 0.5)
        self.assertEqual(result["by_writer"]["writer-b"]["revision_count"]["with_revisions"], 1)
        self.assertEqual(result["issue_codes"], {"marketing_tone": 1})

    def test_invalid_coverage_or_severity_is_rejected(self):
        with self.assertRaises(ValueError):
            quality_summary.normalize_review(review(coverage="unknown"))
        with self.assertRaises(ValueError):
            quality_summary.normalize_review(review(issues=[{"code": "ai_style", "severity": "note"}]))
        with self.assertRaises(ValueError):
            quality_summary.normalize_review(review(issues=[{"code": "made_up", "severity": "minor"}]))

    def test_cli_reads_directory_and_writes_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one").mkdir()
            (root / "one" / "quality-review.json").write_text(json.dumps(review()), encoding="utf-8")
            process = subprocess.run([sys.executable, str(SCRIPT), str(root), "--pretty"], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            output = json.loads(process.stdout)
            self.assertEqual(output["input_count"], 1)
            self.assertEqual(output["totals"]["average_score"], 93)


if __name__ == "__main__":
    unittest.main()
