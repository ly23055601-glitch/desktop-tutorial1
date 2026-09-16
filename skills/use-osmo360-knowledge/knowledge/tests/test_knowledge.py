import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("knowledge", Path(__file__).resolve().parents[1] / "scripts" / "knowledge.py")
knowledge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(knowledge)


def card(identifier, model, status="verified"):
    return {"id": identifier, "kind": "official_fact", "models": [model], "topic": "隐形自拍杆", "statement": "自拍杆需与相机保持同一直线。", "conditions": ["全景模式"], "limitations": ["不能从单镜头拍摄推断隐形效果"], "region": "全球", "firmware": None, "software": None, "sources": [{"source_id": "S-TEST", "locator": "FAQ 自拍杆"}], "checked_at": "2026-09-06", "status": status}


def source():
    return {"id": "S-TEST", "title": "FAQ", "url": "https://www.dji.com/360/faq", "publisher": "DJI", "language": "en", "region": "全球", "models": ["osmo_360"], "checked_at": "2026-09-06", "status": "read", "locators": ["自拍杆"], "notes": "实际读取相关小节"}


class SearchTests(unittest.TestCase):
    def test_model_filter_prevents_generation_leak(self):
        cards = [card("D1-001", "osmo_360"), card("D2-001", "osmo_360_ii")]
        result = knowledge.search(cards, "如何隐形自拍杆", "osmo_360_ii")
        self.assertEqual([f["id"] for f in result], ["D2-001"])

    def test_uncertain_facts_never_become_search_answers(self):
        cards = [card("D1-001", "osmo_360", "pending"), card("D1-002", "osmo_360", "conflict")]
        self.assertEqual(knowledge.search(cards, "自拍杆"), [])

    def test_no_match_is_not_an_arbitrary_answer(self):
        self.assertEqual(knowledge.search([card("D1-001", "osmo_360")], "卫星电话"), [])

    def test_result_preserves_conditions_and_sources(self):
        original = card("D1-001", "osmo_360")
        self.assertEqual(knowledge.search([original], "单镜头")[0], original)

    def test_exact_uncertain_id_never_falls_back_to_other_models(self):
        cards = [card("D1-005", "osmo_360"), card("IX5-005", "insta360_x5", "conflict")]
        self.assertEqual(knowledge.search(cards, "ix5-005"), [])
        self.assertEqual([f["id"] for f in knowledge.related_issues(cards, "ix5-005")], ["IX5-005"])
        self.assertEqual(knowledge.search(cards, "D2-005"), [])

    def test_explicit_model_in_query_filters_results(self):
        cards = [card("D1-001", "osmo_360"), card("IX5-001", "insta360_x5")]
        self.assertEqual([f["id"] for f in knowledge.search(cards, "X5 隐形自拍杆")], ["IX5-001"])

    def test_unresolved_matches_are_separate_from_factual_answers(self):
        cards = [card("D1-001", "osmo_360"), card("D1-002", "osmo_360", "pending")]
        self.assertEqual([f["id"] for f in knowledge.search(cards, "隐形自拍杆")], ["D1-001"])
        self.assertEqual([f["id"] for f in knowledge.related_issues(cards, "隐形自拍杆")], ["D1-002"])


