"""Contract tests for the canonical batch-summary entry point."""

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "quality_summary.py"
SPEC = importlib.util.spec_from_file_location("quality_summary_canonical", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def review(task, coverage="basic", revisions=0):
    return {
        "task_ref": task,
        "profile": "training_cw5",
        "coverage": coverage,
        "dimensions": {"quality_base": 50, "expression": 20, "teaching": 10, "total": 80},
        "issues": [], "revision_count": revisions, "decision": "revise",
        "teaching_complete": True, "user_acceptance": "pending",
    }


class QualitySummaryCanonicalTest(unittest.TestCase):
    def test_compact_task_ref_derives_batch_and_counts_deep(self):
        result = MODULE.summarize([review("B001/T001", "basic"), review("B001/T002", "risk_deep", 1)])
        self.assertEqual(result["by_batch"]["B001"]["count"], 2)
        self.assertEqual(result["coverage"]["deep_review_coverage"]["numerator"], 1)
        self.assertEqual(result["totals"]["revision_count"]["with_revisions"], 1)

    def test_empty_summary_preserves_null_ratio(self):
        result = MODULE.summarize([])
        self.assertEqual(result["quality_profile"], "training_cw5")
        self.assertIsNone(result["coverage"]["deep_review_coverage"]["value"])


if __name__ == "__main__":
    unittest.main()
