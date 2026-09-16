from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import test_check_comment_homogeneity as legacy

CHECKER = legacy.CHECKER
ROOT = legacy.SKILL_ROOT


class LH13ProjectContractTests(unittest.TestCase):
    run_draft = legacy.LH5SemanticTests.run_draft
    allocation = staticmethod(legacy.LH7DeliveryTests.allocation)
    codes = staticmethod(legacy.LH7DeliveryTests.codes)
    assert_clean = legacy.LH9DialogueTests.assert_clean

    def fixture(self, text="Pocket4P这层白纱的拍法我想试试", *, model="pocket_4p", counts=(0, 0)):
        draft, state = legacy.LH12FlexibleDeliveryTests().fixture(counts)
        draft = draft.replace("白纱只遮一半脸那格最喜欢", text)
        state["rule_version"] = CHECKER.LH13_RULE_VERSION
        allocation = self.allocation(state)
        allocation["model_status"].update(level="M1", evidence_type="author_claim", claimed_model=model, confirmed_model="unknown", evidence="作者标题标注该型号")
        allocation["groups"][0].update(target_model=model, product_connection="这层白纱触发具体人像尝试兴趣")
        state["qa"]["semantic_review"]["seeding_review"] = [{"id": allocation["id"], "verdict": "passed", "reason": "主评从白纱画面产生对Pocket拍摄人像的具体兴趣", "interest_entries": [{"group": 1, "exact_copy_quote": text, "interest": "想尝试这种人像表达"}]}]
        return draft, state

    def result(self, draft, state, *, rehash=True):
        if rehash:
            state["draft_sha256"] = hashlib.sha256(draft.encode()).hexdigest()
        return self.run_draft(draft, state)

    def fact(self, claim_id, quote, model="pocket_4p"):
        claim = legacy.REGISTRY["lh13"]["claims"].get(claim_id, legacy.REGISTRY["claims"].get(claim_id))
        return {"claim_id": claim_id, "target_model": model, "source_urls": claim["official_sources"], "checked_at": date.today().isoformat(), "exact_copy_quote": quote}

    def register(self, state, fact, group=1):
        self.allocation(state)["groups"][group-1]["product_facts"] = [fact]

    def test_lh13_flexible_counts_and_visual_supplements(self):
        for counts in [(0, 0), (0, 1, 3), (0, 1, 2, 4)]:
            with self.subTest(counts=counts):
                draft, state = self.fixture(counts=counts)
                result = self.result(draft, state)
                self.assert_clean(result)
                self.assertEqual(result["seeding_review"]["records_passed"], 1)

    def test_lh13_accepts_observed_and_personal_need_official_facts_without_MF_inflation(self):
        text = "想试试4p那个3倍镜头，就拍这种半身"
        for mode in ["observed", "personal_need"]:
            draft, state = self.fixture(text)
            group = self.allocation(state)["groups"][0]
            if mode == "personal_need":
                group.update(claim_mode=mode, target_s_level="S1", actual_s_level="S1", need_connection="半身画面触发镜头使用兴趣")
            self.register(state, self.fact("4p_3x_physical_lens", text))
            before = copy.deepcopy(self.allocation(state))
            self.assert_clean(self.result(draft, state))
            self.assertEqual(self.allocation(state)["model_status"], before["model_status"])
            self.assertEqual(self.allocation(state)["feature_use"], before["feature_use"])

    def test_lh13_zoom_key_and_auto_rotation_require_independent_facts(self):
        cases = [
            ("4p那个变焦键我还挺喜欢的，按一下换远近，拍着拍着不用戳屏幕", "4p_zoom_button", "pocket_4p"),
            ("原来Pocket4能自己转镜头，我还在脑补摄影师拧来拧去", "p4_spinshot_auto", "pocket_4"),
        ]
        for text, cid, model in cases:
            with self.subTest(cid=cid):
                draft, state = self.fixture(text, model=model)
                self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))
                self.register(state, self.fact(cid, text, model))
                self.assert_clean(self.result(draft, state))

    def test_lh13_tracking_and_zoom_questions_do_not_need_claim_records(self):
        cases = [
            ("Pocket4架着开跟随，能自己拍瀑布前回头这段吗？想把自己也拍进去", "pocket_4"),
            ("隔着白纱这段想抄作业，Pocket4P用的1倍还是3倍呀", "pocket_4p"),
            ("Pocket4能自动旋转吗？想看看操作", "pocket_4"),
        ]
        for text, model in cases:
            draft, state = self.fixture(text, model=model)
            self.assert_clean(self.result(draft, state))

    def test_lh13_factual_clause_after_question_still_requires_record(self):
        text = "Pocket4能开跟随吗？这台还能自动旋转"
        draft, state = self.fixture(text, model="pocket_4")
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))

    def test_lh13_rhetorical_question_is_not_exempt(self):
        draft, state = self.fixture("Pocket4不就是能自动旋转吗", model="pocket_4")
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))

    def test_lh13_quote_only_covers_its_own_fact(self):
        text = "Pocket4能自动旋转，这台也能拍8K"
        draft, state = self.fixture(text, model="pocket_4")
        self.register(state, self.fact("p4_spinshot_auto", "Pocket4能自动旋转", "pocket_4"))
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))

    def test_lh13_cannot_launder_unverified_fact_with_different_claim(self):
        text = "Pocket4能拍8K"
        draft, state = self.fixture(text, model="pocket_4")
        self.register(state, self.fact("p4_spinshot_auto", text, "pocket_4"))
        self.assertIn("E_PRODUCT_FACT_CLAIM_MISMATCH", self.codes(self.result(draft, state)))

    def test_lh13_P0_and_question_mode_do_not_hide_assertions(self):
        draft, state = self.fixture("Pocket4P支持8K")
        a = self.allocation(state)
        a["fact_status"].update(level="P0", verified_claim_ids=[], source_urls=[])
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))
        a["groups"][0]["claim_mode"] = "question"
        self.assertIn("E_SEED_GROUP_CONTEXT_INVALID", self.codes(self.result(draft, state)))

    def test_lh13_source_and_article_id_validation(self):
        text = "Pocket4能自动旋转"
        draft, state = self.fixture(text, model="pocket_4")
        fact = self.fact("p4_spinshot_auto", text, "pocket_4")
        self.register(state, fact)
        help_url = next(u for u in fact["source_urls"] if "repair.dji.com" in u)
        fact["source_urls"] = [help_url]
        self.assert_clean(self.result(draft, state))
        for invalid in [help_url.replace("01700043653", "01700000000"), help_url.replace("repair.dji.com", "repair.dji.com.evil.test"), "https://example.com/dji", "http://store.dji.com/cn/product/osmo-pocket-4"]:
            fact["source_urls"] = [invalid]
            self.assertIn("E_PRODUCT_FACT_SOURCE_MISMATCH", self.codes(self.result(draft, state)))

    def test_lh13_store_query_noise_preserves_content_identity(self):
        a = "https://store.dji.com/cn/product/osmo-pocket-4p-vlog-combo?from=site-nav&vid=241311"
        b = "https://store.dji.com/cn/product/osmo-pocket-4p-vlog-combo?set_region=CN"
        self.assertEqual(CHECKER.lh13_official_source_key(a), CHECKER.lh13_official_source_key(b))

    def test_lh13_new_fact_registry_id_unknown_and_model_mismatch(self):
        text = "Pocket4P那个3倍镜头我想试试"
        for bad, value, code in [("claim_id", "new_thing", "E_PRODUCT_FACT_UNKNOWN"), ("target_model", "pocket_4", "E_PRODUCT_FACT_MODEL_MISMATCH"), ("exact_copy_quote", "旧稿原句", "E_PRODUCT_FACT_QUOTE_MISMATCH")]:
            draft, state = self.fixture(text)
            fact = self.fact("4p_3x_physical_lens", text);fact[bad] = value
            self.register(state, fact)
            self.assertIn(code, self.codes(self.result(draft, state)))

    def test_lh13_p2_date_is_current_and_p1_not_future(self):
        for cid, text, model, delta in [("p4_spinshot_auto", "Pocket4能自动旋转", "pocket_4", -1), ("4p_3x_physical_lens", "Pocket4P有3倍镜头", "pocket_4p", 1)]:
            draft, state = self.fixture(text, model=model)
            fact = self.fact(cid, text, model);fact["checked_at"] = (date.today()+timedelta(days=delta)).isoformat()
            self.register(state, fact)
            self.assertIn("E_PRODUCT_FACT_DATE_INVALID", self.codes(self.result(draft, state)))

    def test_lh13_product_fact_is_not_original_footage_causal_evidence(self):
        text = "Pocket4能自动旋转，这段这么稳全靠这台相机"
        draft, state = self.fixture(text, model="pocket_4")
        self.register(state, self.fact("p4_spinshot_auto", "Pocket4能自动旋转", "pocket_4"))
        self.assertIn("E_OBSERVED_CURRENT_CAUSALITY", self.codes(self.result(draft, state)))

    def test_lh13_rotation_cannot_claim_simultaneous_tracking(self):
        text = "Pocket4能自动旋转同时跟随"
        draft, state = self.fixture(text, model="pocket_4")
        self.register(state, self.fact("p4_spinshot_auto", text, "pocket_4"))
        self.assertIn("E_PRODUCT_FACT_FORBIDDEN", self.codes(self.result(draft, state)))

    def test_lh13_fourth_group_facts_cannot_escape(self):
        draft, state = self.fixture(counts=(0, 0, 0, 0))
        draft = draft.replace("门口那次回头留得恰好", "4p有3倍镜头")
        self.allocation(state)["groups"][3].update(product_connection="镜头试用兴趣", target_model="pocket_4p")
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))
        self.register(state, self.fact("4p_3x_physical_lens", "4p有3倍镜头"), group=4)
        self.assert_clean(self.result(draft, state))

    def test_lh13_visual_main_reply_capability_requires_own_quote(self):
        draft, state = self.fixture(counts=(0, 1))
        draft = draft.replace("杯沿已经快挨着桌边了", "这台支持8K")
        self.assertIn("E_PRODUCT_FACT_UNREGISTERED", self.codes(self.result(draft, state)))

    def test_lh13_missing_hash_and_stale_hash_rejected(self):
        draft, state = self.fixture()
        self.assertIn("E_DRAFT_HASH_MISMATCH", self.codes(self.result(draft, state, rehash=False)))
        self.result(draft, state)
        self.assertIn("E_DRAFT_HASH_MISMATCH", self.codes(self.result(draft+"\n", state, rehash=False)))

    def test_lh13_missing_or_revise_semantic_review_is_not_accepted(self):
        draft, state = self.fixture()
        state["qa"]["semantic_review"].pop("seeding_review")
        self.assertIn("E_SEEDING_REVIEW_MISSING", self.codes(self.result(draft, state)))
        draft, state = self.fixture()
        state["qa"]["semantic_review"]["seeding_review"][0]["verdict"] = "revise"
        self.assertIn("E_SEEDING_REVIEW_REVISE", self.codes(self.result(draft, state)))

    def test_lh13_interest_quote_group_and_product_name_only_rejected(self):
        for change, code in [({"group": 4}, "E_SEEDING_INTEREST_GROUP_INVALID"), ({"exact_copy_quote": "旧稿"}, "E_SEEDING_INTEREST_QUOTE_MISMATCH"), ({"exact_copy_quote": "Pocket4P"}, "E_SEEDING_INTEREST_NAME_ONLY"), ({"interest": ""}, "E_SEEDING_INTEREST_INVALID")]:
            draft, state = self.fixture()
            state["qa"]["semantic_review"]["seeding_review"][0]["interest_entries"][0].update(change)
            self.assertIn(code, self.codes(self.result(draft, state)))

    def test_lh13_semantic_review_duplicate_and_orphan_rejected(self):
        draft, state = self.fixture()
        records = state["qa"]["semantic_review"]["seeding_review"]
        records.append(copy.deepcopy(records[0]))
        self.assertIn("E_SEEDING_REVIEW_DUPLICATE", self.codes(self.result(draft, state)))
        records[-1]["id"] = "orphan"
        self.assertIn("E_SEEDING_REVIEW_ORPHAN", self.codes(self.result(draft, state)))

    def test_lh13_template_does_not_prefill_passed_or_comment_counts(self):
        state = json.loads((ROOT/"assets/pocket_comment_state.lh13.template.json").read_text())
        self.assertEqual(state["rule_version"], CHECKER.LH13_RULE_VERSION)
        self.assertEqual(state["draft_sha256"], "")
        self.assertEqual(state["capture_policy"]["source_skill"], "/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/MODULE.md")
        self.assertEqual(state["qa"]["semantic_review"]["seeding_review"], [])
        self.assertEqual(len(self.allocation(state)["groups"]), 1)
        self.assertEqual(self.allocation(state)["groups"][0]["product_facts"], [])

    def test_lh13_minimum_fact_quote_accepts_emotional_prefix(self):
        text = "想试试4p那个3倍镜头，就拍这种半身"
        draft, state = self.fixture(text)
        self.register(state, self.fact("4p_3x_physical_lens", "4p那个3倍镜头"))
        self.assert_clean(self.result(draft, state))

    def test_lh13_invalid_claim_pattern_reports_registry_error(self):
        data = copy.deepcopy(legacy.REGISTRY)
        data["lh13"]["claims"]["4p_zoom_button"]["lh13_assertion_patterns"] = ["["]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"claims.json"
            path.write_text(json.dumps(data))
            diagnostics = []
            registry = CHECKER.load_claim_registry(path, "strict", diagnostics, lh13=True)
        self.assertEqual(registry, {})
        self.assertTrue(any(d["code"] == "E_CLAIM_REGISTRY_INVALID" for d in diagnostics))

    def test_lh13_passed_label_without_reason_or_interest_is_insufficient(self):
        for field, value, code in [("reason", "", "E_SEEDING_REVIEW_REASON_MISSING"), ("interest_entries", [], "E_SEEDING_INTEREST_MISSING")]:
            draft, state = self.fixture()
            state["qa"]["semantic_review"]["seeding_review"][0][field] = value
            self.assertIn(code, self.codes(self.result(draft, state)))

    def test_lh13_visual_supplement_cannot_be_the_only_declared_seeding_basis(self):
        draft, state = self.fixture()
        self.allocation(state)["groups"][0]["product_connection"] = ""
        self.assertIn("E_SEEDING_INTEREST_CONNECTION_MISSING", self.codes(self.result(draft, state)))

    def test_lh13_positive_claim_cannot_support_its_explicit_opposite(self):
        cases = [("Pocket4不能自动旋转", "p4_spinshot_auto", "pocket_4"), ("4p没有3倍镜头", "4p_3x_physical_lens", "pocket_4p"), ("4p没有实体变焦键", "4p_zoom_button", "pocket_4p")]
        for text, cid, model in cases:
            with self.subTest(cid=cid):
                draft, state = self.fixture(text, model=model)
                self.register(state, self.fact(cid, text, model))
                self.assertIn("E_PRODUCT_FACT_FORBIDDEN", self.codes(self.result(draft, state)))

    def test_lh13_true_rotation_limit_and_negative_question_remain_accepted(self):
        text = "Pocket4的旋转模式不能同时开跟随"
        draft, state = self.fixture(text, model="pocket_4")
        self.register(state, self.fact("p4_spinshot_auto", text, "pocket_4"))
        self.assert_clean(self.result(draft, state))
        draft, state = self.fixture("Pocket4不能自动旋转吗？想试试", model="pocket_4")
        self.assert_clean(self.result(draft, state))

    def material_fixture(self, material_path):
        draft, state = self.fixture()
        draft = draft.replace("https://www.xiaohongshu.com/explore/test", "user-material:T1")
        allocation = self.allocation(state)
        allocation.update(id="T1", canonical_url="user-material:T1", user_material={"path": str(material_path), "anchor": "T1", "exact_quote": "白纱旁的人像材料来自用户输入"})
        state["capture_policy"] = {"primary_surface": "user_supplied_evidence"}
        for kind in ["diversity_review", "seeding_review"]:
            state["qa"]["semantic_review"][kind][0]["id"] = "T1"
        return draft, state

    def test_lh13_user_material_requires_real_local_anchor_and_quote(self):
        with tempfile.TemporaryDirectory() as tmp:
            material = Path(tmp)/"input.md"
            material.write_text("## T1\n白纱旁的人像材料来自用户输入\n## T2\n别的材料\n")
            draft, state = self.material_fixture(material)
            self.assert_clean(self.result(draft, state))
            source = self.allocation(state)["user_material"]
            source["exact_quote"] = "别的材料"
            self.assertIn("E_USER_MATERIAL_INVALID", self.codes(self.result(draft, state)))
            source["exact_quote"] = "白纱旁的人像材料来自用户输入"
            material.unlink()
            self.assertIn("E_USER_MATERIAL_INVALID", self.codes(self.result(draft, state)))

    def test_lh13_user_material_cannot_substitute_for_remote_or_paused_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            material = Path(tmp)/"input.md"
            material.write_text("## T1\n白纱旁的人像材料来自用户输入\n")
            for kind in ["capture", "paused", "remote"]:
                draft, state = self.material_fixture(material)
                if kind == "capture": state["capture_policy"]["primary_surface"] = "connected_google_chrome_social_media_assistant"
                elif kind == "paused": state["failed_ids"] = ["T1"]
                else: self.allocation(state)["user_material"]["origin_url"] = "https://www.xiaohongshu.com/explore/blocked"
                self.assertIn("E_USER_MATERIAL_INVALID", self.codes(self.result(draft, state)))

    def test_lh13_user_material_does_not_relax_legacy_link_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            material = Path(tmp)/"input.md"
            material.write_text("## T1\n白纱旁的人像材料来自用户输入\n")
            draft, state = self.material_fixture(material)
            state["rule_version"] = CHECKER.LH12_RULE_VERSION
            self.assertIn("E_SEED_CONTEXT_LINK_INVALID", self.codes(self.result(draft, state)))

    def test_lh13_extension_is_inert_for_lh12_and_prior(self):
        diagnostics=[]
        registry = CHECKER.load_claim_registry(legacy.REGISTRY_PATH, "strict", diagnostics)
        self.assertNotIn("p4_spinshot_auto", registry["claims"])
        self.assertEqual(diagnostics, [])
        draft, state = legacy.LH12FlexibleDeliveryTests().fixture((0, 0))
        state["draft_sha256"] = "not-a-hash"
        state["qa"]["semantic_review"]["seeding_review"] = [{"verdict":"revise"}]
        self.assert_clean(self.run_draft(draft, state))

    def test_lh13_older_model_ids_are_registered_only_in_extension(self):
        diagnostics = []
        registry = CHECKER.load_claim_registry(legacy.REGISTRY_PATH, "strict", diagnostics, lh13=True)
        self.assertEqual(diagnostics, [])
        self.assertTrue({"pocket_1", "pocket_2"}.issubset(registry["model_ids"]))
        previous = CHECKER.load_claim_registry(legacy.REGISTRY_PATH, "strict", [], lh13=False)
        self.assertNotIn("pocket_1", previous["model_ids"])
        self.assertNotIn("pocket_2", previous["model_ids"])

    def test_lh13_old_model_aliases_remain_explicit(self):
        for alias in ["p1", "op1", "Pocket1", "初代"]:
            self.assertEqual(CHECKER.normalize_model(alias), "pocket_1")
        for alias in ["p2", "DJI Pocket 2", "Pocket2", "2"]:
            self.assertEqual(CHECKER.normalize_model(alias), "pocket_2")
        self.assertEqual(CHECKER.normalize_model("Pocket"), "unknown")

    def test_lh13_new_source_overlay_does_not_mutate_legacy_claim(self):
        diagnostics = []
        current = CHECKER.load_claim_registry(legacy.REGISTRY_PATH, "strict", diagnostics, lh13=True)
        original = CHECKER.load_claim_registry(legacy.REGISTRY_PATH, "strict", [], lh13=False)
        self.assertEqual(diagnostics, [])
        self.assertTrue(any("customId=01700043653" in source for source in current["claims"]["p4_internal_107gb"]["official_sources"]))
        self.assertFalse(any("repair.dji.com" in source for source in original["claims"]["p4_internal_107gb"]["official_sources"]))


if __name__ == "__main__":
    unittest.main()