class RealKnowledgeSearchTests(unittest.TestCase):
    """用当前知识卡验证完整问句，避免简化测试漏掉型号词造成的排序干扰。"""

    @classmethod
    def setUpClass(cls):
        cls.facts, _, errors = knowledge.load(knowledge.ROOT)
        if errors:
            raise AssertionError(errors)

    def test_named_model_does_not_hide_follow_export_answer(self):
        expected = knowledge.search(self.facts, "跟随 导出", "osmo_360_ii")
        actual = knowledge.search(self.facts, "Osmo 360 II 跟随 导出")
        self.assertEqual(actual, expected)
        self.assertIn("D2-024", [f["id"] for f in actual])

    def test_second_generation_aliases_never_include_first_generation(self):
        for alias in ("Osmo 360 二代", "大疆360二代", "大疆 Osmo 360 第二代", "osmo_360_ii", "Osmo 360 Ⅱ"):
            with self.subTest(alias=alias):
                self.assertEqual(knowledge.query_models(alias), {"osmo_360_ii"})
                actual = knowledge.search(self.facts, alias + " 主角跟随")
                self.assertIn("D2-024", [f["id"] for f in actual])
                self.assertTrue(all(f["models"] == ["osmo_360_ii"] for f in actual))

    def test_unknown_topic_with_named_model_has_no_factual_answers(self):
        for alias in ("Osmo 360", "Osmo 360 II", "Osmo 360 二代", "大疆360二代", "Insta360 X5", "Insta360 X6", "GoPro MAX2"):
            for question in (" 卫星电话", "支持卫星电话吗"):
                with self.subTest(query=alias + question):
                    self.assertEqual(knowledge.search(self.facts, alias + question), [])

    def test_named_model_keeps_relevant_gap_separate(self):
        actual = knowledge.related_issues(self.facts, "Osmo 360 II 跟随 导出")
        self.assertEqual([f["id"] for f in actual], ["D2-051"])
        answers = knowledge.search(self.facts, "X5 8K 续航")
        self.assertNotIn("IX5-005", [f["id"] for f in answers])
        self.assertIn("IX5-005", [f["id"] for f in knowledge.related_issues(self.facts, "X5 8K 续航")])

    def test_exact_card_id_keeps_status_and_model_boundaries(self):
        self.assertEqual([f["id"] for f in knowledge.search(self.facts, "d2-024")], ["D2-024"])
        self.assertEqual(knowledge.search(self.facts, "D2-024", "osmo_360"), [])
        self.assertEqual(knowledge.search(self.facts, "IX5-005"), [])
        self.assertEqual([f["id"] for f in knowledge.related_issues(self.facts, "IX5-005")], ["IX5-005"])
        self.assertEqual(knowledge.search(self.facts, "D2-999"), [])

    def test_explicit_model_parameter_still_takes_precedence(self):
        expected = knowledge.search(self.facts, "隐形自拍杆", "osmo_360")
        actual = knowledge.search(self.facts, "Osmo 360 II 隐形自拍杆", "osmo_360")
        self.assertEqual(actual, expected)
        self.assertTrue(all(f["models"] == ["osmo_360"] for f in actual))

    def test_comparison_preserves_both_explicit_generations(self):
        query = "Osmo 360 和大疆360二代 隐形自拍杆"
        self.assertEqual(knowledge.query_models(query), {"osmo_360", "osmo_360_ii"})
        actual = knowledge.search(self.facts, query)
        self.assertTrue({"D1-008", "D2-018"}.issubset({f["id"] for f in actual}))
        self.assertTrue(all(set(f["models"]).issubset({"osmo_360", "osmo_360_ii"}) for f in actual))


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def issues(self, facts=None, sources=None):
        return knowledge.audit(self.root, facts if facts is not None else [card("D1-001", "osmo_360")], sources if sources is not None else [source()])["errors"]

    def test_verified_fact_cannot_use_unread_or_wrong_model_source(self):
        s = source()
        s.update(status="unread", models=["osmo_360_ii"])
        errors = self.issues(sources=[s])
        self.assertTrue(any("未读取来源" in e for e in errors))
        self.assertTrue(any("型号不符" in e for e in errors))

    def test_duplicate_and_missing_source_are_reported(self):
        f = card("D1-001", "osmo_360")
        errors = self.issues(facts=[f, copy.deepcopy(f)], sources=[])
        self.assertTrue(any("重复 ID" in e for e in errors))
        self.assertTrue(any("未登记来源" in e for e in errors))

    def test_broken_link_and_unknown_fact_are_reported(self):
        (self.root / "example.md").write_text("[D2-999](missing.md)", encoding="utf-8")
        errors = self.issues()
        self.assertTrue(any("未知知识卡" in e for e in errors))
        self.assertTrue(any("本地链接不存在" in e for e in errors))

    def test_invalid_json_is_not_silently_ignored(self):
        (self.root / "products").mkdir()
        (self.root / "products" / "test.facts.jsonl").write_text("{broken}\n", encoding="utf-8")
        facts, sources, errors = knowledge.load(self.root)
        self.assertEqual(facts, [])
        self.assertEqual(len(errors), 1)

    def test_generated_catalog_retains_conditions_and_source(self):
        (self.root / "sources").mkdir()
        knowledge.build(self.root, [card("D1-001", "osmo_360")], [source()])
        body = (self.root / "CARDS.md").read_text(encoding="utf-8")
        for expected in ("### D1-001", "全景模式", "不能从单镜头", "https://www.dji.com/360/faq", "FAQ 自拍杆"):
            self.assertIn(expected, body)


if __name__ == "__main__":
    unittest.main()
