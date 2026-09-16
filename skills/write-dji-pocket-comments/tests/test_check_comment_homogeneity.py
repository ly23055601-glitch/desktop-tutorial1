from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "check_comment_homogeneity.py"
REGISTRY_PATH = SKILL_ROOT / "references" / "product-claims.json"
REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
SPEC = importlib.util.spec_from_file_location("pocket_lh5_checker", SCRIPT_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


def lh10_neutral_template_fixture() -> dict:
    # Keep the legacy three-slot fixture explicit as the shipped template evolves.
    state = json.loads((SKILL_ROOT / "assets" / "pocket_comment_state.template.json").read_text(encoding="utf-8"))
    state["rule_version"] = "2026-09-05-LH10"
    state["semantic_policy"].pop("lh11_optional_main_name", None)
    state["semantic_policy"].pop("lh12_content_driven_delivery", None)
    for block in state["block_allocations"]:
        for allocation in block["persuasion_allocations"]:
            example = allocation["groups"][0]
            allocation["groups"] = [{**json.loads(json.dumps(example)), "group": number} for number in range(1, 4)]
    return state


def lh11_neutral_template_fixture() -> dict:
    state = lh10_neutral_template_fixture()
    state["rule_version"] = "2026-09-05-LH11"
    state["semantic_policy"]["lh11_optional_main_name"] = {
        "usual_arrangement": "two_naturally_named_mains_and_one_visual_main_without_name; not_a_hard_ratio",
        "new_claim_modes": [], "new_group_flags": [],
    }
    return state


def draft_text(main: str) -> str:
    return f"""## 小红书 1｜https://www.xiaohongshu.com/explore/test

主评论：{main}
↳ 回复1：这个距离才是我会纠结的点
↳ 回复2：也得看平时是不是真的常拍

主评论：柜台签字那下，“不买了”已经没人信了
↳ 回复1：那个停顿太真实了
↳ 回复2：我倒更喜欢前面没说完的半句

主评论：最后那个回头我反而多看了一遍
↳ 回复1：我也是，差点划走又退回来
↳ 回复2：但前一秒更好笑
"""


def group_context(
    group: int,
    *,
    mode: str = "observed",
    claim_id: str = "",
    target_model: str = "unknown",
    basis: str = "visual",
    benefit: str = "",
    condition: str = "",
    boundary: str = "",
    sources: list[str] | None = None,
    contrast_models: list[str] | None = None,
    s_level: str = "S0",
    include_actual_s: bool = True,
) -> dict:
    result = {
        "group": group,
        "seeding_mechanism": "",
        "purchase_stage": "",
        "audience_perspective": "",
        "claim_mode": mode,
        "claim_id": claim_id,
        "target_model": target_model,
        "contrast_models": contrast_models or [],
        "benefit_basis": basis,
        "user_benefit": benefit,
        "usage_condition": condition,
        "boundary": boundary,
        "evidence_sources": sources or [],
        "target_s_level": s_level,
    }
    if include_actual_s:
        result["actual_s_level"] = s_level
    return result


def state_for(
    strong: dict,
    *,
    model_level: str = "M2",
    confirmed_model: str = "pocket_4p",
    claimed_model: str | None = None,
    evidence_type: str | None = None,
    watermark_present: bool = False,
    watermark_used: bool = False,
    n_level: str = "N1",
    scene_tags: list[str] | None = None,
    f_level: str = "F0",
    feature_claims: list[str] | None = None,
    p_level: str = "P1",
    verified_claims: list[str] | None = None,
    causal_cap: str = "S0",
    scenario_cap: str = "S2",
    strong_group: int | None = 1,
    mixed_models: list[str] | None = None,
    shot_mapping: str = "not_applicable",
    shot_mapping_evidence: list[str] | None = None,
    source_urls: list[str] | None = None,
    allocation_id: str = "test",
    under_target_reason: str = "",
    evidence_stop_ids: list[str] | None = None,
) -> dict:
    if evidence_type is None:
        evidence_type = {
            "M0": "unknown",
            "M1": "author_claim",
            "M2": "ui_confirmed",
        }.get(model_level, "unknown")
    verified = verified_claims or []
    if source_urls is None:
        source_urls = []
        for claim_id in verified:
            source_urls.extend(REGISTRY["claims"][claim_id].get("official_sources", []))
    return {
        "rule_version": "2026-09-02-LH5",
        "claim_registry_version": "2026-09-02-LH5",
        "semantic_policy": {
            "evidence_source_format": "kind:shared_anchor:detail",
            "shot_mapping_format": "shot:anchor:model:source",
            "user_benefit_must_quote_copy": True,
            "s3_usage_condition_and_boundary_must_quote_copy": True,
            "actual_s_level_required": True,
        },
        "evidence_stop_ids": evidence_stop_ids or [],
        "block_allocations": [
            {
                "block_id": "test",
                "persuasion_allocations": [
                    {
                        "id": allocation_id,
                        "section_number": "1",
                        "canonical_url": "https://www.xiaohongshu.com/explore/test",
                        "model_status": {
                            "level": model_level,
                            "claimed_model": claimed_model or confirmed_model,
                            "confirmed_model": confirmed_model,
                            "evidence_type": evidence_type,
                            "mixed_models": mixed_models or [],
                            "shot_mapping": shot_mapping,
                            "shot_mapping_evidence": shot_mapping_evidence or [],
                            "evidence": "fixture",
                        },
                        "watermark_hint": {
                            "present": watermark_present,
                            "model": confirmed_model if watermark_present else "unknown",
                            "used_as_evidence": watermark_used,
                            "mentioned_in_copy": False,
                        },
                        "scene_need": {
                            "level": n_level,
                            "tags": scene_tags or [],
                            "evidence": "fixture",
                        },
                        "feature_use": {
                            "level": f_level,
                            "claim_ids": feature_claims or [],
                            "evidence": "fixture",
                        },
                        "fact_status": {
                            "level": p_level,
                            "verified_claim_ids": verified,
                            "checked_at": date.today().isoformat(),
                            "source_urls": source_urls,
                        },
                        "clip_causality_cap": causal_cap,
                        "scenario_fit_cap": scenario_cap,
                        "strong_seed_group": strong_group,
                        "under_target_reason": under_target_reason,
                        "groups": [
                            strong,
                            group_context(2),
                            group_context(3),
                        ],
                    }
                ],
            }
        ],
    }


LH6_GROUP_SCHEMA = json.loads(json.dumps(CHECKER.LH6_GROUP_SCHEMA_CONTRACT, ensure_ascii=False))


def as_lh6(state: dict) -> dict:
    converted = json.loads(json.dumps(state, ensure_ascii=False))
    converted["rule_version"] = "2026-09-03-LH6"
    converted["claim_registry_version"] = "2026-09-02-LH5"
    converted["semantic_policy"]["lh6_group_schema"] = json.loads(
        json.dumps(LH6_GROUP_SCHEMA, ensure_ascii=False)
    )
    for block in converted["block_allocations"]:
        for allocation in block["persuasion_allocations"]:
            for group in allocation["groups"]:
                anchor = f"anchor-{allocation['section_number']}-{group['group']}"
                group.update(
                    {
                        "main_anchor_ids": [anchor],
                        "main_moves": ["observation"],
                        "seed_layers": {"main": [], "replies": []},
                        "light_meme_anchor": "",
                    }
                )
    return converted


def stopped_state(*, first_s_level: str = "S0") -> dict:
    return state_for(
        group_context(1, s_level=first_s_level),
        model_level="M0",
        confirmed_model="unknown",
        n_level="N0",
        p_level="P0",
        causal_cap="S0",
        scenario_cap="S0",
        strong_group=None,
        under_target_reason="没有足够证据建立产品链路",
        evidence_stop_ids=["test"],
    )


def draft_from_groups(groups: list[tuple[str, list[str]]]) -> str:
    lines = ["## 小红书 1｜https://www.xiaohongshu.com/explore/test", ""]
    for main, replies in groups:
        lines.append(f"主评论：{main}")
        lines.extend(f"↳ 回复{index}：{reply}" for index, reply in enumerate(replies, 1))
        lines.append("")
    return "\n".join(lines)


def as_lh7(state: dict, *, count: int = 3, main_only: bool = False) -> dict:
    converted = as_lh6(state)
    converted["rule_version"] = "2026-09-05-LH7"
    converted["delivery_mode"] = "main_only" if main_only else "with_replies"
    for block in converted["block_allocations"]:
        for allocation in block["persuasion_allocations"]:
            allocation["groups"] = allocation["groups"][:count]
            allocation["reduced_output_reason"] = "只找到两处可独立回应的帖子细节" if count < 3 else ""
    return converted


def lh7_draft(mains: list[str] | None = None, *, main_only: bool = False) -> str:
    mains = mains if mains is not None else [
        "你给Pocket挪了半张桌子哈哈",
        "杯子都没摆稳就开始给大疆Pocket找位置了",
        "旁边那只猫好像也在等OsmoPocket摆好",
    ]
    replies = [
        ["杯子先委屈一下", "还给它垫了块布"],
        ["那个摇晃看得我伸手想扶", "我也盯着杯子看完了"],
        ["猫一直没移开眼睛", "桌上突然多了个东西它得看看"],
    ]
    return draft_from_groups([(main, [] if main_only else replies[index]) for index, main in enumerate(mains)])


def personal_state(*, count: int = 1, main_only: bool = True, model: str | None = None, facts: list[str] | None = None) -> dict:
    state = as_lh7(stopped_state(), count=count, main_only=main_only)
    state["rule_version"] = "2026-09-05-LH8"
    state["evidence_stop_ids"] = []
    allocation = state["block_allocations"][0]["persuasion_allocations"][0]
    allocation["under_target_reason"] = ""
    for group in allocation["groups"]:
        group.update(claim_mode="personal_need", benefit_basis="workflow", target_s_level="S1", actual_s_level="S1", need_connection="原帖讲解出门前的设置顺序，触发自己的出游拍摄准备", personal_context=None)
        group["main_moves"] = ["need", "reaction"]
        group["seed_layers"] = {"main": ["need", "product"], "replies": []}
    if model or facts:
        allocation["groups"][0]["personal_context"] = {"source_ref": "user-material:test-personal-brief", "facts": facts or ["用户材料中明确持有该型号并准备出游"], "models": [model] if model else []}
    return state


class LH5SemanticTests(unittest.TestCase):
    def run_case(self, main: str, state: dict | None, *, seeding_policy: str = "strict") -> dict:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text(draft_text(main), encoding="utf-8")
            state_path = None
            if state is not None:
                state_path = root / "pocket_comment_state.json"
                state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            return CHECKER.audit(
                [draft],
                product_policy="off",
                state_path=state_path,
                seeding_policy=seeding_policy,
                claim_registry_path=REGISTRY_PATH,
            )

    def run_draft(
        self,
        draft_value: str,
        state: dict,
        *,
        baseline_value: str | None = None,
        seeding_policy: str = "strict",
    ) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            state_path = root / "pocket_comment_state.json"
            draft.write_text(draft_value, encoding="utf-8")
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            baselines: list[Path] = []
            if baseline_value is not None:
                baseline = root / "baseline.md"
                baseline.write_text(baseline_value, encoding="utf-8")
                baselines.append(baseline)
            return CHECKER.audit(
                [draft],
                baseline_paths=baselines,
                product_policy="off",
                state_path=state_path,
                seeding_policy=seeding_policy,
                claim_registry_path=REGISTRY_PATH,
            )

    @staticmethod
    def semantic_codes(result: dict) -> set[str]:
        return set(result["distributions"]["seeding"]["semantic"]["findings_by_code"])

    def test_watermark_and_pretty_sunrise_cannot_score_as_product_benefit(self) -> None:
        strong = group_context(
            1,
            mode="causal",
            basis="visual",
            benefit="把早晨留住",
            sources=["watermark"],
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="watermark_only",
            watermark_present=True,
            watermark_used=True,
            n_level="N1",
            scene_tags=["wide_scene"],
            p_level="P0",
            causal_cap="S0",
        )
        result = self.run_case("朝霞太漂亮了，Pocket把早晨留住了", state)
        codes = self.semantic_codes(result)
        self.assertIn("E_WATERMARK_AS_SEED", codes)
        self.assertIn("E_GENERIC_SCENE_AS_PRODUCT_BENEFIT", codes)

    def test_unshown_stage_feature_passes_as_conditional_60mm_fit(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用为了表情往前挤",
            condition="经常隔着人群拍舞台表情",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="unknown",
            scene_tags=["stage", "across_crowd"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("经常隔着人群拍舞台表情的话，我会先看4P的60mm实体中焦，不用为了表情往前挤", state)
        self.assertEqual(self.semantic_codes(result), set())

    def test_pocket_4_cannot_use_4p_physical_60mm_claim(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4",
            basis="product",
            benefit="不用挤前排",
            condition="经常隔着人群拍表情",
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4",
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("经常隔人群拍表情的话，我会看Pocket 4的60mm实体中焦", state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(result))

    def test_pocket_4_2x_requires_non_optical_and_mode_boundaries(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="p4_2x_lossless",
            target_model="pocket_4",
            basis="product",
            benefit="收紧一点构图",
            condition="主要拍普通视频",
            boundary="不是光学变焦，低光、慢动作和延时不支持",
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4",
            scene_tags=["light_reframe"],
            p_level="P2",
            verified_claims=["p4_2x_lossless"],
        )
        good = self.run_case(
            "主要拍普通视频、想收紧一点构图的话，可以看Pocket 4的2倍无损；它不是光学变焦，低光视频、慢动作和延时摄影不支持",
            state,
        )
        self.assertEqual(self.semantic_codes(good), set())

        missing_modes = self.run_case("想收紧构图的话，可以看Pocket 4的2倍无损，它不是光学变焦", state)
        self.assertIn("E_HIGH_RISK_MODE_CONDITION_MISSING", self.semantic_codes(missing_modes))

        one_mode_only = self.run_case(
            "想收紧一点构图的话，可以看Pocket 4的2倍无损，它不是光学变焦，慢动作不支持",
            state,
        )
        self.assertIn("E_HIGH_RISK_MODE_CONDITION_MISSING", self.semantic_codes(one_mode_only))

        optical = self.run_case("想收紧构图的话，可以看Pocket 4的2倍光学变焦", state)
        self.assertIn("E_DIGITAL_ZOOM_WRITTEN_AS_OPTICAL", self.semantic_codes(optical))

    def test_workflow_or_visual_value_cannot_be_s2(self) -> None:
        for wording in [
            "这个转场用Pocket复刻很省事",
            "固定机位留空景，后期同框确实省事",
            "Pocket和Nano这样混拍，剪起来少返工",
        ]:
            with self.subTest(wording=wording):
                strong = group_context(
                    1,
                    mode="scenario_fit",
                    claim_id="shared_3axis_gimbal",
                    target_model="pocket_4",
                    basis="workflow",
                    benefit="后期少返工",
                    condition="经常做这种内容",
                    s_level="S2",
                )
                state = state_for(
                    strong,
                    confirmed_model="pocket_4",
                    scene_tags=["walking"],
                    verified_claims=["shared_3axis_gimbal"],
                )
                self.assertIn("E_GENERIC_SCENE_AS_PRODUCT_BENEFIT", self.semantic_codes(self.run_case(wording, state)))

    def test_direct_feature_demos_can_use_causal_mode(self) -> None:
        cases = [
            (
                "Pocket画面点开慢动作后，舔鼻从一闪变成能看清动作，回看不用来回拖",
                "shared_slow_motion_mode",
                "pocket_4",
                "P1",
                ["fast_action"],
                "回看不用来回拖",
            ),
            (
                "4P画面先打开智能跟随，人横移时取景框还一直跟住，自己拍能少重来一次",
                "shared_intelligent_tracking",
                "pocket_4p",
                "P2",
                ["remote_moving_subject"],
                "自己拍能少重来一次",
            ),
            (
                "4P画面点按从1×切到3×，人物从环境人像变成半身，站原地也能换景别",
                "4p_dual_20_60",
                "pocket_4p",
                "P1",
                ["near_far_switch"],
                "站原地也能换景别",
            ),
        ]
        for wording, claim_id, model, p_level, tags, benefit in cases:
            with self.subTest(claim_id=claim_id):
                strong = group_context(
                    1,
                    mode="causal",
                    claim_id=claim_id,
                    target_model=model,
                    basis="product",
                    benefit=benefit,
                    sources=["operation:t01:visible-control", "result:t01:visible-output"],
                    s_level="S2",
                )
                state = state_for(
                    strong,
                    confirmed_model=model,
                    scene_tags=tags,
                    f_level="F2",
                    feature_claims=[claim_id],
                    p_level=p_level,
                    verified_claims=[claim_id],
                    causal_cap="S2",
                )
                self.assertEqual(self.semantic_codes(self.run_case(wording, state)), set())

    def test_causal_claim_below_f2_is_rejected(self) -> None:
        claim_id = "4p_dual_20_60"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="站原地也能换景别",
            s_level="S2",
        )
        state = state_for(
            strong,
            scene_tags=["near_far_switch"],
            f_level="F1",
            feature_claims=[claim_id],
            verified_claims=[claim_id],
            causal_cap="S1",
        )
        result = self.run_case("4P的1×和3×让人物从环境人像变成半身，少走几步", state)
        self.assertIn("E_CAUSAL_CLAIM_BELOW_F2", self.semantic_codes(result))

        f2_without_link = state_for(
            strong,
            scene_tags=["near_far_switch"],
            f_level="F2",
            feature_claims=[claim_id],
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        no_link_result = self.run_case("4P的1×和3×让人物从环境人像变成半身，少走几步", f2_without_link)
        self.assertIn("E_FEATURE_EVIDENCE_LINK_MISSING", self.semantic_codes(no_link_result))

    def test_mixed_unmapped_blocks_causal_but_allows_scenario_fit(self) -> None:
        claim_id = "shared_intelligent_tracking"
        causal = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="边骑也能少丢主体",
            sources=["operation:t01:tracking-enabled", "result:t01:subject-remains-framed"],
            s_level="S2",
        )
        causal_state = state_for(
            causal,
            evidence_type="mixed_unmapped",
            scene_tags=["remote_moving_subject"],
            f_level="F2",
            feature_claims=[claim_id],
            p_level="P2",
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        blocked = self.run_case("这段骑行正面就是4P的智能跟随，边骑也能少丢主体", causal_state)
        self.assertIn("E_MIXED_SHOT_MAPPING_MISSING", self.semantic_codes(blocked))

        fit = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="经常拍远处人物",
            s_level="S2",
        )
        fit_state = state_for(
            fit,
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="mixed_unmapped",
            scene_tags=["across_crowd"],
            verified_claims=["4p_physical_60mm"],
        )
        allowed = self.run_case(
            "如果经常隔人群拍人物表情，我会先比较4P的60mm，不用往前挤；这条混拍没标分镜，不能说眼前这格就是它拍的",
            fit_state,
        )
        self.assertEqual(self.semantic_codes(allowed), set())

    def test_mixed_watermark_cannot_appear_in_strong_group(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍舞台",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="mixed_unmapped",
            mixed_models=["pocket_4p", "pocket_4"],
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("这条混拍水印先不管，如果经常拍舞台会看4P的60mm，不用往前挤", state)
        codes = self.semantic_codes(result)
        self.assertIn("E_WATERMARK_AS_SEED", codes)
        self.assertIn("E_WATERMARK_MENTION", codes)

    def test_workflow_cannot_be_relabelled_as_product_benefit(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="shared_3axis_gimbal",
            target_model="pocket_4",
            basis="product",
            benefit="剪起来少返工",
            condition="如果经常做这种转场",
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4",
            scene_tags=["walking"],
            verified_claims=["shared_3axis_gimbal"],
        )
        result = self.run_case("如果经常做这种转场，Pocket的机械云台剪起来少返工", state)
        self.assertIn("E_WORKFLOW_ONLY_ABOVE_S1", self.semantic_codes(result))

    def test_all_mentioned_models_must_fit_claim_or_be_explicit_contrast(self) -> None:
        wrong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用挤前排",
            condition="如果经常拍舞台",
            s_level="S2",
        )
        wrong_state = state_for(
            wrong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        wrong_result = self.run_case("如果经常拍舞台，Pocket 4和4P都有60mm实体中焦，不用挤前排", wrong_state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(wrong_result))

        contrast = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            contrast_models=["pocket_4"],
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            boundary="Pocket 4没有这颗中焦",
            s_level="S2",
        )
        contrast_state = state_for(
            contrast,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
        )
        contrast_result = self.run_case(
            "如果经常拍远处人物，我会看4P的60mm，不用往前挤；Pocket 4没有这颗中焦",
            contrast_state,
        )
        self.assertEqual(self.semantic_codes(contrast_result), set())

    def test_claim_source_must_match_registered_official_page(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
            source_urls=["https://store.dji.com/cn/product/osmo-pocket-4-creator-combo"],
        )
        result = self.run_case("如果经常拍远处人物，会看4P的60mm，不用往前挤", state)
        self.assertIn("E_PRODUCT_FACT_SOURCE_MISSING", self.semantic_codes(result))

    def test_exact_4k240_claim_needs_exact_mode_terms(self) -> None:
        claim_id = "shared_wide_4k240_slowmo"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4",
            basis="product",
            benefit="回看不用来回拖",
            sources=["operation:t01:slow-motion-enabled", "result:t01:action-visible"],
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4",
            scene_tags=["fast_action"],
            f_level="F2",
            feature_claims=[claim_id],
            p_level="P2",
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        vague = self.run_case("画面打开慢动作后动作看清了，回看不用来回拖", state)
        self.assertIn("E_HIGH_RISK_MODE_CONDITION_MISSING", self.semantic_codes(vague))

        exact = self.run_case("Pocket 4画面打开广角4K/240fps慢动作后动作看清了，回看不用来回拖", state)
        self.assertEqual(self.semantic_codes(exact), set())

    def test_missing_actual_s_level_is_rejected(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
            include_actual_s=False,
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("如果经常拍远处人物，会看4P的60mm，不用往前挤", state)
        self.assertIn("E_ACTUAL_S_LEVEL_MISSING", self.semantic_codes(result))

    def test_mixed_mapping_must_share_causal_anchor_and_model(self) -> None:
        claim_id = "4p_dual_20_60"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="站原地也能换景别",
            sources=["operation:t01:tap-1x-to-3x", "result:t01:wide-to-half-body"],
            s_level="S2",
        )
        base_kwargs = dict(
            confirmed_model="pocket_4p",
            evidence_type="mixed_mapped",
            mixed_models=["pocket_4p", "pocket_4"],
            shot_mapping="mapped",
            scene_tags=["near_far_switch"],
            f_level="F2",
            feature_claims=[claim_id],
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        bad_state = state_for(
            strong,
            shot_mapping_evidence=["shot:other:pocket_4p:visible-ui"],
            **base_kwargs,
        )
        wording = "4P画面点按从1×切到3×，人从环境里落到半身，站原地也能换景别"
        self.assertIn("E_MIXED_SHOT_MAPPING_MISSING", self.semantic_codes(self.run_case(wording, bad_state)))

        good_state = state_for(
            strong,
            shot_mapping_evidence=["shot:t01:pocket_4p:visible-ui"],
            **base_kwargs,
        )
        self.assertEqual(self.semantic_codes(self.run_case(wording, good_state)), set())

    def test_s3_boundary_must_be_specific_to_claim(self) -> None:
        weak = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            boundary="不过要按预算选",
            s_level="S3",
        )
        weak_state = state_for(
            weak,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
            scenario_cap="S3",
        )
        weak_result = self.run_case(
            "如果经常拍远处人物，会看4P的60mm，不用往前挤，不过要按预算选",
            weak_state,
        )
        self.assertIn("E_S3_CLAIM_BOUNDARY_MISSING", self.semantic_codes(weak_result))

        good = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            boundary="不用中焦就没必要选4P",
            s_level="S3",
        )
        good_state = state_for(
            good,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
            scenario_cap="S3",
        )
        good_result = self.run_case(
            "如果经常拍远处人物，会看4P的60mm，不用往前挤；不用中焦就没必要选4P",
            good_state,
        )
        self.assertEqual(self.semantic_codes(good_result), set())

    def test_m0_cannot_assert_current_model_and_s0_cannot_hide_false_fact(self) -> None:
        observed = group_context(1)
        state = state_for(
            observed,
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="unknown",
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            allocation_id="test",
            under_target_reason="没有有效场景需求或功能演示",
            evidence_stop_ids=["test"],
        )
        assertion = self.run_case("这条就是Pocket 4P拍的", state)
        self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.semantic_codes(assertion))

        false_fact = self.run_case("Pocket 4P是20-60mm连续光学变焦", state)
        self.assertIn("E_FORBIDDEN_PRODUCT_CLAIM", self.semantic_codes(false_fact))

    def test_invalid_list_types_report_diagnostics_instead_of_crashing(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
        )
        state["block_allocations"][0]["persuasion_allocations"][0]["scene_need"]["tags"] = None
        result = self.run_case("如果经常拍远处人物，会看4P的60mm，不用往前挤", state)
        self.assertIn("E_SEED_CONTEXT_INVALID", self.semantic_codes(result))

    def test_header_only_draft_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("## 1｜virtual://header-only\n", encoding="utf-8")
            result = CHECKER.audit([draft], seeding_policy="off")
        self.assertIn("E_GROUP_COUNT", {item["code"] for item in result["diagnostics"]})

    def test_duplicate_section_numbers_can_be_scoped_by_draft_path(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = root / "left.md"
            right = root / "right.md"
            left.write_text(draft_text("如果经常拍远处人物，会看4P的60mm，不用往前挤"), encoding="utf-8")
            right.write_text(
                draft_text("如果经常拍远处人物，会看4P的60mm，不用往前挤").replace(
                    "/explore/test", "/explore/test-2"
                ),
                encoding="utf-8",
            )
            state = state_for(
                strong,
                model_level="M0",
                confirmed_model="unknown",
                scene_tags=["remote_subject"],
                verified_claims=["4p_physical_60mm"],
            )
            first = state["block_allocations"][0]["persuasion_allocations"][0]
            first["draft_path"] = str(left)
            second = json.loads(json.dumps(first, ensure_ascii=False))
            second["id"] = "test-2"
            second["draft_path"] = str(right)
            state["block_allocations"][0]["persuasion_allocations"].append(second)
            state_path = root / "state.json"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            scoped = CHECKER.audit(
                [left, right],
                state_path=state_path,
                seeding_policy="strict",
                claim_registry_path=REGISTRY_PATH,
            )
            self.assertNotIn("E_SEED_CONTEXT_AMBIGUOUS", self.semantic_codes(scoped))

            first.pop("draft_path")
            second.pop("draft_path")
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            ambiguous = CHECKER.audit(
                [left, right],
                state_path=state_path,
                seeding_policy="strict",
                claim_registry_path=REGISTRY_PATH,
            )
            self.assertIn("E_SEED_CONTEXT_AMBIGUOUS", self.semantic_codes(ambiguous))

    def test_current_assertion_and_shared_claim_must_match_confirmed_target(self) -> None:
        observed = group_context(1)
        state = state_for(
            observed,
            confirmed_model="pocket_4",
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            allocation_id="test",
            under_target_reason="没有有效需求",
            evidence_stop_ids=["test"],
        )
        assertion = self.run_case("这条就是Pocket 4P拍的", state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(assertion))

        claim_id = "shared_intelligent_tracking"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4",
            basis="product",
            benefit="自己拍能少重来一次",
            sources=["operation:t01:tracking-enabled", "result:t01:subject-remains-framed"],
            s_level="S2",
        )
        claim_state = state_for(
            strong,
            confirmed_model="pocket_4",
            scene_tags=["self_filming"],
            f_level="F2",
            feature_claims=[claim_id],
            p_level="P2",
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        shared_wrong = self.run_case("4P智能跟随锁住主体，自己拍能少重来一次", claim_state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(shared_wrong))

    def test_invalid_extra_shot_mapping_entry_is_not_ignored(self) -> None:
        claim_id = "4p_dual_20_60"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="站原地也能换景别",
            sources=["operation:t01:tap-1x-to-3x", "result:t01:wide-to-half-body"],
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4p",
            evidence_type="mixed_mapped",
            mixed_models=["pocket_4p", "pocket_4"],
            shot_mapping="mapped",
            shot_mapping_evidence=["shot:t01:pocket_4p:visible-ui", "garbage"],
            scene_tags=["near_far_switch"],
            f_level="F2",
            feature_claims=[claim_id],
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        wording = "4P画面从1×切到3×，人从环境里落到半身，站原地也能换景别"
        self.assertIn("E_SHOT_MAPPING_EVIDENCE_INVALID", self.semantic_codes(self.run_case(wording, state)))

    def test_exact_numeric_claims_cannot_pass_with_generic_terms(self) -> None:
        cases = [
            (
                "p4_runtime_240_lab",
                "pocket_4",
                "P2",
                ["long_recording"],
                "如果经常录一整天，Pocket 4的实验室续航在1080p条件下能少补一次电",
                "少补一次电",
            ),
            (
                "4p_dlog2_17stop_1x",
                "pocket_4p",
                "P2",
                ["high_contrast"],
                "如果经常调高反差素材，4P在1×广角用D-Log 2会让高光暗部更好调",
                "高光暗部更好调",
            ),
            (
                "p4_internal_107gb",
                "pocket_4",
                "P1",
                ["forgot_card"],
                "如果经常忘带卡，Pocket 4的内置存储能直接开拍",
                "能直接开拍",
            ),
        ]
        for claim_id, model, p_level, tags, wording, benefit in cases:
            with self.subTest(claim_id=claim_id):
                strong = group_context(
                    1,
                    mode="scenario_fit",
                    claim_id=claim_id,
                    target_model=model,
                    basis="product",
                    benefit=benefit,
                    condition="如果经常",
                    s_level="S2",
                )
                state = state_for(
                    strong,
                    model_level="M0",
                    confirmed_model="unknown",
                    scene_tags=tags,
                    p_level=p_level,
                    verified_claims=[claim_id],
                )
                self.assertIn(
                    "E_HIGH_RISK_MODE_CONDITION_MISSING",
                    self.semantic_codes(self.run_case(wording, state)),
                )

    def test_direct_dual_switch_requires_more_specific_claim(self) -> None:
        claim_id = "4p_physical_60mm"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="站原地也能换景别",
            sources=["operation:t01:tap-1x-to-3x", "result:t01:wide-to-half-body"],
            s_level="S2",
        )
        state = state_for(
            strong,
            confirmed_model="pocket_4p",
            scene_tags=["remote_subject"],
            f_level="F2",
            feature_claims=[claim_id],
            verified_claims=[claim_id],
            causal_cap="S2",
        )
        result = self.run_case("4P从1×切到3×和60mm中焦，站原地也能换景别", state)
        self.assertIn("E_MORE_SPECIFIC_CLAIM_REQUIRED", self.semantic_codes(result))

    def test_evidence_stop_ids_cannot_contain_orphans(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=["4p_physical_60mm"],
            evidence_stop_ids=["ghost"],
        )
        result = self.run_case("如果经常拍远处人物，会看4P的60mm，不用往前挤", state)
        self.assertIn("E_EVIDENCE_STOP_ORPHAN", self.semantic_codes(result))

    def test_model_status_internal_contradictions_are_rejected(self) -> None:
        def stopped_state(**kwargs: object) -> dict:
            return state_for(
                group_context(1),
                n_level="N0",
                p_level="P0",
                scenario_cap="S0",
                strong_group=None,
                under_target_reason="没有有效需求",
                evidence_stop_ids=["test"],
                **kwargs,
            )

        cases = [
            stopped_state(model_level="M0", claimed_model="pocket_4p", confirmed_model="unknown"),
            stopped_state(model_level="M1", claimed_model="pocket_4p", confirmed_model="pocket_4p"),
            stopped_state(model_level="M0", confirmed_model="unknown", evidence_type="ui_confirmed"),
        ]
        for state in cases:
            with self.subTest(model_status=state["block_allocations"][0]["persuasion_allocations"][0]["model_status"]):
                self.assertIn("E_MODEL_STATUS_INCONSISTENT", self.semantic_codes(self.run_case("只看柜台那一下", state)))

    def test_unique_context_honors_draft_path_and_short_links_need_canonical_url(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "actual.md"
            draft.write_text(draft_text("如果经常拍远处人物，会看4P的60mm，不用往前挤"), encoding="utf-8")
            state = state_for(
                strong,
                model_level="M0",
                confirmed_model="unknown",
                scene_tags=["remote_subject"],
                verified_claims=["4p_physical_60mm"],
            )
            allocation = state["block_allocations"][0]["persuasion_allocations"][0]
            allocation["draft_path"] = str(root / "other.md")
            state_path = root / "state.json"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            mismatch = CHECKER.audit(
                [draft],
                state_path=state_path,
                seeding_policy="strict",
                claim_registry_path=REGISTRY_PATH,
            )
            self.assertIn("E_SEED_CONTEXT_PATH_MISMATCH", self.semantic_codes(mismatch))

            short = root / "short.md"
            short.write_text(draft_text("如果经常拍远处人物，会看4P的60mm，不用往前挤").replace(
                "https://www.xiaohongshu.com/explore/test", "https://v.douyin.com/abc"
            ), encoding="utf-8")
            allocation["draft_path"] = str(short)
            allocation.pop("canonical_url", None)
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            unbound = CHECKER.audit(
                [short],
                state_path=state_path,
                seeding_policy="strict",
                claim_registry_path=REGISTRY_PATH,
            )
            self.assertIn("E_SEED_CONTEXT_LINK_UNBOUND", self.semantic_codes(unbound))

            allocation["canonical_url"] = "https://v.douyin.com/abc?foo=secret"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            bound = CHECKER.audit(
                [short],
                state_path=state_path,
                seeding_policy="strict",
                claim_registry_path=REGISTRY_PATH,
            )
            self.assertNotIn("E_SEED_CONTEXT_LINK_UNBOUND", self.semantic_codes(bound))

    def test_strong_model_claim_cannot_omit_product_name(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常隔人群拍舞台",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("如果经常隔人群拍舞台，60mm中焦不用往前挤", state)
        self.assertIn("E_TARGET_PRODUCT_NOT_IN_COPY", self.semantic_codes(result))

    def test_watermark_state_and_copy_must_agree(self) -> None:
        state = state_for(
            group_context(1),
            model_level="M0",
            confirmed_model="unknown",
            evidence_type="unknown",
            watermark_present=True,
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            under_target_reason="只有水印与泛成片",
            evidence_stop_ids=["test"],
        )
        result = self.run_case("Pocket拍的朝霞真好看", state)
        codes = self.semantic_codes(result)
        self.assertIn("E_WATERMARK_STATE_INCONSISTENT", codes)
        self.assertIn("E_WATERMARK_ONLY_NAMING", codes)

    def test_registry_loader_validates_every_claim_not_only_used_claims(self) -> None:
        mutated = json.loads(json.dumps(REGISTRY, ensure_ascii=False))
        mutated.pop("verified_at")
        mutated["claims"]["unused_bad_claim"] = {"models": "pocket_4"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(mutated, ensure_ascii=False), encoding="utf-8")
            diagnostics: list[dict] = []
            CHECKER.load_claim_registry(path, "strict", diagnostics)
        self.assertIn("E_CLAIM_REGISTRY_INVALID", {item["code"] for item in diagnostics})

        for field_name, bad_value in (("fact_status_required", "P0"), ("causal_min_feature_use", "F0")):
            with self.subTest(field_name=field_name):
                mutated = json.loads(json.dumps(REGISTRY, ensure_ascii=False))
                mutated["claims"]["4p_physical_60mm"][field_name] = bad_value
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "registry.json"
                    path.write_text(json.dumps(mutated, ensure_ascii=False), encoding="utf-8")
                    diagnostics = []
                    CHECKER.load_claim_registry(path, "strict", diagnostics)
                self.assertIn("E_CLAIM_REGISTRY_INVALID", {item["code"] for item in diagnostics})

    def test_m1_author_attribution_must_match_claimed_model(self) -> None:
        state = state_for(
            group_context(1, mode="attributed"),
            model_level="M1",
            claimed_model="pocket_4",
            confirmed_model="unknown",
            evidence_type="author_claim",
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            under_target_reason="没有有效需求",
            evidence_stop_ids=["test"],
        )
        result = self.run_case("作者说这条是Pocket 4P拍的", state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(result))

    def test_shared_s2_can_target_pocket_family_without_inventing_model(self) -> None:
        claim_id = "shared_internal_storage"
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id=claim_id,
            target_model="unknown",
            basis="product",
            benefit="能直接开拍",
            condition="如果经常忘带卡",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["forgot_card"],
            verified_claims=[claim_id],
        )
        result = self.run_case("如果经常忘带卡，Pocket的内置存储能直接开拍", state)
        self.assertEqual(self.semantic_codes(result), set())

    def test_evidence_axes_level_and_payload_must_be_consistent(self) -> None:
        base = state_for(
            group_context(1),
            model_level="M0",
            confirmed_model="unknown",
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            under_target_reason="没有有效需求",
            evidence_stop_ids=["test"],
        )
        mutations = [
            ("scene_need", "tags", ["stage"]),
            ("feature_use", "claim_ids", ["4p_physical_60mm"]),
            ("fact_status", "verified_claim_ids", ["4p_physical_60mm"]),
        ]
        for container, field, value in mutations:
            with self.subTest(field=f"{container}.{field}"):
                state = json.loads(json.dumps(base, ensure_ascii=False))
                allocation = state["block_allocations"][0]["persuasion_allocations"][0]
                allocation[container][field] = value
                if container == "fact_status":
                    allocation[container]["source_urls"] = REGISTRY["claims"]["4p_physical_60mm"]["official_sources"]
                result = self.run_case("只看柜台那一下", state)
                self.assertIn("E_EVIDENCE_AXIS_INCONSISTENT", self.semantic_codes(result))

    def test_scenario_fit_cannot_claim_current_clip_causality(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果常拍舞台",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        result = self.run_case("如果常拍舞台，4P的60mm就是这段人脸变近的原因，不用往前挤", state)
        self.assertIn("E_SCENARIO_FIT_CURRENT_CAUSALITY", self.semantic_codes(result))

    def test_contrast_model_cannot_inherit_target_only_fact(self) -> None:
        claim_id = "p4_lighter_body"
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id=claim_id,
            target_model="pocket_4",
            contrast_models=["pocket_4p"],
            basis="product",
            benefit="长时间拿着更省力",
            condition="如果经常长时间手持",
            boundary="不过还是看预算",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["long_handheld"],
            verified_claims=[claim_id],
        )
        result = self.run_case(
            "如果经常长时间手持，Pocket 4和4P都是190.5g，长时间拿着更省力，不过还是看预算",
            state,
        )
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.semantic_codes(result))

    def test_runtime_claim_requires_all_lab_conditions(self) -> None:
        claim_id = "p4_runtime_240_lab"
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id=claim_id,
            target_model="pocket_4",
            basis="product",
            benefit="少补一次电",
            condition="如果经常录一整天",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["long_recording"],
            p_level="P2",
            verified_claims=[claim_id],
        )
        incomplete = self.run_case("如果经常录一整天，Pocket 4实验室25℃测到240分钟，能少补一次电", state)
        self.assertIn("E_HIGH_RISK_MODE_CONDITION_MISSING", self.semantic_codes(incomplete))

        complete = self.run_case(
            "如果经常录一整天，Pocket 4在25℃、1080p/24fps、Wi-Fi关闭并息屏的实验室条件是240分钟，能少补一次电",
            state,
        )
        self.assertEqual(self.semantic_codes(complete), set())

    def test_correct_negations_are_not_reported_as_false_product_claims(self) -> None:
        claim_id = "p4_2x_lossless"
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id=claim_id,
            target_model="pocket_4",
            basis="product",
            benefit="能收紧一点构图",
            condition="如果主要拍普通视频",
            boundary="不是2倍光学变焦",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["light_reframe"],
            p_level="P2",
            verified_claims=[claim_id],
        )
        wording = "如果主要拍普通视频，Pocket 4的2倍无损能收紧一点构图；它不是2倍光学变焦，低光、慢动作和延时不支持"
        result = self.run_case(wording, state)
        codes = self.semantic_codes(result)
        self.assertNotIn("E_DIGITAL_ZOOM_WRITTEN_AS_OPTICAL", codes)
        self.assertNotIn("E_FORBIDDEN_PRODUCT_CLAIM", codes)
        self.assertEqual(codes, set())

        stopped = state_for(
            group_context(1),
            model_level="M0",
            confirmed_model="unknown",
            n_level="N0",
            p_level="P0",
            scenario_cap="S0",
            strong_group=None,
            under_target_reason="没有有效需求",
            evidence_stop_ids=["test"],
        )
        negated_assertion = self.run_case("不能说这段就是4P拍的", stopped)
        self.assertNotIn("E_CURRENT_MODEL_BELOW_M2", self.semantic_codes(negated_assertion))

    def test_non_http_official_source_is_rejected(self) -> None:
        claim_id = "4p_physical_60mm"
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="不用往前挤",
            condition="如果经常拍远处人物",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["remote_subject"],
            verified_claims=[claim_id],
            source_urls=["ftp://store.dji.com/cn/product/osmo-pocket-4p-vlog-combo"],
        )
        result = self.run_case("如果经常拍远处人物，会看4P的60mm，不用往前挤", state)
        self.assertIn("E_PRODUCT_FACT_SOURCE_MISSING", self.semantic_codes(result))

    def test_strict_mode_without_state_fails(self) -> None:
        result = self.run_case("柜台那句不买了我先不信", None)
        self.assertIn("E_SEED_STATE_MISSING", {item["code"] for item in result["diagnostics"]})
        self.assertGreater(result["summary"]["errors"], 0)

        empty = self.run_case("柜台那句不买了我先不信", {})
        self.assertIn("E_SEED_STATE_INVALID", {item["code"] for item in empty["diagnostics"]})

    def test_legacy_product_policy_can_be_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text(draft_text("这句停得刚刚好"), encoding="utf-8")
            result = CHECKER.audit([draft], seeding_policy="off")
        codes = {item["code"] for item in result["diagnostics"]}
        self.assertNotIn("W_TWO_CLEAR_ONE_HIDDEN", codes)
        self.assertNotIn("E_TWO_CLEAR_ONE_HIDDEN", codes)
        self.assertNotIn("W_HIDDEN_PRODUCT_CUE", codes)
        self.assertEqual(CHECKER.build_parser().parse_args(["draft.md"]).product_policy, "off")

    def test_documented_cli_contract_accepts_valid_lh5_state(self) -> None:
        strong = group_context(
            1,
            mode="scenario_fit",
            claim_id="4p_physical_60mm",
            target_model="pocket_4p",
            basis="product",
            benefit="不用为了表情往前挤",
            condition="经常拍舞台表情",
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M0",
            confirmed_model="unknown",
            scene_tags=["stage"],
            verified_claims=["4p_physical_60mm"],
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            state_path = root / "pocket_comment_state.json"
            draft.write_text(
                draft_text("经常隔着人群拍舞台表情的话，我会先看4P的60mm实体中焦，不用为了表情往前挤"),
                encoding="utf-8",
            )
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = CHECKER.main(
                    [
                        str(draft),
                        "--state",
                        str(state_path),
                        "--product-policy",
                        "off",
                        "--seeding-policy",
                        "strict",
                    ]
                )
        self.assertEqual(exit_code, 0, output.getvalue())

    def test_lh6_sample_hits_triple_enum_and_closed_copy(self) -> None:
        state = as_lh6(stopped_state())
        result = self.run_case(
            "门洞先替屋檐做了个天然取景框，后面木雕、造像、壁画一层层接上，大同把“景区审美完蛋”的担心原路退回。",
            state,
        )
        codes = self.semantic_codes(result)
        self.assertIn("E_MAIN_TRIPLE_ENUM", codes)
        self.assertIn("W_CLOSED_COPY", codes)

    def test_lh6_rules_do_not_backscan_lh5_or_baseline(self) -> None:
        bad_main = "门洞先框住屋檐，后面木雕、造像、壁画全接上，景区审美的担心原路退回"
        lh5_result = self.run_case(bad_main, stopped_state())
        lh5_codes = self.semantic_codes(lh5_result)
        self.assertNotIn("E_MAIN_TRIPLE_ENUM", lh5_codes)
        self.assertNotIn("W_CLOSED_COPY", lh5_codes)

        current = draft_text("最后那下我笑了")
        baseline = draft_text(bad_main)
        lh6_result = self.run_draft(current, as_lh6(stopped_state()), baseline_value=baseline)
        lh6_codes = self.semantic_codes(lh6_result)
        self.assertNotIn("E_MAIN_TRIPLE_ENUM", lh6_codes)
        self.assertNotIn("W_CLOSED_COPY", lh6_codes)

    def test_lh6_three_item_main_fails_but_split_replies_pass(self) -> None:
        state = as_lh6(stopped_state())
        failed = self.run_case("五分四十五秒的开箱，撕膜、本体、配件分别在哪段？", state)
        self.assertIn("E_MAIN_TRIPLE_ENUM", self.semantic_codes(failed))
        enumerations = [
            "五分四十五秒的开箱，撕膜、本体和配件分别在哪段？",
            "开箱里，撕膜，本体还有配件都想看",
            "先看撕膜，本体和配件都想看",
            "刚看完撕膜，本体和配件都想单独跳转",
            "我觉得撕膜，本体和配件都想看",
            "先推近，跟拍和收音都想测",
            "快速推近，跟拍和收音都想测",
        ]
        for main in enumerations:
            with self.subTest(main=main):
                self.assertIn(
                    "E_MAIN_TRIPLE_ENUM",
                    self.semantic_codes(self.run_case(main, as_lh6(stopped_state()))),
                )
        natural_clauses = [
            "她刚转身，我和旁边的人都笑了",
            "门洞先入画，我觉得屋檐和它更搭",
            "外面很亮，进去后明暗和颜色都变了",
            "镜头推近，我和她一起回头",
            "开头，门洞和屋檐都很搭",
            "灯亮了，人物和背景才看得清",
            "镜头停住，木雕和屋檐刚好叠在一起",
            "她笑了，门洞和屋檐都没抢过她",
        ]
        for main in natural_clauses:
            with self.subTest(natural_main=main):
                self.assertNotIn(
                    "E_MAIN_TRIPLE_ENUM",
                    self.semantic_codes(self.run_case(main, as_lh6(stopped_state()))),
                )
        three_steps = self.run_case("开头先拆纸箱，接着把机身举近，最后又把配件摆了一排", state)
        self.assertIn("E_MAIN_TRIPLE_ENUM", self.semantic_codes(three_steps))

        split = draft_from_groups(
            [
                (
                    "五分四十五秒的开箱求个时间轴",
                    ["撕膜放在哪段了", "本体我也想直接跳过去看", "配件留到最后也行"],
                ),
                ("柜台签字那下没忍住笑", ["停顿很真实", "前半句也好笑"]),
                ("最后那个回头我又看了一遍", ["差点划走", "我更喜欢前一秒"]),
            ]
        )
        passed = self.run_draft(split, state)
        self.assertNotIn("E_MAIN_TRIPLE_ENUM", self.semantic_codes(passed))

    def test_lh6_group_schema_accepts_contract_and_rejects_bad_fields(self) -> None:
        valid = as_lh6(stopped_state())
        self.assertNotIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("门口那下挺好笑", valid)))

        missing_policy_schema = as_lh6(stopped_state())
        del missing_policy_schema["semantic_policy"]["lh6_group_schema"]
        self.assertIn(
            "E_LH6_GROUP_SCHEMA",
            self.semantic_codes(self.run_case("门口那下挺好笑", missing_policy_schema)),
        )

        changed_policy_schema = as_lh6(stopped_state())
        changed_policy_schema["semantic_policy"]["lh6_group_schema"]["main_moves"]["max_items"] = 3
        self.assertIn(
            "E_LH6_GROUP_SCHEMA",
            self.semantic_codes(self.run_case("门口那下挺好笑", changed_policy_schema)),
        )

        mutations = {
            "anchors_empty": ("main_anchor_ids", []),
            "anchors_many": ("main_anchor_ids", ["a", "b"]),
            "anchors_blank_member": ("main_anchor_ids", ["a", ""]),
            "moves_empty": ("main_moves", []),
            "moves_many": ("main_moves", ["observation", "reaction", "question"]),
            "moves_duplicate": ("main_moves", ["reaction", "reaction"]),
            "moves_unknown": ("main_moves", ["summary"]),
            "seed_layers_not_object": ("seed_layers", []),
            "meme_not_string": ("light_meme_anchor", None),
        }
        for label, (field, value) in mutations.items():
            with self.subTest(label=label):
                state = as_lh6(stopped_state())
                group = state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
                group[field] = value
                self.assertIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("门口那下挺好笑", state)))

        layer_mutations = [
            {"main": ["need", "product", "benefit"], "replies": []},
            {"main": ["need", "need"], "replies": []},
            {"main": ["need", ""], "replies": []},
            {"main": ["feature"], "replies": []},
            {"main": [], "replies": ["need", "need"]},
            {"main": [], "replies": ["need", "question", "product", "benefit", "boundary", "extra"]},
            {"main": []},
        ]
        for seed_layers in layer_mutations:
            with self.subTest(seed_layers=seed_layers):
                state = as_lh6(stopped_state())
                state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]["seed_layers"] = seed_layers
                self.assertIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("门口那下挺好笑", state)))

    def test_lh6_light_meme_must_bind_the_single_main_anchor(self) -> None:
        valid = as_lh6(stopped_state())
        first = valid["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        first["main_moves"] = ["reaction", "joke"]
        first["light_meme_anchor"] = first["main_anchor_ids"][0]
        valid_codes = self.semantic_codes(self.run_case("15秒的坏处：刚看清最后那面小像，视频没了", valid))
        self.assertNotIn("E_LH6_GROUP_SCHEMA", valid_codes)

        missing = as_lh6(stopped_state())
        missing_first = missing["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        missing_first["main_moves"] = ["joke"]
        self.assertIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("15秒根本不够看", missing)))

        mismatched = as_lh6(stopped_state())
        mismatched_first = mismatched["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        mismatched_first["light_meme_anchor"] = "another-anchor"
        self.assertIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("15秒根本不够看", mismatched)))

        reply_joke = as_lh6(stopped_state())
        reply_first = reply_joke["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        reply_first["light_meme_anchor"] = reply_first["main_anchor_ids"][0]
        self.assertNotIn("E_LH6_GROUP_SCHEMA", self.semantic_codes(self.run_case("门口那下挺好笑", reply_joke)))

    def test_lh6_internal_audit_voice_is_always_rejected(self) -> None:
        samples = [
            "本地只有封面，其他先不说",
            "这段证据还接不上",
            "标题里的慢动作仍是作者口径",
            "先不替设备认功",
            "性能先不替它下结论",
            "这里还要看因果边界",
        ]
        for main in samples:
            with self.subTest(main=main):
                result = self.run_case(main, as_lh6(stopped_state()), seeding_policy="advisory")
                finding = next(item for item in result["diagnostics"] if item["code"] == "E_INTERNAL_AUDIT_VOICE")
                self.assertEqual(finding["severity"], "error")

    def test_lh6_seed_chain_overload_moves_product_layers_to_replies(self) -> None:
        overloaded_state = as_lh6(stopped_state(first_s_level="S1"))
        first = overloaded_state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        first["main_moves"] = ["need", "product"]
        first["seed_layers"]["main"] = ["need", "product"]
        overloaded = self.run_case(
            "如果常拍舞台，4P的60mm实体中焦能少靠后期裁切，不过不常拍远处就没必要选4P",
            overloaded_state,
        )
        self.assertIn("E_SEED_CHAIN_OVERLOAD", self.semantic_codes(overloaded))

        split_group = group_context(
            1,
            mode="scenario_fit",
            claim_id="shared_slow_motion_mode",
            target_model="pocket_4p",
            basis="product",
            benefit="回看时至少能少拖几次进度条",
            condition="常拍拳击",
            boundary="这条没写具体帧率",
            s_level="S2",
        )
        split_state = as_lh6(
            state_for(
                split_group,
                model_level="M0",
                confirmed_model="unknown",
                n_level="N1",
                scene_tags=["fast_action"],
                f_level="F0",
                p_level="P1",
                verified_claims=["shared_slow_motion_mode"],
                causal_cap="S0",
                scenario_cap="S2",
            )
        )
        split_first = split_state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        split_first["main_moves"] = ["need"]
        split_first["seed_layers"] = {"main": ["need"], "replies": ["product", "benefit", "boundary"]}
        split = draft_from_groups(
            [
                (
                    "拍拳击最烦动作只剩一团影",
                    [
                        "常拍拳击的话，这种情况我会看Pocket的慢动作",
                        "回看时至少能少拖几次进度条",
                        "不过这条没写具体帧率，先别猜最高档",
                    ],
                ),
                ("柜台签字那下没忍住笑", ["停顿很真实", "前半句也好笑"]),
                ("最后那个回头我又看了一遍", ["差点划走", "我更喜欢前一秒"]),
            ]
        )
        split_codes = self.semantic_codes(self.run_draft(split, split_state))
        self.assertNotIn("E_SEED_CHAIN_OVERLOAD", split_codes)
        self.assertEqual(split_codes, set())

    def test_lh6_conditional_seed_formula_allows_two_and_rejects_third(self) -> None:
        state = as_lh6(stopped_state())
        for group in state["block_allocations"][0]["persuasion_allocations"][0]["groups"]:
            group["main_moves"] = ["need", "product"]
            group["seed_layers"]["main"] = ["need", "product"]

        two = draft_from_groups(
            [
                ("如果常拍舞台，Pocket能少错过表情", ["这个距离最纠结", "也看站位"]),
                ("要是常拍宠物，4P会更容易跟上", ["跑起来最难", "我更关心室内"]),
                ("最后那个回头我又看了一遍", ["差点划走", "前一秒也好笑"]),
            ]
        )
        self.assertNotIn("E_SEED_FORMULA_REPEAT", self.semantic_codes(self.run_draft(two, state)))

        three = draft_from_groups(
            [
                ("如果常拍舞台，Pocket能少错过表情", ["这个距离最纠结", "也看站位"]),
                ("要是常拍宠物，4P会更容易跟上", ["跑起来最难", "我更关心室内"]),
                ("如果常拍训练，Pocket能少错过动作", ["回放才是重点", "也得看光线"]),
            ]
        )
        findings = [
            item for item in self.run_draft(three, state)["diagnostics"] if item["code"] == "E_SEED_FORMULA_REPEAT"
        ]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["locations"][0]["group"], 3)

    def test_lh6_datong_raw_clip_question_is_valid_s1_without_causality(self) -> None:
        first = group_context(1, mode="attributed", target_model="pocket_4p", s_level="S1")
        state = state_for(
            first,
            model_level="M1",
            claimed_model="pocket_4p",
            confirmed_model="unknown",
            n_level="N0",
            p_level="P0",
            causal_cap="S1",
            scenario_cap="S0",
            strong_group=None,
            under_target_reason="只够转述作者型号并提出原片问题",
            evidence_stop_ids=["test"],
        )
        state = as_lh6(state)
        first = state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        first["main_moves"] = ["question", "product"]
        first["seed_layers"]["main"] = ["question", "product"]
        result = self.run_case(
            "正文说这趟用4P拍，我更想看进门那段原片：外面那么亮，走进去要不要停下来调曝光？",
            state,
        )
        codes = self.semantic_codes(result)
        self.assertNotIn("E_MAIN_TRIPLE_ENUM", codes)
        self.assertNotIn("W_CLOSED_COPY", codes)
        self.assertNotIn("E_SEED_CHAIN_OVERLOAD", codes)
        self.assertNotIn("E_CURRENT_MODEL_BELOW_M2", codes)

    def test_lh6_closed_copy_exempts_verified_f2_operation_result(self) -> None:
        claim_id = "shared_intelligent_tracking"
        strong = group_context(
            1,
            mode="causal",
            claim_id=claim_id,
            target_model="pocket_4p",
            basis="product",
            benefit="自己拍也能少重来一次",
            sources=["operation:t01:打开智能跟随", "result:t01:横移时取景框跟住"],
            s_level="S2",
        )
        state = state_for(
            strong,
            model_level="M2",
            confirmed_model="pocket_4p",
            n_level="N1",
            scene_tags=["remote_moving_subject"],
            f_level="F2",
            feature_claims=[claim_id],
            p_level="P2",
            verified_claims=[claim_id],
            causal_cap="S3",
            scenario_cap="S3",
        )
        state = as_lh6(state)
        first = state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        first["main_moves"] = ["observation", "benefit"]
        first["seed_layers"]["main"] = ["benefit"]
        main = "先点开智能跟随，人物横移时取景框还跟着，最后自己拍也能少重来一次"
        self.assertNotIn("W_CLOSED_COPY", self.semantic_codes(self.run_case(main, state)))

        not_linked = json.loads(json.dumps(state, ensure_ascii=False))
        not_linked_first = not_linked["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        not_linked_first["evidence_sources"] = ["operation:t01:打开智能跟随", "result:t02:横移时取景框跟住"]
        self.assertIn("W_CLOSED_COPY", self.semantic_codes(self.run_case(main, not_linked)))

        weak_model = json.loads(json.dumps(state, ensure_ascii=False))
        weak_model["block_allocations"][0]["persuasion_allocations"][0]["model_status"]["level"] = "M1"
        self.assertIn("W_CLOSED_COPY", self.semantic_codes(self.run_case(main, weak_model)))

        unverified = json.loads(json.dumps(state, ensure_ascii=False))
        unverified["block_allocations"][0]["persuasion_allocations"][0]["fact_status"]["verified_claim_ids"] = []
        self.assertIn("W_CLOSED_COPY", self.semantic_codes(self.run_case(main, unverified)))

    def test_lh6_two_object_contrast_and_grounded_short_meme_pass(self) -> None:
        state = as_lh6(stopped_state())
        first = state["block_allocations"][0]["persuasion_allocations"][0]["groups"][0]
        first["main_moves"] = ["preference", "joke"]
        first["light_meme_anchor"] = first["main_anchor_ids"][0]
        result = self.run_case("我选门洞不选屋檐，15秒根本不够看", state)
        codes = self.semantic_codes(result)
        self.assertNotIn("E_MAIN_TRIPLE_ENUM", codes)
        self.assertNotIn("W_CLOSED_COPY", codes)
        self.assertNotIn("E_LH6_GROUP_SCHEMA", codes)

    def test_lh6_keeps_lh5_claim_registry_version(self) -> None:
        state = as_lh6(stopped_state())
        self.assertEqual(state["claim_registry_version"], "2026-09-02-LH5")
        result = self.run_case("门口那下挺好笑", state)
        self.assertNotIn("E_CLAIM_REGISTRY_VERSION", self.semantic_codes(result))


class LH7DeliveryTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft

    @staticmethod
    def codes(result: dict) -> set[str]:
        return {item["code"] for item in result["diagnostics"]}

    @staticmethod
    def allocation(state: dict) -> dict:
        return state["block_allocations"][0]["persuasion_allocations"][0]

    @staticmethod
    def known_model_state(model: str = "pocket_3") -> dict:
        state = as_lh7(stopped_state())
        LH7DeliveryTests.allocation(state)["model_status"].update(
            {"level": "M2", "confirmed_model": model, "claimed_model": model, "evidence_type": "ui_confirmed"}
        )
        return state

    def test_lh7_default_three_groups_two_replies_has_no_quantity_warnings(self) -> None:
        state = as_lh7(stopped_state())
        del state["delivery_mode"]  # with_replies is backwards-compatible default.
        result = self.run_draft(lh7_draft(), state)
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])
        self.assertFalse(any(code.startswith("W_REPLY_") for code in self.codes(result)))
        self.assertNotIn("E_TWO_CLEAR_ONE_HIDDEN", self.codes(result))

    def test_lh7_batch_keeps_real_label_position_repetition_without_class_quotas(self) -> None:
        state = self.known_model_state()
        source = self.allocation(state)
        allocations = []
        drafts = []
        for number in range(1, 11):
            allocation = json.loads(json.dumps(source))
            allocation["id"] = f"test{number}"
            allocation["section_number"] = str(number)
            allocation["canonical_url"] = f"https://www.xiaohongshu.com/explore/test{number}"
            allocations.append(allocation)
            draft = lh7_draft(["你给Pocket3挪了半张桌子哈哈", "杯子这下比p3抢镜", "猫在等大疆Pocket3摆好"])
            drafts.append(draft.replace("## 小红书 1｜", f"## 小红书 {number}｜").replace("/explore/test", f"/explore/test{number}"))
        state["block_allocations"][0]["persuasion_allocations"] = allocations
        state["evidence_stop_ids"] = [allocation["id"] for allocation in allocations]
        result = self.run_draft("\n".join(drafts), state)
        codes = self.codes(result)
        self.assertFalse(codes & {"W_PRODUCT_SLOT", "W_PRODUCT_ARRANGEMENT", "W_PRODUCT_ARRANGEMENT_RUN", "W_FULL_PRODUCT_ROLLING"})
        self.assertFalse(any(code.startswith("W_REPLY_COUNT") or code.startswith("W_REPLY_COMBO") for code in codes))
        self.assertIn("W_PRODUCT_LABEL_POSITION_RUN", codes)
        self.assertIn("E_EXACT_MAIN", codes)

    def test_lh7_different_aliases_name_the_same_confirmed_model(self) -> None:
        for full, short, model in [("Pocket2", "p2", "pocket_2"), ("Pocket3", "p3", "pocket_3"), ("Pocket4", "p4", "pocket_4"), ("Pocket4P", "4P", "pocket_4p")]:
            with self.subTest(model=model):
                draft = lh7_draft([
                    f"你给{full}挪了半张桌子哈哈",
                    f"杯子都没摆稳就开始给{short}找位置了",
                    f"旁边那只猫好像也在等大疆{full}摆好",
                ])
                result = self.run_draft(draft, self.known_model_state(model))
                self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])

    def test_lh7_name_is_required_in_main_not_only_replies(self) -> None:
        for main in ["这台也太抢镜了", "它占了半张桌子", "大疆这次这么拍", "华为p3还挺抢镜", "手机p3还挺抢镜", "飞宇Pocket3很抢镜", "p3手机还挺抢镜", "看这个https://example.com/Pocket3"]:
            with self.subTest(main=main):
                draft = lh7_draft().replace("你给Pocket挪了半张桌子哈哈", main).replace("杯子先委屈一下", "Pocket放那儿刚好")
                self.assertIn("E_MAIN_PRODUCT_NAME_MISSING", self.codes(self.run_draft(draft, as_lh7(stopped_state()))))

    def test_lh7_repeat_name_normalizes_case_and_spaces(self) -> None:
        result = self.run_draft(lh7_draft(["你给Pocket3挪了半张桌子", "这下POCKET 3真抢镜", "猫在等大疆Pocket3摆好"]), self.known_model_state())
        self.assertIn("E_MAIN_PRODUCT_NAME_REPEAT", self.codes(result))
        self.assertIn("E_PRODUCT_INTERNAL_SPACE", self.codes(result))

    def test_lh7_name_changes_cannot_switch_or_guess_generation(self) -> None:
        draft = lh7_draft(["你给Pocket3挪了半张桌子", "杯子这下比p4抢镜", "猫还在等大疆Pocket3摆好"])
        result = self.run_draft(draft, self.known_model_state())
        self.assertIn("E_MAIN_MODEL_UNGROUNDED", self.codes(result))
        unknown = self.run_draft(lh7_draft(["你给p3挪了半张桌子", "杯子这下比大疆Pocket抢镜", "猫还在等OsmoPocket摆好"]), as_lh7(stopped_state()))
        self.assertIn("E_MAIN_MODEL_UNGROUNDED", self.codes(unknown))

    def test_lh7_competing_p3_does_not_inflate_pocket_model_or_canon(self) -> None:
        fact_models = CHECKER.extract_models(CHECKER.lh7_fact_text("华为p3手机对比Pocket2"), lh7=True)
        self.assertEqual(fact_models, {"pocket_2"})
        self.assertNotEqual(CHECKER.canonical("华为p3手机那个位置刚好", lh7=True), CHECKER.canonical("华为Pocket3手机那个位置刚好", lh7=True))
        self.assertEqual(CHECKER.extract_models(CHECKER.lh7_fact_text("看这个https://example.com/p3"), lh7=True), set())

    def test_lh7_product_spaces_are_checked_in_replies_and_competitors(self) -> None:
        for text in ["DJI Osmo Pocket 3放那里", "我在看p 3", "Osmo Pocket放那儿", "iPhone 16 Pro也能试试", "Insta360 GO 3放那儿", "GoPro HERO 13那个位置"]:
            with self.subTest(text=text):
                draft = lh7_draft().replace("杯子先委屈一下", text)
                self.assertIn("E_PRODUCT_INTERNAL_SPACE", self.codes(self.run_draft(draft, as_lh7(stopped_state()))))
        self.assertNotIn("E_PRODUCT_INTERNAL_SPACE", self.codes(self.run_draft(lh7_draft().replace("杯子先委屈一下", "Insta360 looks fine"), as_lh7(stopped_state()))))

    def test_lh7_sentence_period_is_blocked_in_both_body_roles(self) -> None:
        for fragment in ["哈哈。", "哈哈.", "哈哈. 还有后半句", "哈哈.”", "哈哈．", "哈哈.😂", "哈哈.!", "哈哈.?", "哈哈.🌷"]:
            with self.subTest(fragment=fragment):
                for source in ["你给Pocket挪了半张桌子哈哈", "杯子先委屈一下"]:
                    draft = lh7_draft().replace(source, source + fragment)
                    self.assertIn("E_COPY_SENTENCE_PERIOD", self.codes(self.run_draft(draft, as_lh7(stopped_state()))))

    def test_lh7_legal_decimal_url_ellipsis_and_ordinary_english_survive(self) -> None:
        for fragment in ["2.5秒那里", "到这儿我都看了3.14遍", "...", "…", "……", "https://example.com/a.v2.mp4?x=1.5", "so cute", "IMG_001.MP4"]:
            with self.subTest(fragment=fragment):
                draft = lh7_draft().replace("杯子先委屈一下", fragment)
                result = self.run_draft(draft, as_lh7(stopped_state()))
                self.assertNotIn("E_COPY_SENTENCE_PERIOD", self.codes(result))
                self.assertNotIn("E_PRODUCT_INTERNAL_SPACE", self.codes(result))
        self.assertTrue(CHECKER.lh7_has_sentence_period("https://example.com/a.mp4."))

    def test_lh7_format_only_audits_body_not_heading_notes_or_history(self) -> None:
        draft = "# DJI Osmo Pocket 3范本。\n\n说明：这里保留正常句号。\n\n" + lh7_draft()
        result = self.run_draft(draft, as_lh7(stopped_state()), baseline_value=draft_text("旧稿里的Pocket 3句号。"))
        self.assertNotIn("E_COPY_SENTENCE_PERIOD", self.codes(result))
        self.assertNotIn("E_PRODUCT_INTERNAL_SPACE", self.codes(result))
        self.assertNotIn("E_MAIN_PRODUCT_NAME_MISSING", self.codes(result))

    def test_lh7_reduced_delivery_requires_reason_and_matching_context_count(self) -> None:
        for count in [1, 2]:
            with self.subTest(count=count):
                mains = ["你给Pocket挪了半张桌子哈哈", "杯子这下比大疆Pocket抢镜"][:count]
                state = as_lh7(stopped_state(), count=count)
                result = self.run_draft(lh7_draft(mains), state)
                self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])
                self.allocation(state)["reduced_output_reason"] = " "
                self.assertIn("E_REDUCED_OUTPUT_REASON", self.codes(self.run_draft(lh7_draft(mains), state)))
        mismatched = self.run_draft(lh7_draft(["你给Pocket挪了半张桌子哈哈"]), as_lh7(stopped_state()))
        self.assertIn("E_LH7_GROUP_CONTEXT_COUNT", self.codes(mismatched))

    def test_lh7_main_only_has_no_replies_but_retains_count_checks(self) -> None:
        for count in [1, 2, 3]:
            state = as_lh7(stopped_state(), count=count, main_only=True)
            mains = ["你给Pocket挪了半张桌子哈哈", "杯子这下比大疆Pocket抢镜", "猫还在等OsmoPocket摆好"][:count]
            result = self.run_draft(lh7_draft(mains, main_only=True), state)
            self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])
            self.assertEqual(result["summary"]["replies"], 0)
        self.assertIn("E_REPLY_COUNT", self.codes(self.run_draft(lh7_draft(), as_lh7(stopped_state(), main_only=True))))
        self.assertIn("E_REPLY_COUNT", self.codes(self.run_draft(lh7_draft(main_only=True), as_lh7(stopped_state()))))
        for mode in ["silent", None, [], {}]:
            with self.subTest(mode=mode):
                invalid = as_lh7(stopped_state())
                invalid["delivery_mode"] = mode
                self.assertIn("E_LH7_DELIVERY_MODE", self.codes(self.run_draft(lh7_draft(), invalid)))

    def test_lh7_open_interaction_needs_no_manufactured_answer_or_disagreement(self) -> None:
        draft = lh7_draft(["给Pocket铺那块布是怕它滑下来吗？", "杯子晃那下比大疆Pocket还抢镜", "猫在等OsmoPocket摆好"])
        result = self.run_draft(draft, as_lh7(stopped_state()))
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])
        self.assertNotIn("W_SEED_QUESTION_ONLY", self.codes(result))

    def test_lh7_alias_swapping_is_still_canonical_duplication_across_drafts(self) -> None:
        current = lh7_draft(["我看p3摆在那个角落反而刚好", "杯子这下比大疆Pocket3抢镜", "猫还在等OsmoPocket3摆好"])
        historical = lh7_draft(["我看Pocket3摆在那个角落反而刚好", "柜台签字这下挺有意思", "最后回头的半秒还没看够"])
        result = self.run_draft(current, self.known_model_state(), baseline_value=historical)
        self.assertIn("E_BASELINE_CANON_MAIN", self.codes(result))
        local = lh7_draft(["我看p3摆在那个角落反而刚好", "我看大疆Pocket3摆在那个角落反而刚好", "猫还在等OsmoPocket3摆好"])
        self.assertIn("E_CANON_MAIN", self.codes(self.run_draft(local, self.known_model_state())))

    def test_lh7_keeps_lh6_anchor_and_load_contract(self) -> None:
        state = as_lh7(stopped_state())
        first = self.allocation(state)["groups"][0]
        first["main_anchor_ids"] = ["a", "b"]
        draft = lh7_draft().replace("你给Pocket挪了半张桌子哈哈", "看完Pocket这段我想拍花瓣、树影和门洞")
        codes = self.codes(self.run_draft(draft, state))
        self.assertIn("E_LH6_GROUP_SCHEMA", codes)
        self.assertIn("E_MAIN_TRIPLE_ENUM", codes)
        self.assertNotIn("E_CLAIM_REGISTRY_VERSION", codes)
        loaded_state = self.known_model_state()
        loaded_group = self.allocation(loaded_state)["groups"][0]
        loaded_group["main_moves"] = ["need", "product"]
        loaded_group["seed_layers"]["main"] = ["need", "product"]
        loaded = lh7_draft(["如果常拍舞台，p3能少靠后期裁切，不过不常拍就没必要选它", "杯子这下比大疆Pocket3抢镜", "猫还在等OsmoPocket3摆好"])
        self.assertIn("E_SEED_CHAIN_OVERLOAD", self.codes(self.run_draft(loaded, loaded_state)))

    def test_lh7_p4_alias_does_not_bypass_existing_fact_gates(self) -> None:
        draft = lh7_draft(["p4有60mm实体中焦", "杯子这下比Pocket4抢镜", "猫还在等大疆Pocket4摆好"])
        codes = self.codes(self.run_draft(draft, self.known_model_state("pocket_4")))
        self.assertIn("E_MODEL_FEATURE_MISMATCH", codes)
        optical = draft.replace("p4有60mm实体中焦", "p4有2倍光学变焦")
        self.assertIn("E_DIGITAL_ZOOM_WRITTEN_AS_OPTICAL", self.codes(self.run_draft(optical, self.known_model_state("pocket_4"))))

    def test_lh7_older_model_does_not_inherit_newer_registered_claim(self) -> None:
        state = self.known_model_state("pocket_2")
        self.allocation(state)["groups"][0].update({"claim_id": "4p_physical_60mm", "target_model": "pocket_2"})
        draft = lh7_draft(["p2有60mm实体中焦", "杯子这下比Pocket2抢镜", "猫还在等大疆Pocket2摆好"])
        result = self.run_draft(draft, state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.codes(result))
        self.assertNotIn("E_MODEL_STATUS_INVALID", self.codes(result))
        self.assertNotIn("E_CLAIM_REGISTRY_VERSION", self.codes(result))

    def test_lh7_m1_author_model_requires_attribution_for_current_clip_assertion(self) -> None:
        state = self.known_model_state("pocket_2")
        self.allocation(state)["model_status"].update({"level": "M1", "confirmed_model": "unknown", "evidence_type": "author_claim"})
        self.allocation(state)["groups"][0]["claim_mode"] = "attributed"
        draft = lh7_draft(["博主说这段是p2拍的", "杯子这下比Pocket2抢镜", "猫还在等大疆Pocket2摆好"])
        result = self.run_draft(draft, state)
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])
        independent = self.run_draft(draft.replace("博主说这段是p2拍的", "这段就是p2拍的"), state)
        self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(independent))

    def test_lh7_known_official_scenario_can_be_discussed_in_reply_to_unknown_post(self) -> None:
        strong = group_context(1, mode="scenario_fit", claim_id="4p_physical_60mm", target_model="pocket_4p", basis="product", benefit="不用为了表情往前挤", condition="经常拍舞台表情", s_level="S2")
        state = as_lh7(state_for(strong, model_level="M0", confirmed_model="unknown", scene_tags=["stage"], verified_claims=["4p_physical_60mm"]))
        self.allocation(state)["groups"][0]["seed_layers"] = {"main": ["product"], "replies": ["need", "product", "benefit"]}
        draft = lh7_draft().replace("你给Pocket挪了半张桌子哈哈", "看完这段有点好奇Pocket拍舞台会是什么样")
        draft = draft.replace("杯子先委屈一下", "经常隔着人群拍舞台表情的话，我会先看4P的60mm实体中焦，不用为了表情往前挤")
        result = self.run_draft(draft, state)
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])

    def test_lh7_rules_do_not_change_lh5_lh6_or_missing_state_behavior(self) -> None:
        draft = draft_text("门口摆得挺整齐。")
        for state in [stopped_state(), as_lh6(stopped_state())]:
            codes = self.codes(self.run_draft(draft, state))
            self.assertNotIn("E_MAIN_PRODUCT_NAME_MISSING", codes)
            self.assertNotIn("E_COPY_SENTENCE_PERIOD", codes)
            self.assertIn("W_REPLY_COUNT_LOCAL", codes)
            fewer = self.run_draft(lh7_draft(["你给Pocket挪了半张桌子"]), state)
            self.assertIn("E_GROUP_COUNT", self.codes(fewer))
        result = LH5SemanticTests.run_case(self, "你给Pocket挪了半张桌子", None)
        self.assertIn("E_SEED_STATE_MISSING", self.codes(result))

    def test_lh7_cli_returns_success_and_copy_gate_failure_with_legacy_policy_off(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            state_path = root / "state.json"
            state_path.write_text(json.dumps(as_lh7(stopped_state()), ensure_ascii=False), encoding="utf-8")
            for text, expected in [(lh7_draft(), 0), (lh7_draft().replace("杯子先委屈一下", "杯子先委屈一下。"), 1)]:
                with self.subTest(expected=expected):
                    draft.write_text(text, encoding="utf-8")
                    output = io.StringIO()
                    with redirect_stdout(output):
                        exit_code = CHECKER.main([str(draft), "--state", str(state_path), "--product-policy", "off", "--seeding-policy", "strict", "--format", "json"])
                    self.assertEqual(exit_code, expected, output.getvalue())
                    self.assertEqual(json.loads(output.getvalue())["summary"]["sections"], 1)


class LH8PersonalNeedTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft
    codes = staticmethod(LH7DeliveryTests.codes)
    allocation = staticmethod(LH7DeliveryTests.allocation)

    def run_main(self, main: str, state: dict | None = None, replies: list[str] | None = None) -> dict:
        return self.run_draft(draft_from_groups([(main, replies or [])]), state or personal_state())

    def assert_clean(self, result: dict) -> None:
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])

    def test_lh8_user_example_uses_sourced_personal_model_and_tutorial_value(self) -> None:
        state = personal_state(model="pocket_4p", facts=["刚入手4p，十一去云南，担心不会使用"])
        result = self.run_main("我刚刚入手了4p正准备十一去云南旅游使用，本来还害怕不会使用这不瞌睡送来了枕头", state)
        self.assert_clean(result)
        self.assertNotIn("W_SEED_ZERO_PROXY", self.codes(result))
        self.assertEqual(self.allocation(state)["model_status"]["level"], "M0")
        self.assertEqual(self.allocation(state)["scenario_fit_cap"], "S0")
        self.assertEqual(self.allocation(state)["groups"][0]["actual_s_level"], "S1")

    def test_lh8_n0_need_needs_no_question_feature_purchase_or_strong_slot(self) -> None:
        result = self.run_main("纸箱先别扔，想用Pocket试试你这个空房变满房的转场")
        self.assert_clean(result)
        self.assertTrue({"E_EVIDENCE_STOP_MISSING", "E_STRONG_SEED_GROUP_UNSET", "W_SEED_ZERO_PROXY", "W_SEED_QUESTION_ONLY"}.isdisjoint(self.codes(result)))

    def test_lh8_valid_post_scene_does_not_force_strong_seed(self) -> None:
        state = personal_state()
        self.allocation(state)["scene_need"].update(level="N1", tags=["travel"], evidence="原帖讨论出游准备")
        self.allocation(state)["scenario_fit_cap"] = "S1"
        self.assert_clean(self.run_main("Pocket也想照着你这个顺序摆好再出门", state))

    def test_lh8_declared_strong_seed_is_still_verified(self) -> None:
        state = personal_state()
        self.allocation(state)["strong_seed_group"] = 1
        result = self.run_main("想拿Pocket试试你这个纸箱转场", state)
        self.assertIn("E_STRONG_SEED_GROUP_INVALID", self.codes(result))

    def test_lh8_need_connection_is_required(self) -> None:
        for value in [None, "", "  ", []]:
            with self.subTest(value=value):
                state = personal_state()
                self.allocation(state)["groups"][0]["need_connection"] = value
                self.assertIn("E_PERSONAL_NEED_CONNECTION_MISSING", self.codes(self.run_main("想拿Pocket试试纸箱转场", state)))

    def test_lh8_personal_context_has_strict_source_fact_and_model_types(self) -> None:
        for value in [{}, "user said", {"source_ref": "", "facts": ["刚买"], "models": ["pocket_3"]}, {"source_ref": "user:1", "facts": [], "models": ["pocket_3"]}, {"source_ref": "user:1", "facts": ["刚买"], "models": "pocket_3"}, {"source_ref": "user:1", "facts": ["刚买"], "models": ["unknown"]}]:
            with self.subTest(value=value):
                state = personal_state()
                self.allocation(state)["groups"][0]["personal_context"] = value
                codes = self.codes(self.run_main("我刚买p3，正好学你这招", state))
                self.assertIn("E_PERSONAL_CONTEXT_INVALID", codes)
                self.assertIn("E_MAIN_MODEL_UNGROUNDED", codes)

    def test_lh8_personal_models_do_not_leak_to_other_groups(self) -> None:
        state = personal_state(count=2, model="pocket_3", facts=["我刚买p3"])
        result = self.run_draft(draft_from_groups([("我刚买p3，今晚试试纸箱转场", []), ("想用Pocket3拍房间变化", [])]), state)
        errors = [d for d in result["diagnostics"] if d["code"] == "E_MAIN_MODEL_UNGROUNDED"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["locations"][0]["group"], 2)

    def test_lh8_personal_model_does_not_identify_original_camera(self) -> None:
        for main in ["原片就是p3拍的，我也要这样录", "我觉得这段就是p3拍的", "这段是p3拍的，我刚买的p3也试试"]:
            with self.subTest(main=main):
                state = personal_state(model="pocket_3", facts=["刚买p3"])
                self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(self.run_main(main, state)))

    def test_lh8_personal_source_cannot_name_creators_unknown_device(self) -> None:
        state = personal_state(model="pocket_3", facts=["用户已有p3"])
        self.assertIn("E_MAIN_MODEL_UNGROUNDED", self.codes(self.run_main("你手里的p3也想照这个位置摆好", state)))
        self.assert_clean(self.run_main("看你这个摆位，我的p3也想这样摆好", state))

    def test_lh8_sourced_personal_photo_is_not_original_camera_attribution(self) -> None:
        state = personal_state(model="pocket_3", facts=["我上次用p3拍的旅行片一直没剪"])
        self.assert_clean(self.run_main("我上次用p3拍的旅行片还没剪，你这个先排顺序的办法今晚试试", state))

    def test_lh8_reply_does_not_inherit_main_authors_personal_camera(self) -> None:
        state = personal_state(main_only=False, model="pocket_3", facts=["我刚买p3"])
        result = self.run_main("我刚买p3，先学你这个摆位", state, ["我上次用p3拍的那段也很好看", "这个角度可以学学"])
        self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(result))
        self.assertNotIn("E_CURRENT_MODEL_BELOW_M2", self.codes(result))

    def test_lh8_replies_with_explicit_history_need_their_own_sources(self) -> None:
        state = personal_state(main_only=False, model="pocket_3", facts=["我刚买p3"])
        for reply in ["我也有p3", "我家猫也这样"]:
            with self.subTest(reply=reply):
                result = self.run_main("我刚买p3，先学你这个摆位", state, [reply, "这个角度可以学学"])
                self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(result))
                self.assertNotIn("E_CURRENT_MODEL_BELOW_M2", self.codes(result))

    def test_lh8_sourced_reply_recollection_is_not_original_clip_attribution(self) -> None:
        state = personal_state(main_only=False)
        self.allocation(state)["groups"][0]["reply_personal_contexts"] = {"1": {"source_ref": "user:reply-author-1", "facts": ["上次用p3拍过旅行片"], "models": ["pocket_3"]}}
        result = self.run_main("Pocket也想照这个摆位试试", state, ["我上次用p3拍的那段也很好看", "这个角度可以学学"])
        self.assert_clean(result)

    def test_lh8_reply_sources_do_not_leak_to_next_reply_or_original_clip(self) -> None:
        state = personal_state(main_only=False)
        self.allocation(state)["groups"][0]["reply_personal_contexts"] = {"1": {"source_ref": "user:reply-author-1", "facts": ["我有p3"], "models": ["pocket_3"]}}
        result = self.run_main("Pocket也想照这个摆位试试", state, ["我也有p3", "我也刚入手p3"])
        missing = [d for d in result["diagnostics"] if d["code"] == "E_REPLY_PERSONAL_CONTEXT_MISSING"]
        self.assertEqual([d["metrics"]["reply"] for d in missing], [2])
        result = self.run_main("Pocket也想照这个摆位试试", state, ["原片就是p3拍的", "这个角度可以学学"])
        self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(result))

    def test_lh8_reply_context_keys_and_values_must_match_actual_replies(self) -> None:
        context = {"source_ref": "user:reply-1", "facts": ["我有p3"], "models": ["pocket_3"]}
        for value in [None, [], {"0": context}, {"3": context}, {"01": context}, {"1": None}, {"1": {}}, {"1": {"source_ref": "", "facts": ["我有p3"], "models": ["pocket_3"]}}]:
            with self.subTest(value=value):
                state = personal_state(main_only=False)
                self.allocation(state)["groups"][0]["reply_personal_contexts"] = value
                self.assertIn("E_REPLY_PERSONAL_CONTEXT_INVALID", self.codes(self.run_main("Pocket也想照这个摆位试试", state, ["这个角度挺好", "先记下来"])))

    def test_lh8_reply_personal_model_must_belong_to_its_own_source(self) -> None:
        state = personal_state(main_only=False, model="pocket_3", facts=["用户主评作者有p3"])
        self.allocation(state)["groups"][0]["reply_personal_contexts"] = {"1": {"source_ref": "user:reply-author-1", "facts": ["回复作者有p4"], "models": ["pocket_4"]}}
        self.assertIn("E_REPLY_PERSONAL_MODEL_UNGROUNDED", self.codes(self.run_main("我的p3也想这样摆好", state, ["我也有p3", "记下这个位置"])))

    def test_lh8_current_reply_ideas_need_no_personal_context(self) -> None:
        state = personal_state(main_only=False)
        result = self.run_main("Pocket也想照这个摆位试试", state, ["我想试试从拆纸箱开始拍", "我不知道怎么摆，这个位置看明白了"])
        self.assert_clean(result)

    def test_lh8_owned_reply_model_does_not_turn_desired_upgrade_into_history(self) -> None:
        state = personal_state(main_only=False)
        self.allocation(state)["groups"][0]["reply_personal_contexts"] = {"1": {"source_ref": "user:reply-author-1", "facts": ["我有p3"], "models": ["pocket_3"]}}
        for reply in ["我也有p3，想换4p试试", "我也有p3但想换4p试试"]:
            with self.subTest(reply=reply):
                self.assert_clean(self.run_main("Pocket也想照这个摆位试试", state, [reply, "先学这个位置"]))

    def test_lh8_device_pronoun_cannot_hide_hardware_claim_after_comma(self) -> None:
        for main in ["Pocket想买，它支持8K240fps", "Pocket想买，这台支持8K240fps", "Pocket想买，而且它支持8K240fps"]:
            with self.subTest(main=main):
                self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(self.run_main(main)))
        state = personal_state(main_only=False)
        self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(self.run_main("Pocket想照着这个转场拍", state, ["它支持8K240fps", "今晚试试"])))

    def test_lh8_personal_relief_after_tutorial_is_not_device_pronoun_claim(self) -> None:
        result = self.run_main("Pocket的设置这段视频讲清楚了，我终于能开始拍，下次试试你这个位置")
        self.assert_clean(result)
        self.assertNotIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(result))

    def test_lh8_explicit_history_requires_personal_source_but_current_thought_does_not(self) -> None:
        for main in ["我刚入手Pocket，正好学你这招", "我家猫也这样，想拿Pocket录下来", "Pocket用了几年，拍法还得跟你学"]:
            with self.subTest(main=main):
                self.assertIn("E_PERSONAL_CONTEXT_MISSING", self.codes(self.run_main(main)))
        for main in ["准备入手Pocket，你这个纸箱转场想试试", "我想买Pocket拍这个转场", "我不知道怎么用Pocket，你这段终于讲清楚了", "看你说“我刚买Pocket”，这个反应太好玩了", "看你说我刚买Pocket这个表情，我也想试试"]:
            with self.subTest(main=main):
                self.assertNotIn("E_PERSONAL_CONTEXT_MISSING", self.codes(self.run_main(main)))

    def test_lh8_s1_cannot_hide_hardware_assertions_in_main_or_reply(self) -> None:
        state = personal_state(model="pocket_3", facts=["用户已有p3"])
        self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(self.run_main("p3支持4K拍摄，下次想试试", state)))
        state["delivery_mode"] = "with_replies"
        result = self.run_main("p3也想照你这个顺序摆好", state, ["Pocket3支持4K拍摄", "今晚试试"])
        self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(result))
        self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(self.run_main("p3能8K240fps拍摄", personal_state(model="pocket_3"))))
        self.assertIn("E_PERSONAL_NEED_PRODUCT_ASSERTION", self.codes(self.run_main("Pocket有云台，旅行不用折腾了")))

    def test_lh8_s1_cannot_hide_registered_false_parameter(self) -> None:
        state = personal_state(model="pocket_4", facts=["已有p4"])
        result = self.run_main("p4有60mm实体中焦，正好去云南用", state)
        self.assertIn("E_MODEL_FEATURE_MISMATCH", self.codes(result))

    def test_lh8_personal_need_cannot_assert_current_result_causality(self) -> None:
        state = personal_state(model="pocket_3", facts=["已有p3"])
        result = self.run_main("这段靠p3的云台才拍成这样，正好旅行用", state)
        self.assertIn("E_PERSONAL_NEED_CURRENT_CAUSALITY", self.codes(result))

    def test_lh8_tutorial_clarity_is_not_hardware_causality_or_marketing_overload(self) -> None:
        state = personal_state(model="pocket_4p", facts=["已有4p，准备旅行"])
        result = self.run_main("这段就是把4p的参数讲清楚了，想试的拍法终于知道怎么设置，出门不用瞎猜了", state)
        self.assert_clean(result)
        self.assertNotIn("E_SEED_CHAIN_OVERLOAD", self.codes(result))

    def test_lh8_personal_need_rejects_s2_product_basis_and_claim_id(self) -> None:
        for change in [{"target_s_level": "S2", "actual_s_level": "S2"}, {"benefit_basis": "product"}, {"claim_id": "pocket_mechanical_stabilization"}, {"claim_id": None}]:
            with self.subTest(change=change):
                state = personal_state()
                self.allocation(state)["groups"][0].update(change)
                self.assertIn("E_PERSONAL_NEED_CONTRACT", self.codes(self.run_main("Pocket也想照你这个转场拍一段", state)))

    def test_lh8_personal_need_does_not_raise_original_caps(self) -> None:
        state = personal_state()
        self.allocation(state)["scenario_fit_cap"] = "S1"
        self.assertIn("E_DECLARED_CAP_EXCEEDS_EVIDENCE", self.codes(self.run_main("Pocket也想试你这个转场", state)))

    def test_lh8_osmo_is_forbidden_case_insensitively_in_both_roles_only(self) -> None:
        for name in ["OsmoPocket", "oSmO", "OSMO"]:
            with self.subTest(name=name):
                self.assertIn("E_COPY_OSMO_NAME", self.codes(self.run_main(f"想拿Pocket学你这个{name}转场")))
                state = personal_state(main_only=False)
                self.assertIn("E_COPY_OSMO_NAME", self.codes(self.run_main("想拿Pocket学你这个转场", state, [name, "这个角度好玩"])))
        state = personal_state(facts=["用户材料保留 DJI Osmo Pocket 官方写法"])
        draft = "# DJI Osmo Pocket 示例。\n说明：Osmo名称只限原材料\n" + draft_from_groups([("想拿Pocket学你这个转场", [])])
        self.assertNotIn("E_COPY_OSMO_NAME", self.codes(self.run_draft(draft, state)))

    def test_lh8_three_generic_names_are_valid_and_repeated_names_still_fail(self) -> None:
        state = personal_state(count=3)
        mains = ["Pocket先别打包，想留个空房转场", "下次用大疆Pocket从集合就开始录", "DJIPocket也想试你这个回头拍法"]
        self.assert_clean(self.run_draft(draft_from_groups([(main, []) for main in mains]), state))
        mains[2] = "POCKET也想试你这个回头拍法"
        self.assertIn("E_MAIN_PRODUCT_NAME_REPEAT", self.codes(self.run_draft(draft_from_groups([(main, []) for main in mains]), state)))

    def test_lh8_retains_format_rules_and_model_grounding(self) -> None:
        for main, code in [("想拿Pocket试试这个转场。", "E_COPY_SENTENCE_PERIOD"), ("想拿DJI Pocket试试这个转场", "E_PRODUCT_INTERNAL_SPACE"), ("想拿p3试试这个转场", "E_MAIN_MODEL_UNGROUNDED"), ("想拿它试试这个转场", "E_MAIN_PRODUCT_NAME_MISSING")]:
            with self.subTest(main=main):
                self.assertIn(code, self.codes(self.run_main(main)))

    def test_lh8_historical_purchases_are_not_purchase_intentions(self) -> None:
        state = personal_state(count=2)
        for group in self.allocation(state)["groups"]:
            group["personal_context"] = {"source_ref": "user:purchase", "facts": ["用户刚入手Pocket"], "models": []}
        draft = draft_from_groups([("我刚刚入手Pocket，先学你这个转场", []), ("我之前下单了大疆Pocket，终于找到想拍的东西", [])])
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertNotIn("W_PUSH_WORD_DENSITY", self.codes(result))
        self.assertEqual(CHECKER.lh8_soft_purchase_terms("想买Pocket，准备入手，考虑下单"), ["想买", "入手", "下单"])

    def test_lh8_new_mode_is_rejected_by_lh7_and_legacy_osmo_remains_accepted(self) -> None:
        state = personal_state()
        state["rule_version"] = "2026-09-05-LH7"
        self.assertIn("E_SEED_GROUP_CONTEXT_INVALID", self.codes(self.run_main("想拿OsmoPocket学你这个转场", state)))
        self.assertNotIn("E_COPY_OSMO_NAME", self.codes(self.run_main("想拿OsmoPocket学你这个转场", state)))

    def test_lh8_preserves_verified_causality_and_rejects_missing_function_evidence(self) -> None:
        claim_id = "shared_slow_motion_mode"
        strong = group_context(1, mode="causal", claim_id=claim_id, target_model="pocket_4", basis="product", benefit="回看不用来回拖", sources=["operation:t01:visible-control", "result:t01:visible-output"], s_level="S2")
        state = as_lh7(state_for(strong, confirmed_model="pocket_4", scene_tags=["fast_action"], f_level="F2", feature_claims=[claim_id], verified_claims=[claim_id], causal_cap="S2"), count=1, main_only=True)
        state["rule_version"] = "2026-09-05-LH8"
        self.allocation(state)["groups"][0]["main_anchor_ids"] = ["t01"]
        main = "Pocket4画面点开慢动作后，舔鼻从一闪变成能看清动作，回看不用来回拖"
        self.assert_clean(self.run_main(main, state))
        self.allocation(state)["feature_use"].update(level="F0", claim_ids=[], evidence="")
        self.allocation(state)["clip_causality_cap"] = "S0"
        result = self.run_main(main, state)
        self.assertIn("E_CAUSAL_CLAIM_BELOW_F2", self.codes(result))


class LH9DialogueTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft
    codes = staticmethod(LH7DeliveryTests.codes)
    allocation = staticmethod(LH7DeliveryTests.allocation)

    def fixture(self, *, main: str = "周末想拿Pocket学你这个转场，纸箱先留着", replies: list[str] | None = None, speakers: list[str] | None = None, parents: list[str] | None = None, main_source: dict | None = None) -> tuple[str, dict]:
        replies = replies if replies is not None else ["纸箱里要不要先放点东西", "放两件衣服就行，搬起来别太费劲"]
        speakers = speakers or ["B", "A"]
        parents = parents or ["main", *[f"reply:{number}" for number in range(1, len(replies))]]
        state = personal_state(main_only=not replies)
        state["rule_version"] = "2026-09-05-LH9"
        group = self.allocation(state)["groups"][0]
        group["personal_context"] = main_source
        group["reply_personal_contexts"] = {}
        turns = []
        lines = ["## 小红书 1｜https://www.xiaohongshu.com/explore/test", f"主评论（A）：{main}"]
        for number, (reply, speaker, parent) in enumerate(zip(replies, speakers, parents), 1):
            parent_index = int(parent.split(":")[1]) - 1 if parent != "main" else None
            parent_speaker = speakers[parent_index] if parent_index is not None else "A"
            parent_body = replies[parent_index] if parent_index is not None else main
            turns.append({"reply": number, "speaker": speaker, "reply_to": parent, "anchor_quote": parent_body[:6], "response_move": "承接上一句再给出一个具体反应"})
            lines.append(f"↳ 回复{number}（{speaker}→{parent_speaker}）：{reply}")
        group["dialogue"] = {"main_speaker": "A", "replies": turns}
        return "\n".join(lines), state

    def source(self, ref: str, models: list[str] | None = None, facts: list[str] | None = None) -> dict:
        return {"source_ref": f"user-material:{ref}", "facts": facts or ["该发布者持有 p3，近期搬家"], "models": models if models is not None else ["pocket_3"]}

    def group(self, state: dict) -> dict:
        return self.allocation(state)["groups"][0]

    def assert_clean(self, result: dict) -> None:
        self.assertEqual(result["summary"]["errors"], 0, result["diagnostics"])

    def test_lh9_aba_source_reuse_and_body_only_parsing(self) -> None:
        draft, state = self.fixture(main="我刚入手了p3，周末想学你这个转场", replies=["纸箱里要不要先放点东西", "我的p3先不装箱了，试完这个再收"], main_source=self.source("A"))
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertTrue(result["dialogue"]["semantic_review_required"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.md"
            path.write_text(draft, encoding="utf-8")
            parsed, _ = CHECKER.parse_file(path)
            self.assertEqual(parsed[0].groups[0].main.speaker, "A")
            self.assertEqual(parsed[0].groups[0].replies[1].speaker, "A")
            self.assertEqual(parsed[0].groups[0].replies[1].reply_target, "B")
            self.assertTrue(parsed[0].groups[0].main.text.startswith("我刚"))
            self.assertNotIn("（A）", parsed[0].groups[0].main.text)

    def test_lh9_abc_needs_no_personal_sources_for_present_ideas(self) -> None:
        draft, state = self.fixture(speakers=["B", "C"])
        self.assert_clean(self.run_draft(draft, state))

    def test_lh9_abc_c_cannot_inherit_a_source(self) -> None:
        draft, state = self.fixture(replies=["纸箱里要不要先放点东西", "我的p3也先不装箱了"], speakers=["B", "C"], main_source=self.source("A"))
        self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh9_bcb_reuses_bs_own_earlier_source(self) -> None:
        draft, state = self.fixture(replies=["我刚入手了p3，想拿纸箱练练", "箱子里要不要先放点东西", "我的p3先不装箱了，试完再收"], speakers=["B", "C", "B"])
        self.group(state)["reply_personal_contexts"] = {"1": self.source("B")}
        self.assert_clean(self.run_draft(draft, state))

    def test_lh9_earlier_reply_cannot_borrow_a_later_source(self) -> None:
        draft, state = self.fixture(replies=["我的p3想试试这个转场", "试完再收起来就行", "我刚入手了p3，正好练练"], speakers=["B", "C", "B"])
        self.group(state)["reply_personal_contexts"] = {"3": self.source("B")}
        result = self.run_draft(draft, state)
        missing = [d for d in result["diagnostics"] if d["code"] == "E_REPLY_PERSONAL_CONTEXT_MISSING"]
        self.assertEqual(len(missing), 1, result["diagnostics"])

    def test_lh9_parallel_main_replies_are_rejected(self) -> None:
        draft, state = self.fixture(speakers=["B", "C"], parents=["main", "main"])
        self.assertIn("E_DIALOGUE_NO_EXCHANGE", self.codes(self.run_draft(draft, state)))

    def test_lh9_self_reply_is_rejected(self) -> None:
        draft, state = self.fixture(speakers=["B", "B"])
        self.assertIn("E_DIALOGUE_SELF_REPLY", self.codes(self.run_draft(draft, state)))

    def test_lh9_first_reply_cannot_be_main_author(self) -> None:
        draft, state = self.fixture(speakers=["A", "B"])
        self.assertIn("E_DIALOGUE_SELF_REPLY", self.codes(self.run_draft(draft, state)))

    def test_lh9_missing_future_and_cyclic_parents_are_rejected(self) -> None:
        for parent in ["reply:2", "reply:3", "reply:0", "reply:99", "reply:1", "other:main", None]:
            with self.subTest(parent=parent):
                draft, state = self.fixture()
                self.group(state)["dialogue"]["replies"][0]["reply_to"] = parent
                self.assertIn("E_DIALOGUE_PARENT", self.codes(self.run_draft(draft, state)))

    def test_lh9_mapping_cannot_be_missing_duplicate_extra_or_reordered(self) -> None:
        for variant in ["missing", "duplicate", "extra", "reorder", "bool", "not_list", "not_object"]:
            with self.subTest(variant=variant):
                draft, state = self.fixture()
                dialogue = self.group(state)["dialogue"]
                turns = dialogue["replies"]
                if variant == "missing": turns.pop()
                elif variant == "duplicate": turns.append(dict(turns[0]))
                elif variant == "extra": turns.append({**turns[0], "reply": 3})
                elif variant == "reorder": turns.reverse()
                elif variant == "bool": turns[0]["reply"] = True
                elif variant == "not_list": dialogue["replies"] = {}
                else: turns[0] = "not an object"
                self.assertIn("E_DIALOGUE_REPLY_MAPPING", self.codes(self.run_draft(draft, state)))

    def test_lh9_anchor_must_come_from_actual_parent(self) -> None:
        for quote in ["纸箱先留着", "关于纸箱的讨论", "", None, 1]:
            with self.subTest(quote=quote):
                draft, state = self.fixture()
                self.group(state)["dialogue"]["replies"][1]["anchor_quote"] = quote
                self.assertIn("E_DIALOGUE_ANCHOR_QUOTE", self.codes(self.run_draft(draft, state)))

    def test_lh9_anchor_cleaning_accepts_unicode_and_whitespace_equivalence(self) -> None:
        draft, state = self.fixture(replies=["纸箱Ａ   先放门口吗", "先留着试一下，别急着收"])
        self.group(state)["dialogue"]["replies"][1]["anchor_quote"] = "纸箱A 先放"
        self.assert_clean(self.run_draft(draft, state))

    def test_lh9_response_move_is_description_not_a_closed_enum(self) -> None:
        draft, state = self.fixture()
        turns = self.group(state)["dialogue"]["replies"]
        turns[0]["response_move"] = "接住纸箱准备这个细节，随口问一下"
        turns[1]["response_move"] = "把东西选好然后顺口收住"
        self.assert_clean(self.run_draft(draft, state))
        turns[1]["response_move"] = " "
        self.assertIn("E_DIALOGUE_RESPONSE_MOVE", self.codes(self.run_draft(draft, state)))

    def test_lh9_labels_must_match_speaker_and_parent_speaker(self) -> None:
        draft, state = self.fixture()
        for before, after in [("主评论（A）", "主评论（B）"), ("回复1（B→A）", "回复1（C→A）"), ("回复2（A→B）", "回复2（A→C）")]:
            with self.subTest(after=after):
                self.assertIn("E_DIALOGUE_LABEL_MISMATCH", self.codes(self.run_draft(draft.replace(before, after), state)))

    def test_lh9_unlabelled_copy_does_not_silently_pass(self) -> None:
        draft, state = self.fixture()
        plain = draft.replace("（A）", "").replace("（B→A）", "").replace("（A→B）", "")
        self.assertIn("E_DIALOGUE_LABEL_MISMATCH", self.codes(self.run_draft(plain, state)))

    def test_lh9_malformed_label_line_is_error_not_ignored_warning(self) -> None:
        draft, state = self.fixture()
        malformed = draft.replace("回复2（A→B）", "回复2【A→B】")
        self.assertIn("E_DIALOGUE_LABEL_INVALID", self.codes(self.run_draft(malformed, state)))

    def test_lh9_dialogue_state_is_required_for_replies(self) -> None:
        draft, state = self.fixture()
        self.group(state).pop("dialogue")
        self.assertIn("E_DIALOGUE_CONTEXT_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh9_main_only_accepts_legacy_unlabelled_main(self) -> None:
        draft, state = self.fixture(replies=[])
        self.group(state).pop("dialogue")
        self.assert_clean(self.run_draft(draft.replace("主评论（A）", "主评论"), state))

    def test_lh9_invalid_speaker_and_main_speaker_are_rejected(self) -> None:
        for speaker in ["博主", "F", "a", [], {}, None]:
            with self.subTest(speaker=speaker):
                draft, state = self.fixture()
                self.group(state)["dialogue"]["replies"][0]["speaker"] = speaker
                self.assertIn("E_DIALOGUE_SPEAKER", self.codes(self.run_draft(draft, state)))
        draft, state = self.fixture()
        self.group(state)["dialogue"]["main_speaker"] = "B"
        self.assertIn("E_DIALOGUE_MAIN_SPEAKER", self.codes(self.run_draft(draft, state)))

    def test_lh9_four_reply_extension_can_revisit_earlier_parent(self) -> None:
        draft, state = self.fixture(replies=["纸箱里放什么", "这里是不是要先搬一下", "放两件衣服行不行", "好像得先把箱盖扣上"], speakers=["B", "C", "A", "E"], parents=["main", "main", "reply:1", "reply:3"])
        self.assert_clean(self.run_draft(draft, state))

    def test_lh9_same_speaker_conflicting_source_is_rejected(self) -> None:
        draft, state = self.fixture(main_source=self.source("A"))
        self.group(state)["reply_personal_contexts"] = {"2": self.source("another-account")}
        self.assertIn("E_DIALOGUE_SOURCE_CONFLICT", self.codes(self.run_draft(draft, state)))

    def test_lh9_cross_speaker_copy_of_source_is_rejected(self) -> None:
        draft, state = self.fixture(speakers=["B", "C"], main_source=self.source("A"))
        self.group(state)["reply_personal_contexts"] = {"2": self.source("A")}
        self.assertIn("E_DIALOGUE_SOURCE_BORROWED", self.codes(self.run_draft(draft, state)))

    def test_lh9_same_source_can_add_reviewable_facts_and_models(self) -> None:
        draft, state = self.fixture(main_source=self.source("A"), replies=["还要换机器拍一段吗", "我刚入手了4p，也想留出来试试"])
        self.group(state)["reply_personal_contexts"] = {"2": self.source("A", ["pocket_4p"], ["同一发布者补充，刚入手了4p"])}
        self.assert_clean(self.run_draft(draft, state))

    def test_lh9_new_personal_model_needs_same_speaker_source_supplement(self) -> None:
        draft, state = self.fixture(main_source=self.source("A"), replies=["还要换机器拍一段吗", "我刚入手了4p，也想留出来试试"])
        self.assertIn("E_REPLY_PERSONAL_MODEL_UNGROUNDED", self.codes(self.run_draft(draft, state)))

    def test_lh9_source_types_and_mapping_still_validated(self) -> None:
        for sources in [[], {"3": self.source("B")}, {"1": None}, {"1": {"source_ref": "", "facts": [], "models": []}}]:
            with self.subTest(sources=sources):
                draft, state = self.fixture()
                self.group(state)["reply_personal_contexts"] = sources
                self.assertIn("E_REPLY_PERSONAL_CONTEXT_INVALID", self.codes(self.run_draft(draft, state)))

    def test_lh9_product_and_format_gates_apply_to_reply_bodies(self) -> None:
        variants = [("想试试OsmoPocket", "E_COPY_OSMO_NAME"), ("想试试Pocket 3", "E_PRODUCT_INTERNAL_SPACE"), ("好像可以试试。", "E_COPY_SENTENCE_PERIOD"), ("Pocket支持防水", "E_PERSONAL_NEED_PRODUCT_ASSERTION")]
        for body, code in variants:
            with self.subTest(body=body):
                draft, state = self.fixture(replies=["你打算怎么试", body])
                self.assertIn(code, self.codes(self.run_draft(draft, state)))

    def test_lh9_personal_source_cannot_identify_original_device(self) -> None:
        draft, state = self.fixture(main_source=self.source("A"), replies=["你打算怎么试", "这段就是Pocket3拍的"])
        self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(self.run_draft(draft, state)))

    def test_lh9_anchor_validity_does_not_certify_semantic_naturalness(self) -> None:
        draft, state = self.fixture(replies=["纸箱里放什么", "镜头的叙事表达让情绪更加饱满"])
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertTrue(result["dialogue"]["semantic_review_required"])
        self.assertIn("互动自然度", result["dialogue"]["note"])

    def test_lh9_structure_gates_are_active_with_seeding_off(self) -> None:
        draft, state = self.fixture(speakers=["B", "C"], parents=["main", "main"])
        with tempfile.TemporaryDirectory() as tmp:
            path, state_path = Path(tmp) / "draft.md", Path(tmp) / "state.json"
            path.write_text(draft, encoding="utf-8")
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = CHECKER.audit([path], state_path=state_path, seeding_policy="off")
            self.assertIn("E_DIALOGUE_NO_EXCHANGE", self.codes(result))


class LH10ExpressionTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft
    codes = staticmethod(LH7DeliveryTests.codes)
    allocation = staticmethod(LH7DeliveryTests.allocation)
    assert_clean = LH9DialogueTests.assert_clean

    def convert(self, state: dict) -> dict:
        state["rule_version"] = "2026-09-05-LH10"
        descriptions = ["调侃猫把开箱镜头抢走", "担心腾桌面时杯子会倒", "希望垫布上的构图停留更久"]
        connections = ["猫盯着正在拆封的Pocket盒子，回应抢镜关系", "挪出Pocket摆位时碰到杯子，回应这一下紧张", "Pocket放在垫布上的镜头成为构图主体，回应停留时长"]
        for group in self.allocation(state)["groups"]:
            group["dominant_expression"] = descriptions[group["group"] - 1]
            group["product_connection"] = connections[group["group"] - 1]
        state["qa"] = {"semantic_review": {"diversity_review": [{"id": "test", "verdict": "passed", "comparison_reason": "逐组并排看：一组调侃抢镜，另一组担忧杯子，最后一组要求画面停留；实际对象与表达目的不同。单组时按其实际主导表达复核。"}]}}
        return state

    def fixture(self, *, count: int = 3) -> tuple[str, dict]:
        state = as_lh7(stopped_state(), count=count, main_only=True)
        state["evidence_stop_ids"] = []
        self.allocation(state)["under_target_reason"] = ""
        mains = ["Pocket这场开箱真正的主角是那只抢镜的猫", "你给大疆Pocket腾位置时杯子晃那一下，看得我跟着屏住气", "DJIPocket放在垫布上那一格留久一点吧，喜欢这个构图"]
        return draft_from_groups([(main, []) for main in mains[:count]]), self.convert(state)

    def dialogue_fixture(self, **kwargs) -> tuple[str, dict]:
        draft, state = LH9DialogueTests().fixture(**kwargs)
        return draft, self.convert(state)

    def test_lh10_observed_s0_n0_f0_three_distinct_expressions_deliver(self) -> None:
        draft, state = self.fixture()
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertTrue({"E_EVIDENCE_STOP_MISSING", "E_STRONG_SEED_GROUP_UNSET", "W_SEED_ZERO_PROXY"}.isdisjoint(self.codes(result)))
        self.assertEqual(result["diversity"]["records_passed"], 1)
        self.assertTrue(result["diversity"]["semantic_review_required"])
        self.assertEqual(self.allocation(state)["scenario_fit_cap"], "S0")
        self.assertEqual(self.allocation(state)["clip_causality_cap"], "S0")

    def test_lh10_mixed_personal_need_and_observed_modes_deliver(self) -> None:
        draft, state = self.fixture()
        group = self.allocation(state)["groups"][1]
        group.update(claim_mode="personal_need", target_s_level="S1", actual_s_level="S1", benefit_basis="workflow", need_connection="看到挪机器时杯子晃动，想到先清好自己的桌面", dominant_expression="想先清好自己的桌面再摆机器", product_connection="挪Pocket时杯子晃动的细节触发摆放前准备")
        draft = draft.replace("你给大疆Pocket腾位置时杯子晃那一下，看得我跟着屏住气", "杯子晃那一下提醒我了，想摆大疆Pocket得先给桌子腾块地方")
        self.assert_clean(self.run_draft(draft, state))
        group.pop("need_connection")
        self.assertIn("E_PERSONAL_NEED_CONNECTION_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh10_required_free_form_descriptions_are_not_enums(self) -> None:
        for field in ["dominant_expression", "product_connection"]:
            for value in [None, "", "  ", [], "？！"]:
                with self.subTest(field=field, value=value):
                    draft, state = self.fixture(count=1)
                    self.allocation(state)["groups"][0][field] = value
                    result = self.run_draft(draft, state)
                    self.assertIn("E_LH10_" + field.upper() + "_MISSING", self.codes(result))
                    self.assertIn("W_SEED_ZERO_PROXY", self.codes(result))

    def test_lh10_missing_revise_or_empty_review_blocks_delivery(self) -> None:
        for variant in ["missing", "empty", "revise", "unreviewed", "reason_missing"]:
            with self.subTest(variant=variant):
                draft, state = self.fixture(count=1)
                semantic = state["qa"]["semantic_review"]
                if variant == "missing": semantic.pop("diversity_review")
                elif variant == "empty": semantic["diversity_review"] = []
                elif variant == "revise": semantic["diversity_review"][0]["verdict"] = "revise"
                elif variant == "unreviewed": semantic["diversity_review"][0]["verdict"] = ""
                else: semantic["diversity_review"][0]["comparison_reason"] = ""
                result = self.run_draft(draft, state)
                self.assertGreater(result["summary"]["errors"], 0)
                self.assertIn("W_SEED_ZERO_PROXY", self.codes(result))

    def test_lh10_review_ids_cannot_be_wrong_duplicate_or_orphan(self) -> None:
        for variant in ["wrong", "duplicate", "orphan"]:
            with self.subTest(variant=variant):
                draft, state = self.fixture()
                reviews = state["qa"]["semantic_review"]["diversity_review"]
                if variant == "wrong": reviews[0]["id"] = "another-post"
                elif variant == "duplicate": reviews.append(dict(reviews[0]))
                else: reviews.append({**reviews[0], "id": "another-post"})
                self.assertGreater(self.run_draft(draft, state)["summary"]["errors"], 0)

    def test_lh10_identical_dominant_expression_fails_even_after_passed_review(self) -> None:
        draft, state = self.fixture()
        groups = self.allocation(state)["groups"]
        groups[1]["dominant_expression"] = "调侃猫把开箱镜头抢走！"
        result = self.run_draft(draft, state)
        self.assertIn("E_DOMINANT_EXPRESSION_DUPLICATE", self.codes(result))
        self.assertEqual(result["diversity"]["records_passed"], 0)

    def test_lh10_observed_main_and_replies_cannot_smuggle_hardware_claims(self) -> None:
        for mode in ["observed", "personal_need"]:
            for position in ["main", "reply1", "reply2"]:
                with self.subTest(mode=mode, position=position):
                    main = "Pocket这一下转场是怎么拍的？"
                    replies = ["纸箱里要不要先放点东西", "放两件衣服就行"]
                    assertion = "Pocket支持4K录制"
                    if position == "main": main = assertion
                    else: replies[int(position[-1]) - 1] = assertion
                    draft, state = self.dialogue_fixture(main=main, replies=replies)
                    self.allocation(state)["groups"][0].update(claim_mode=mode, target_s_level="S0" if mode == "observed" else "S1", actual_s_level="S0" if mode == "observed" else "S1")
                    result = self.run_draft(draft, state)
                    self.assertIn("E_" + mode.upper() + "_PRODUCT_ASSERTION", self.codes(result))

    def test_lh10_observed_pronoun_reply_cannot_borrow_question_to_hide_assertion(self) -> None:
        for reply in ["它支持4K录制", "支持4K录制"]:
            with self.subTest(reply=reply):
                draft, state = self.dialogue_fixture(main="Pocket这一下转场是怎么拍的？", replies=[reply, "这样解释不了转场怎么接上吧"])
                self.allocation(state)["groups"][0].update(claim_mode="observed", target_s_level="S0", actual_s_level="S0")
                self.assertIn("E_OBSERVED_PRODUCT_ASSERTION", self.codes(self.run_draft(draft, state)))

    def test_lh10_observed_current_result_causality_is_checked_each_turn(self) -> None:
        for position in ["main", "reply1", "reply2"]:
            with self.subTest(position=position):
                main = "Pocket这一下转场是怎么拍的？"
                replies = ["纸箱里要不要先放点东西", "放两件衣服就行"]
                assertion = "这段这么稳全靠Pocket的三轴云台"
                if position == "main": main = assertion
                else: replies[int(position[-1]) - 1] = assertion
                draft, state = self.dialogue_fixture(main=main, replies=replies)
                self.allocation(state)["groups"][0].update(claim_mode="observed", target_s_level="S0", actual_s_level="S0")
                self.assertIn("E_OBSERVED_CURRENT_CAUSALITY", self.codes(self.run_draft(draft, state)))

    def test_lh10_invalid_anchor_never_gets_observed_zero_proxy_exemption(self) -> None:
        draft, state = self.fixture(count=1)
        self.allocation(state)["groups"][0]["main_anchor_ids"] = ["", "second"]
        result = self.run_draft(draft, state)
        self.assertIn("E_LH6_GROUP_SCHEMA", self.codes(result))
        self.assertIn("W_SEED_ZERO_PROXY", self.codes(result))

    def test_lh10_lh9_a_can_return_and_c_cannot_borrow_a_source(self) -> None:
        source = LH9DialogueTests().source("A")
        for speaker in ["A", "C"]:
            with self.subTest(speaker=speaker):
                draft, state = self.dialogue_fixture(main="我刚入手了p3，周末想学你这个转场", replies=["纸箱里要不要先放点东西", "我的p3先不装箱了，试完这个再收"], speakers=["B", speaker], main_source=source)
                result = self.run_draft(draft, state)
                if speaker == "A": self.assert_clean(result)
                else: self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(result))
        self.allocation(state)["groups"][0]["reply_personal_contexts"] = {"2": source}
        self.assertIn("E_DIALOGUE_SOURCE_BORROWED", self.codes(self.run_draft(draft, state)))

    def test_lh10_main_naming_and_no_osmo_rules_still_apply(self) -> None:
        draft, state = self.fixture(count=1)
        self.assertIn("E_MAIN_PRODUCT_NAME_MISSING", self.codes(self.run_draft(draft.replace("Pocket", "相机"), state)))
        self.assertIn("E_COPY_OSMO_NAME", self.codes(self.run_draft(draft.replace("Pocket", "OsmoPocket"), state)))

    def test_lh10_review_gate_remains_active_with_seeding_off(self) -> None:
        draft, state = self.fixture()
        state["qa"]["semantic_review"]["diversity_review"][0]["verdict"] = "revise"
        self.assertIn("E_DIVERSITY_REVIEW_REVISE", self.codes(self.run_draft(draft, state, seeding_policy="off")))

    def test_lh10_template_has_unclassified_slots_and_pending_review(self) -> None:
        state = lh10_neutral_template_fixture()
        self.assertEqual(state["rule_version"], "2026-09-05-LH10")
        groups = self.allocation(state)["groups"]
        self.assertEqual(len(groups), 3)
        for group in groups:
            for field in ["claim_mode", "target_s_level", "actual_s_level", "dominant_expression", "product_connection"]:
                self.assertEqual(group[field], "", (group["group"], field))
        self.assertEqual(state["qa"]["semantic_review"]["diversity_review"][0]["verdict"], "")

    def test_lh10_low_s_claims_cannot_escape_by_changing_mode(self) -> None:
        for mode in ["attributed", "scenario_fit", "causal", "comparative"]:
            for claim_id, expected in [("", "E_SEED_CLAIM_MISSING"), ("invented_claim", "E_SEED_CLAIM_UNKNOWN")]:
                with self.subTest(mode=mode, claim_id=claim_id):
                    draft, state = self.fixture()
                    draft = draft.replace("Pocket这场开箱真正的主角是那只抢镜的猫", "Pocket支持4K录制")
                    self.allocation(state)["groups"][0].update(claim_mode=mode, claim_id=claim_id)
                    self.assertIn(expected, self.codes(self.run_draft(draft, state)))

    def low_fact_fixture(self, *, mode: str = "scenario_fit") -> tuple[str, dict]:
        group = group_context(1, mode=mode, claim_id="shared_3axis_gimbal", condition="要是出门拍走路段", s_level="S0")
        state = as_lh7(state_for(group, model_level="M0", confirmed_model="unknown", n_level="N1", scene_tags=["walking"], p_level="P1", verified_claims=["shared_3axis_gimbal"], strong_group=None), count=1, main_only=True)
        draft = draft_from_groups([("要是出门拍走路段，Pocket有三轴机械云台", [])])
        return draft, self.convert(state)

    def test_lh10_registered_low_s_fact_requires_p_source_and_matching_claim(self) -> None:
        for variant, expected in [("p0", "E_PRODUCT_FACT_UNVERIFIED"), ("not_verified", "E_PRODUCT_FACT_UNVERIFIED"), ("no_source", "E_PRODUCT_FACT_SOURCE_MISSING"), ("wrong_claim", "E_CLAIM_NOT_IN_COPY"), ("wrong_model", "E_MODEL_FEATURE_MISMATCH")]:
            with self.subTest(variant=variant):
                draft, state = self.low_fact_fixture()
                allocation = self.allocation(state)
                if variant == "p0": allocation["fact_status"]["level"] = "P0"
                elif variant == "not_verified": allocation["fact_status"]["verified_claim_ids"] = []
                elif variant == "no_source": allocation["fact_status"]["source_urls"] = []
                elif variant == "wrong_claim": allocation["groups"][0]["claim_id"] = "shared_intelligent_tracking"
                else: allocation["groups"][0]["target_model"] = "pocket_2"
                self.assertIn(expected, self.codes(self.run_draft(draft, state)))

    def test_lh10_verified_low_s_fact_keeps_s0_without_benefit_or_strong_quota(self) -> None:
        draft, state = self.low_fact_fixture()
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertEqual(self.allocation(state)["groups"][0]["actual_s_level"], "S0")
        self.assertEqual(self.allocation(state)["groups"][0]["user_benefit"], "")
        self.assertEqual(result["distributions"]["seeding"]["semantic"]["strong_seed_sections"], 0)

    def test_lh10_low_s_attribution_requires_author_evidence(self) -> None:
        draft, state = self.low_fact_fixture(mode="attributed")
        result = self.run_draft(draft, state)
        self.assertIn("E_PRODUCT_ATTRIBUTION_MISSING", self.codes(result))
        self.assertIn("E_PRODUCT_ATTRIBUTION_UNGROUNDED", self.codes(result))
        draft = draft.replace("要是出门拍走路段，Pocket", "博主说Pocket")
        self.allocation(state)["feature_use"].update(level="F1", claim_ids=["shared_3axis_gimbal"], evidence="作者明确说该设备有三轴机械云台")
        self.assert_clean(self.run_draft(draft, state))

    def test_lh10_low_s_current_cause_still_requires_f2_and_m2(self) -> None:
        draft, state = self.low_fact_fixture(mode="causal")
        draft = draft.replace("要是出门拍走路段，Pocket有三轴机械云台", "这段靠Pocket3的三轴机械云台才拍成这样")
        allocation = self.allocation(state)
        allocation["groups"][0].update(target_model="pocket_3", usage_condition="", evidence_sources=["operation:t00:visible-gimbal-operation", "result:t00:walking-frame-result"])
        result = self.run_draft(draft, state)
        self.assertIn("E_CAUSAL_CLAIM_BELOW_F2", self.codes(result))
        self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(result))
        allocation["model_status"].update(level="M2", confirmed_model="pocket_3", claimed_model="pocket_3", evidence_type="ui_confirmed")
        allocation["feature_use"].update(level="F2", claim_ids=["shared_3axis_gimbal"], evidence="同一锚点的云台操作和结果")
        self.assert_clean(self.run_draft(draft, state))
        allocation["groups"][0]["claim_mode"] = "scenario_fit"
        self.assertIn("E_PRODUCT_CAUSALITY_MODE_INVALID", self.codes(self.run_draft(draft, state)))

    def test_lh10_neutral_prefix_and_parent_device_pronoun_cannot_hide_facts(self) -> None:
        for mode, level in [("observed", "S0"), ("personal_need", "S1")]:
            for reply, suffix in [("确实，它支持4K录制", "PRODUCT_ASSERTION"), ("这段这么稳全靠它", "CURRENT_CAUSALITY"), ("确实，这段这么稳全靠它", "CURRENT_CAUSALITY")]:
                with self.subTest(mode=mode, reply=reply):
                    draft, state = self.dialogue_fixture(main="Pocket这一下转场是怎么拍的？", replies=[reply, "这样解释不了转场怎么接上吧"])
                    self.allocation(state)["groups"][0].update(claim_mode=mode, target_s_level=level, actual_s_level=level)
                    self.assertIn("E_" + mode.upper() + "_" + suffix, self.codes(self.run_draft(draft, state)))

    def test_lh10_real_questions_and_non_device_pronouns_remain_interaction(self) -> None:
        for mode, level in [("observed", "S0"), ("personal_need", "S1")]:
            for main, reply in [("Pocket这一下转场是怎么拍的？", "它支持4K录制吗？"), ("Pocket这一下转场是怎么拍的？", "确实，它支持4K录制？"), ("Pocket这一下转场是怎么拍的？", "这段这么稳全靠它吗？"), ("Pocket旁边那只猫坐得好端正", "这段这么稳全靠它"), ("Pocket旁边那只猫坐得好端正", "确实，它还盯着镜头呢")]:
                with self.subTest(mode=mode, main=main, reply=reply):
                    draft, state = self.dialogue_fixture(main=main, replies=[reply, "看着这个镜头再等一等"])
                    self.allocation(state)["groups"][0].update(claim_mode=mode, target_s_level=level, actual_s_level=level)
                    self.assert_clean(self.run_draft(draft, state))

    def test_lh10_filming_animal_or_child_does_not_erase_explicit_device_subject(self) -> None:
        for main in ["Pocket支持4K录制猫咪", "Pocket能拍4K视频给小孩留念"]:
            with self.subTest(main=main):
                draft, state = self.fixture(count=1)
                draft = draft.replace("Pocket这场开箱真正的主角是那只抢镜的猫", main)
                self.assertIn("E_OBSERVED_PRODUCT_ASSERTION", self.codes(self.run_draft(draft, state)))


class LH11OptionalNameTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft
    codes = staticmethod(LH7DeliveryTests.codes)
    allocation = staticmethod(LH7DeliveryTests.allocation)
    assert_clean = LH9DialogueTests.assert_clean

    def fixture(self, *, count: int = 3) -> tuple[str, dict]:
        draft, state = LH10ExpressionTests().fixture(count=count)
        state["rule_version"] = "2026-09-05-LH11"
        return draft, state

    def visual_dialogue(self, *, main: str = "白纱透过来的光好漂亮", replies: list[str] | None = None, speakers: list[str] | None = None, main_source: dict | None = None) -> tuple[str, dict]:
        draft, state = LH10ExpressionTests().dialogue_fixture(main=main, replies=replies if replies is not None else ["像隔着一层很轻的雾", "对，刚好没有把人完全遮住"], speakers=speakers, main_source=main_source)
        state["rule_version"] = "2026-09-05-LH11"
        group = self.allocation(state)["groups"][0]
        group.update(claim_mode="observed", target_s_level="S0", actual_s_level="S0", benefit_basis="visual", product_connection="", dominant_expression="喜欢白纱滤过来的光与遮住一半的人像")
        return draft, state

    def test_lh11_visual_main_can_occupy_each_position_without_product_connection(self) -> None:
        named = ["Pocket这场开箱真正的主角是那只抢镜的猫", "你给大疆Pocket腾位置时杯子晃那一下，看得我跟着屏住气", "DJIPocket放在垫布上那一格留久一点吧，喜欢这个构图"]
        visual = ["猫一直盯着拆盒子的手，比谁都着急", "杯子晃那一下，看得我跟着屏住气", "垫布上那一格留久一点吧，喜欢这个构图"]
        for position in range(3):
            with self.subTest(position=position + 1):
                draft, state = self.fixture()
                draft = draft.replace(named[position], visual[position])
                self.allocation(state)["groups"][position]["product_connection"] = ""
                result = self.run_draft(draft, state)
                self.assert_clean(result)
                self.assertTrue({"E_MAIN_PRODUCT_NAME_MISSING", "E_EVIDENCE_STOP_MISSING", "W_SEED_ZERO_PROXY"}.isdisjoint(self.codes(result)))

    def test_lh11_arrangement_is_not_a_hard_naming_ratio(self) -> None:
        for named in [True, False]:
            with self.subTest(named=named):
                draft, state = self.fixture()
                if not named:
                    draft = draft.replace("DJIPocket", "相机").replace("大疆Pocket", "相机").replace("Pocket", "相机")
                    for group in self.allocation(state)["groups"]:
                        group.pop("product_connection")
                self.assert_clean(self.run_draft(draft, state))

    def test_lh11_visual_thread_does_not_need_product_in_replies(self) -> None:
        draft, state = self.visual_dialogue()
        result = self.run_draft(draft, state)
        self.assert_clean(result)
        self.assertNotIn("W_SEED_ZERO_PROXY", self.codes(result))
        self.assertEqual(result["diversity"]["records_passed"], 1)

    def test_lh11_named_reply_requires_this_groups_product_connection(self) -> None:
        for position in [0, 1]:
            with self.subTest(position=position):
                replies = ["像隔着一层很轻的雾", "对，刚好没有把人完全遮住"]
                replies[position] = "Pocket这组里最喜欢这层白纱"
                draft, state = self.visual_dialogue(replies=replies)
                result = self.run_draft(draft, state)
                self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(result))
                self.assertIn("W_SEED_ZERO_PROXY", self.codes(result))
                self.allocation(state)["groups"][0]["product_connection"] = "回复讨论Pocket这组人像里的白纱与光线"
                self.assert_clean(self.run_draft(draft, state))

    def test_lh11_only_pure_observed_s0_group_can_leave_connection_empty(self) -> None:
        for variant in ["named_main", "personal_need", "s1", "workflow"]:
            with self.subTest(variant=variant):
                draft, state = self.visual_dialogue()
                group = self.allocation(state)["groups"][0]
                if variant == "named_main":
                    draft, state = self.visual_dialogue(main="Pocket这组白纱透过来的光好漂亮")
                elif variant == "personal_need":
                    group.update(claim_mode="personal_need", target_s_level="S1", actual_s_level="S1")
                elif variant == "workflow":
                    group["benefit_basis"] = "workflow"
                else:
                    group.update(target_s_level="S1", actual_s_level="S1")
                self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh11_visual_group_still_requires_real_anchor_and_dominant_expression(self) -> None:
        for field, value, expected in [("main_anchor_ids", [], "E_LH6_GROUP_SCHEMA"), ("dominant_expression", "", "E_LH10_DOMINANT_EXPRESSION_MISSING")]:
            with self.subTest(field=field):
                draft, state = self.visual_dialogue()
                self.allocation(state)["groups"][0][field] = value
                result = self.run_draft(draft, state)
                self.assertIn(expected, self.codes(result))
                self.assertIn("E_EVIDENCE_STOP_MISSING", self.codes(result))

    def test_lh11_generic_praise_rejected_by_semantic_review_cannot_claim_visual_exemption(self) -> None:
        draft, state = self.visual_dialogue(main="好美太好看了")
        review = state["qa"]["semantic_review"]["diversity_review"][0]
        review.update(verdict="revise", comparison_reason="主评未指出原帖细节，泛夸可直接移到其他帖子，需退回")
        result = self.run_draft(draft, state)
        self.assertIn("E_DIVERSITY_REVIEW_REVISE", self.codes(result))
        self.assertIn("E_EVIDENCE_STOP_MISSING", self.codes(result))
        self.assertIn("E_DIVERSITY_REVIEW_REVISE", self.codes(self.run_draft(draft, state, seeding_policy="off")))

    def test_lh11_named_label_variation_and_copy_format_still_apply(self) -> None:
        for main, expected in [("OsmoPocket这组白纱的光好看", "E_COPY_OSMO_NAME"), ("DJI Pocket这组白纱的光好看", "E_PRODUCT_INTERNAL_SPACE"), ("白纱这束光好漂亮。", "E_COPY_SENTENCE_PERIOD")]:
            with self.subTest(main=main):
                draft, state = self.visual_dialogue(main=main)
                self.assertIn(expected, self.codes(self.run_draft(draft, state)))
        draft, state = self.fixture()
        draft = draft.replace("你给大疆Pocket", "你给Pocket")
        self.assertIn("E_MAIN_PRODUCT_NAME_REPEAT", self.codes(self.run_draft(draft, state)))

    def test_lh11_nameless_main_cannot_hide_device_or_spec_capability_in_any_turn(self) -> None:
        for claim in ["这台支持4K录制", "确实，这台相机支持4K录制", "相机支持4K录制", "它支持4K录制", "支持4K录制", "这台能拍4K视频给小孩留念"]:
            for position in ["main", "reply1", "reply2"]:
                with self.subTest(claim=claim, position=position):
                    main = claim if position == "main" else "白纱透过来的光好漂亮"
                    replies = ["像隔着一层很轻的雾", "对，刚好没有把人完全遮住"]
                    if position != "main": replies[int(position[-1]) - 1] = claim
                    draft, state = self.visual_dialogue(main=main, replies=replies)
                    result = self.run_draft(draft, state)
                    self.assertIn("E_OBSERVED_PRODUCT_ASSERTION", self.codes(result))
                    self.assertIn("E_SEED_CLAIM_MISSING", self.codes(result))
                    self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(result))

    def test_lh11_nameless_main_cannot_hide_explicit_camera_causality(self) -> None:
        for claim in ["这段这么稳全靠这台相机", "确实，这段这么稳全靠这台相机", "这段这么清晰归功于那台摄像机"]:
            draft, state = self.visual_dialogue(replies=[claim, "还是想看一下现场是怎么拍的"])
            result = self.run_draft(draft, state)
            self.assertIn("E_OBSERVED_CURRENT_CAUSALITY", self.codes(result))
            self.assertIn("E_SEED_CLAIM_MISSING", self.codes(result))
            self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(result))

    def test_lh11_actual_facts_cannot_escape_by_changing_mode(self) -> None:
        for mode in ["observed", "personal_need", "attributed", "scenario_fit", "causal", "comparative"]:
            with self.subTest(mode=mode):
                draft, state = self.visual_dialogue(replies=["这台支持4K录制", "还想看现场怎么摆的位置"])
                self.allocation(state)["groups"][0]["claim_mode"] = mode
                self.assertIn("E_SEED_CLAIM_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh11_explicit_camera_claim_cannot_borrow_sibling_named_copy(self) -> None:
        draft, state = self.fixture()
        draft = draft.replace("Pocket这场开箱真正的主角是那只抢镜的猫", "这台有三轴机械云台")
        group = self.allocation(state)["groups"][0]
        group.update(claim_mode="attributed", claim_id="shared_3axis_gimbal", product_connection="断言该设备具备三轴机械云台")
        allocation = self.allocation(state)
        allocation["fact_status"].update(level="P1", verified_claim_ids=["shared_3axis_gimbal"], source_urls=REGISTRY["claims"]["shared_3axis_gimbal"]["official_sources"])
        result = self.run_draft(draft, state)
        self.assertIn("E_TARGET_PRODUCT_NOT_IN_COPY", self.codes(result))
        self.assertIn("E_PRODUCT_ATTRIBUTION_MISSING", self.codes(result))

    def test_lh11_true_questions_and_animal_or_person_referents_are_not_claims(self) -> None:
        cases = [
            ("白纱透过来的光好漂亮", "这台支持4K录制吗？"),
            ("白纱透过来的光好漂亮", "这段这么稳全靠这台相机吗？"),
            ("白纱透过来的光好漂亮", "它支持4K录制吗？"),
            ("白纱旁边那只猫坐得好端正", "确实，它还盯着镜头呢"),
            ("白纱旁边那只猫坐得好端正", "这段这么稳全靠它"),
            ("白纱后面的她都没怎么动", "她支持4K录制"),
            ("白纱旁边那只猫坐得好端正", "它支持4K录制"),
        ]
        for main, reply in cases:
            with self.subTest(main=main, reply=reply):
                draft, state = self.visual_dialogue(main=main, replies=[reply, "再看一遍这个镜头"])
                result = self.run_draft(draft, state)
                self.assert_clean(result)

    def test_lh11_explicit_device_reply_after_animal_still_requires_facts(self) -> None:
        draft, state = self.visual_dialogue(main="白纱旁边那只猫坐得好端正", replies=["这台相机支持4K录制猫咪", "还想看一下现场的摆放"])
        self.assertIn("E_OBSERVED_PRODUCT_ASSERTION", self.codes(self.run_draft(draft, state)))

    def test_lh11_reply_model_must_have_own_or_post_evidence(self) -> None:
        draft, state = self.visual_dialogue(replies=["p3这组白纱的感觉好喜欢", "我喜欢留了一半轮廓这点"])
        group = self.allocation(state)["groups"][0]
        group["product_connection"] = "回复在讨论p3这组作品的白纱画面"
        self.assertIn("E_REPLY_MODEL_UNGROUNDED", self.codes(self.run_draft(draft, state)))
        self.allocation(state)["model_status"].update(level="M1", claimed_model="pocket_3", evidence_type="author_claim")
        self.assert_clean(self.run_draft(draft, state))

    def test_lh11_reply_cannot_borrow_main_authors_or_sibling_groups_model_source(self) -> None:
        source = LH9DialogueTests().source("A")
        draft, state = self.visual_dialogue(replies=["p3这组白纱的感觉好喜欢", "我喜欢留了一半轮廓这点"], main_source=source)
        group = self.allocation(state)["groups"][0]
        group["product_connection"] = "回复在讨论p3这组作品的白纱画面"
        self.assertIn("E_REPLY_MODEL_UNGROUNDED", self.codes(self.run_draft(draft, state)))
        group["personal_context"] = None
        sibling_draft, sibling_state = self.visual_dialogue(main="我的p3也想留着这个白纱布景", main_source=source)
        sibling = self.allocation(sibling_state)["groups"][0]
        sibling.update(group=2, dominant_expression="希望给自己的机器留着白纱布景", product_connection="个人材料中的p3与白纱布景愿望有关")
        self.allocation(state)["groups"].append(sibling)
        draft += "\n" + sibling_draft.split("\n", 1)[1]
        result = self.run_draft(draft, state)
        self.assertIn("E_REPLY_MODEL_UNGROUNDED", self.codes(result))
        self.assertNotIn("E_MAIN_MODEL_UNGROUNDED", self.codes(result))

    def test_lh11_own_speaker_models_and_personal_source_continuity_remain_valid(self) -> None:
        draft, state = self.visual_dialogue(replies=["我的p3也想留着这个白纱布景", "试完先别收，留着再换个动作"], speakers=["B", "A"])
        group = self.allocation(state)["groups"][0]
        group["product_connection"] = "B提及个人p3与白纱布景尝试"
        self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(self.run_draft(draft, state)))
        group["reply_personal_contexts"] = {"1": LH9DialogueTests().source("B")}
        self.assert_clean(self.run_draft(draft, state))

    def test_lh11_no_name_does_not_loosen_legacy_lh10_naming(self) -> None:
        draft, state = self.visual_dialogue()
        state["rule_version"] = "2026-09-05-LH10"
        result = self.run_draft(draft, state)
        self.assertIn("E_MAIN_PRODUCT_NAME_MISSING", self.codes(result))
        self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(result))

    def test_lh11_template_keeps_neutral_slots_and_documents_optional_naming(self) -> None:
        state = lh11_neutral_template_fixture()
        self.assertEqual(state["rule_version"], "2026-09-05-LH11")
        policy = state["semantic_policy"]["lh11_optional_main_name"]
        self.assertIn("not_a_hard_ratio", policy["usual_arrangement"])
        self.assertEqual(policy["new_claim_modes"], [])
        self.assertEqual(policy["new_group_flags"], [])
        for group in self.allocation(state)["groups"]:
            for field in ["claim_mode", "target_s_level", "actual_s_level", "dominant_expression", "product_connection"]:
                self.assertEqual(group[field], "")
        self.assertEqual(state["qa"]["semantic_review"]["diversity_review"][0]["verdict"], "")

    def test_lh11_generic_device_aliases_require_fact_evidence(self) -> None:
        for claim, code in [("这个设备支持防抖", "E_OBSERVED_PRODUCT_ASSERTION"), ("该设备支持4K录制", "E_OBSERVED_PRODUCT_ASSERTION"), ("这个机器支持4K录制", "E_OBSERVED_PRODUCT_ASSERTION"), ("这段这么稳全靠这个设备", "E_OBSERVED_CURRENT_CAUSALITY")]:
            with self.subTest(claim=claim):
                draft, state = self.visual_dialogue(replies=[claim, "还想看看现场是怎么摆放的"])
                result = self.run_draft(draft, state)
                self.assertIn(code, self.codes(result))
                self.assertIn("E_SEED_CLAIM_MISSING", self.codes(result))
                self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", self.codes(result))
        draft, state = self.visual_dialogue(replies=["这个设备支持防抖吗？", "还想看看现场是怎么摆放的"])
        self.assert_clean(self.run_draft(draft, state))

    def test_lh11_device_owner_does_not_replace_device_subject(self) -> None:
        for claim in ["这台相机是她的，支持4K录制", "Pocket是博主用的，支持4K录制", "该设备属于她，确实，它支持4K录制"]:
            with self.subTest(claim=claim):
                draft, state = self.visual_dialogue(replies=[claim, "还想看看现场是怎么摆放的"])
                result = self.run_draft(draft, state)
                self.assertIn("E_OBSERVED_PRODUCT_ASSERTION", self.codes(result))
                self.assertIn("E_SEED_CLAIM_MISSING", self.codes(result))
        for main, reply in [("Pocket旁边的她都没怎么动", "她支持4K录制"), ("Pocket旁边那只猫坐得好端正", "它支持4K录制")]:
            with self.subTest(main=main):
                draft, state = self.visual_dialogue(main=main, replies=[reply, "还想看看现场是怎么摆放的"])
                self.allocation(state)["groups"][0]["product_connection"] = "回应Pocket旁边人物或猫咪的姿态"
                self.assert_clean(self.run_draft(draft, state))


class LH12FlexibleDeliveryTests(unittest.TestCase):
    run_draft = LH5SemanticTests.run_draft
    codes = staticmethod(LH7DeliveryTests.codes)
    allocation = staticmethod(LH7DeliveryTests.allocation)
    assert_clean = LH9DialogueTests.assert_clean

    def fixture(self, counts: tuple[int, ...] = (0, 1), *, legacy: bool = False, labels: bool = False) -> tuple[str, dict]:
        _, state = LH11OptionalNameTests().fixture()
        state.update(rule_version=CHECKER.LH12_RULE_VERSION, delivery_mode="with_replies")
        allocation = self.allocation(state)
        allocation["reduced_output_reason"] = ""
        sample = allocation["groups"][0]
        allocation["groups"] = []
        mains = ["白纱只遮一半脸那格最喜欢", "杯子晃那一下看得我屏住气", "猫盯着拆盒子的手比谁都着急", "门口那次回头留得恰好"]
        bodies = [
            ["这层光像隔了薄雾", "嗯，轮廓还留着", "侧脸没有被盖住", "眼睛刚好从边上露出来"],
            ["杯沿已经快挨着桌边了", "先挪一点位置会踏实些", "镜头切走才松口气", "还好没碰到旁边的花瓶"],
            ["耳朵都竖起来了", "它还往手边凑了一下", "盒子一响就抬头", "最后还在等下一层"],
            ["回头之后停住才有意思", "那半秒刚好够看清表情", "人走远了我还等着回头", "切在迈步前也挺有味道"],
        ]
        lines = ["## 小红书 1｜https://www.xiaohongshu.com/explore/test"]
        for index, count in enumerate(counts):
            main = mains[index % 4] + (str(index) if index >= 4 else "")
            group = json.loads(json.dumps(sample))
            group.update(group=index + 1, main_anchor_ids=[f"actual-{index + 1}"], dominant_expression=f"回应第{index + 1}组的具体画面", product_connection="", reply_personal_contexts={}, personal_context=None)
            group.pop("dialogue", None)
            lines.append(("主评论（A）：" if labels else "主评论：") + main if legacy else f"{index + 1}. {main}")
            turns = []
            for offset in range(count):
                number = offset + 1
                body = bodies[index % 4][offset % 4] + (str(offset) if offset >= 4 else "")
                parent = "main" if number == 1 else f"reply:{number - 1}"
                parent_body = main if number == 1 else bodies[index % 4][offset - 1]
                speaker = "B" if number % 2 else "A"
                recipient = "A" if number % 2 else "B"
                turns.append({"reply": number, "speaker": speaker, "reply_to": parent, "anchor_quote": parent_body[:6], "response_move": "回应父句提到的细节"})
                prefix = f"↳ 回复{number}（{speaker}→{recipient}）：" if labels else f"↳ 回复{number}："
                lines.append(prefix + body if legacy else "    - " + body)
            if count:
                group["dialogue"] = {"main_speaker": "A", "replies": turns}
            allocation["groups"].append(group)
        return "\n".join(lines), state

    def test_lh12_two_to_four_mains_and_mixed_reply_counts(self) -> None:
        for counts in [(0, 1), (0, 1, 3), (0, 1, 2, 4), (4, 0, 1, 3)]:
            with self.subTest(counts=counts):
                draft, state = self.fixture(counts)
                result = self.run_draft(draft, state)
                self.assert_clean(result)
                self.assertEqual(result["summary"]["mains"], len(counts))
                self.assertEqual(result["summary"]["replies"], sum(counts))
                self.assertNotIn("E_REDUCED_OUTPUT_REASON", self.codes(result))

    def test_lh12_rejects_one_five_mains_and_five_replies(self) -> None:
        for counts, code in [((0,), "E_GROUP_COUNT"), ((0, 0, 0, 0, 0), "E_GROUP_COUNT"), ((0, 5), "E_REPLY_COUNT")]:
            with self.subTest(counts=counts):
                draft, state = self.fixture(counts)
                self.assertIn(code, self.codes(self.run_draft(draft, state)))

    def test_lh12_main_only_still_forbids_replies(self) -> None:
        for counts, allowed in [((0, 0), True), ((0, 1), False)]:
            draft, state = self.fixture(counts)
            state["delivery_mode"] = "main_only"
            result = self.run_draft(draft, state)
            if allowed: self.assert_clean(result)
            else: self.assertIn("E_REPLY_COUNT", self.codes(result))

    def test_lh12_numbering_and_bullets_are_removed_from_bodies(self) -> None:
        draft, state = self.fixture((0, 1, 2, 4))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "final.md"
            path.write_text(draft, encoding="utf-8")
            sections, diagnostics = CHECKER.parse_file(path, lh12=True)
        self.assertEqual(diagnostics, [])
        self.assertEqual([g.main.group for g in sections[0].groups], [1, 2, 3, 4])
        self.assertEqual([r.reply_no for r in sections[0].groups[3].replies], [1, 2, 3, 4])
        self.assertEqual(sections[0].groups[0].main.text, "白纱只遮一半脸那格最喜欢")
        self.assertNotIn("E_COPY_SENTENCE_PERIOD", self.codes(self.run_draft(draft, state)))
        self.assertIn("E_COPY_SENTENCE_PERIOD", self.codes(self.run_draft(draft.replace("那格最喜欢", "那格最喜欢."), state)))

    def test_lh12_main_numbers_must_start_at_one_and_be_contiguous(self) -> None:
        draft, state = self.fixture()
        for before, after in [("1. ", "0. "), ("1. ", "2. "), ("2. ", "1. "), ("2. ", "3. ")]:
            with self.subTest(after=after):
                self.assertIn("E_MAIN_SEQUENCE", self.codes(self.run_draft(draft.replace(before, after, 1), state)))

    def test_lh12_numbering_restarts_per_section(self) -> None:
        draft, state = self.fixture((0, 0))
        second = json.loads(json.dumps(self.allocation(state)))
        second.update(id="other", section_number="2", canonical_url="https://www.xiaohongshu.com/explore/other")
        state["block_allocations"][0]["persuasion_allocations"].append(second)
        state["qa"]["semantic_review"]["diversity_review"].append({"id": "other", "verdict": "passed", "comparison_reason": "分别接住水边光线与脚步的细节"})
        other = "## 小红书 2｜https://www.xiaohongshu.com/explore/other\n1. 水面那点反光让我停了一下\n2. 踩到落叶时那半步像故意放慢了"
        self.assert_clean(self.run_draft(draft + "\n" + other, state))

    def test_lh12_malformed_or_nested_reply_lines_are_not_silently_dropped(self) -> None:
        draft, state = self.fixture((0, 2))
        for changed, code in [(draft.replace("    - 杯沿", "- 杯沿"), "E_DELIVERY_LINE_INVALID"), (draft.replace("    - 先挪", "        - 先挪"), "E_REPLY_INDENT"), (draft.replace("2. ", "2. ".replace(" ", "")), "E_DELIVERY_LINE_INVALID")]:
            self.assertIn(code, self.codes(self.run_draft(changed, state)))

    def test_lh12_visible_extra_copy_cannot_hide_in_a_fence_or_heading(self) -> None:
        draft, state = self.fixture((0, 0))
        for extra in ["\n```text\n这个设备支持防抖\n```", "\n# 这个设备支持防抖"]:
            self.assertIn("E_DELIVERY_LINE_INVALID", self.codes(self.run_draft(draft + extra, state)))

    def test_lh12_legacy_syntax_with_optional_labels_remains_readable(self) -> None:
        for labels in [False, True]:
            draft, state = self.fixture((0, 1, 3), legacy=True, labels=labels)
            self.assert_clean(self.run_draft(draft, state))
        draft, state = self.fixture((0, 1), legacy=True, labels=True)
        self.assertIn("E_DIALOGUE_LABEL_MISMATCH", self.codes(self.run_draft(draft.replace("回复1（B→A）", "回复1（C→A）"), state)))
        self.assertIn("E_DIALOGUE_LABEL_MISMATCH", self.codes(self.run_draft(draft.replace("主评论（A）", "主评论（B）", 1), state)))

    def test_lh12_one_reply_and_parallel_parents_need_no_forced_exchange(self) -> None:
        for count in [1, 2, 4]:
            draft, state = self.fixture((0, count))
            for index, turn in enumerate(self.allocation(state)["groups"][1]["dialogue"]["replies"]):
                turn.update(speaker="BCDE"[index], reply_to="main", anchor_quote="杯子晃那一下")
            result = self.run_draft(draft, state)
            self.assert_clean(result)
            self.assertTrue(result["dialogue"]["semantic_review_required"])

    def test_lh12_zero_reply_groups_accept_only_absent_or_empty_mapping(self) -> None:
        for variant in ["absent", "empty", "orphan_turn", "orphan_source", "invalid_sources", "invalid_dialogue"]:
            draft, state = self.fixture((0, 0))
            group = self.allocation(state)["groups"][0]
            if variant != "absent": group["dialogue"] = {"main_speaker": "A", "replies": []}
            if variant == "orphan_turn": group["dialogue"]["replies"] = [{"reply": 1, "speaker": "B", "reply_to": "main"}]
            if variant == "orphan_source": group["reply_personal_contexts"] = {"1": LH9DialogueTests().source("B")}
            if variant == "invalid_sources": group["reply_personal_contexts"] = []
            if variant == "invalid_dialogue": group["dialogue"] = []
            result = self.run_draft(draft, state)
            if variant in {"absent", "empty"}: self.assert_clean(result)
            else: self.assertGreater(result["summary"]["errors"], 0, variant)

    def test_lh12_unlabelled_replies_still_require_complete_internal_dialogue(self) -> None:
        for variant in ["missing", "empty", "duplicate", "reordered"]:
            draft, state = self.fixture((0, 2))
            group = self.allocation(state)["groups"][1]
            if variant == "missing": group.pop("dialogue")
            elif variant == "empty": group["dialogue"]["replies"] = []
            elif variant == "duplicate": group["dialogue"]["replies"].append(dict(group["dialogue"]["replies"][0]))
            else: group["dialogue"]["replies"].reverse()
            result = self.run_draft(draft, state)
            self.assertGreater(result["summary"]["errors"], 0, variant)

    def test_lh12_parent_self_speaker_and_anchor_gates_remain_active(self) -> None:
        variants = [("reply_to", "reply:2", "E_DIALOGUE_PARENT"), ("reply_to", "reply:99", "E_DIALOGUE_PARENT"), ("speaker", "A", "E_DIALOGUE_SELF_REPLY"), ("speaker", "F", "E_DIALOGUE_SPEAKER"), ("speaker", [], "E_DIALOGUE_SPEAKER"), ("anchor_quote", "不存在的原话", "E_DIALOGUE_ANCHOR_QUOTE")]
        for field, value, code in variants:
            draft, state = self.fixture((0, 2))
            self.allocation(state)["groups"][1]["dialogue"]["replies"][0][field] = value
            self.assertIn(code, self.codes(self.run_draft(draft, state)))

    def test_lh12_unlabelled_aba_retains_sources_and_c_cannot_borrow(self) -> None:
        draft, state = self.fixture((0, 2))
        group = self.allocation(state)["groups"][1]
        group.update(personal_context=LH9DialogueTests().source("A"), product_connection="A拿自己的p3参与布景讨论")
        draft = draft.replace("先挪一点位置会踏实些", "我的p3先不收起来了")
        self.assert_clean(self.run_draft(draft, state))
        group["dialogue"]["replies"][1]["speaker"] = "C"
        codes = self.codes(self.run_draft(draft, state))
        self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", codes)
        self.assertIn("E_REPLY_MODEL_UNGROUNDED", codes)

    def test_lh12_unlabelled_bcb_can_reuse_only_its_own_source(self) -> None:
        draft, state = self.fixture((0, 3))
        group = self.allocation(state)["groups"][1]
        group.update(product_connection="B继续讨论自己的p3与桌面布景", reply_personal_contexts={"1": LH9DialogueTests().source("B")})
        draft = draft.replace("杯沿已经快挨着桌边了", "我刚入手了p3，也想试试")
        draft = draft.replace("镜头切走才松口气", "我的p3先不收起来了")
        turns = group["dialogue"]["replies"]
        turns[1].update(speaker="C", anchor_quote="我刚入手了p3")
        self.assert_clean(self.run_draft(draft, state))
        group["reply_personal_contexts"] = {"3": LH9DialogueTests().source("B")}
        self.assertIn("E_REPLY_PERSONAL_CONTEXT_MISSING", self.codes(self.run_draft(draft, state)))

    def test_lh12_fourth_group_gets_anchor_mode_and_actual_mapping_gates(self) -> None:
        for field, value, code in [("main_anchor_ids", [], "E_LH6_GROUP_SCHEMA"), ("main_moves", [], "E_LH6_GROUP_SCHEMA"), ("actual_s_level", "", "E_ACTUAL_S_LEVEL_MISSING"), ("claim_mode", "invented", "E_SEED_GROUP_CONTEXT_INVALID")]:
            draft, state = self.fixture((0, 0, 0, 0))
            self.allocation(state)["groups"][3][field] = value
            self.assertIn(code, self.codes(self.run_draft(draft, state)))
        draft, state = self.fixture((0, 0, 0, 0))
        self.allocation(state)["groups"].pop()
        self.assertIn("E_LH7_GROUP_CONTEXT_COUNT", self.codes(self.run_draft(draft, state)))

    def test_lh12_fourth_group_main_and_single_reply_cannot_hide_device_facts(self) -> None:
        for original, assertion, code in [("门口那次回头留得恰好", "该设备支持4K录制", "E_OBSERVED_PRODUCT_ASSERTION"), ("回头之后停住才有意思", "这段这么稳全靠这个设备", "E_OBSERVED_CURRENT_CAUSALITY")]:
            draft, state = self.fixture((0, 0, 0, 1))
            draft = draft.replace(original, assertion)
            if original.startswith("门口"):
                self.allocation(state)["groups"][3]["dialogue"]["replies"][0]["anchor_quote"] = "该设备"
            codes = self.codes(self.run_draft(draft, state))
            self.assertIn(code, codes)
            self.assertIn("E_SEED_CLAIM_MISSING", codes)
            self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", codes)

    def test_lh12_verified_strong_group_can_be_fourth(self) -> None:
        draft, state = self.fixture((0, 0, 0, 1))
        allocation = self.allocation(state)
        strong = group_context(4, mode="scenario_fit", claim_id="4p_physical_60mm", target_model="pocket_4p", basis="product", benefit="不用为了表情往前挤", condition="经常拍舞台表情", s_level="S2")
        evidence = self.allocation(state_for(strong, scene_tags=["stage"], verified_claims=["4p_physical_60mm"]))
        for key in ["model_status", "scene_need", "feature_use", "fact_status", "clip_causality_cap", "scenario_fit_cap"]:
            allocation[key] = evidence[key]
        allocation["strong_seed_group"] = 4
        fourth = allocation["groups"][3]
        fourth.update(strong, product_connection="第四组讨论舞台表情的拍摄距离", seed_layers={"main": ["product"], "replies": ["need", "product", "benefit"]})
        draft = draft.replace("门口那次回头留得恰好", "看完这段有点好奇Pocket4P拍舞台会是什么样")
        draft = draft.replace("回头之后停住才有意思", "经常隔着人群拍舞台表情的话，我会先看4P的60mm实体中焦，不用为了表情往前挤")
        fourth["dialogue"]["replies"][0]["anchor_quote"] = "Pocket4P拍舞台"
        self.assert_clean(self.run_draft(draft, state))

    def test_lh12_off_policy_keeps_number_and_dialogue_structure_checks(self) -> None:
        draft, state = self.fixture((0, 1))
        self.allocation(state)["groups"][1].pop("dialogue")
        with tempfile.TemporaryDirectory() as tmp:
            path, state_path = Path(tmp) / "final.md", Path(tmp) / "state.json"
            path.write_text(draft.replace("2. ", "3. "), encoding="utf-8")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            codes = self.codes(CHECKER.audit([path], state_path=state_path, seeding_policy="off"))
        self.assertIn("E_MAIN_SEQUENCE", codes)
        self.assertIn("E_DIALOGUE_CONTEXT_MISSING", codes)

    def test_lh12_does_not_change_lh11_counts_labels_or_exchange(self) -> None:
        draft, state = self.fixture((0, 1), legacy=True)
        state["rule_version"] = CHECKER.LH11_RULE_VERSION
        codes = self.codes(self.run_draft(draft, state))
        self.assertTrue({"E_REPLY_COUNT", "E_REDUCED_OUTPUT_REASON", "E_DIALOGUE_LABEL_MISMATCH", "E_DIALOGUE_NO_EXCHANGE"}.issubset(codes))
        draft, state = self.fixture((0, 0, 0, 0), legacy=True)
        state.update(rule_version=CHECKER.LH11_RULE_VERSION, delivery_mode="main_only")
        self.assertIn("E_GROUP_COUNT", self.codes(self.run_draft(draft, state)))

    def test_lh12_template_is_one_reusable_group_with_no_reply_slots(self) -> None:
        state = json.loads((SKILL_ROOT / "assets" / "pocket_comment_state.template.json").read_text(encoding="utf-8"))
        self.assertEqual(state["rule_version"], CHECKER.LH12_RULE_VERSION)
        groups = self.allocation(state)["groups"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["dialogue"]["replies"], [])
        self.assertEqual(groups[0]["reply_personal_contexts"], {})
        for key in ["claim_mode", "actual_s_level", "dominant_expression", "product_connection"]:
            self.assertEqual(groups[0][key], "")

    def model_question_fixture(self, text: str, *, legacy: bool = False) -> tuple[str, dict]:
        draft, state = self.fixture((0, 0), legacy=legacy)
        allocation = self.allocation(state)
        allocation["model_status"].update(level="M1", evidence_type="author_claim", claimed_model="pocket_4p", confirmed_model="unknown", evidence="作者标题标注Pocket4P")
        allocation["groups"][0].update(target_model="pocket_4p", product_connection="沿用作者标签讨论这组人像的地点")
        return draft.replace("白纱只遮一半脸那格最喜欢", text), state

    def test_lh12_current_model_location_questions_do_not_claim_verified_camera(self) -> None:
        for text in ["最后那组Pocket4P人像是在店里拍的吗，桌边这一圈绿植好喜欢", "这段是Pocket4P拍的吗？"]:
            with self.subTest(text=text):
                draft, state = self.model_question_fixture(text)
                self.assert_clean(self.run_draft(draft, state))

    def test_lh12_current_model_assertion_survives_questions_in_other_clauses(self) -> None:
        for text in ["最后那组Pocket4P人像是在店里拍的，桌边这一圈绿植好喜欢", "这段是Pocket4P拍的吗？这段是Pocket4P拍的", "这段是Pocket4P拍的，店在哪里呀？", "这段不就是Pocket4P拍的吗？"]:
            with self.subTest(text=text):
                draft, state = self.model_question_fixture(text)
                self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(self.run_draft(draft, state)))

    def test_lh12_question_filter_does_not_change_old_version_assertions(self) -> None:
        text = "最后那组Pocket4P人像是在店里拍的吗，桌边这一圈绿植好喜欢"
        self.assertTrue(CHECKER.lh8_current_model_assertions(text))
        self.assertEqual(CHECKER.lh8_current_model_assertions(text, lh12=True), [])
        for version in [CHECKER.LH8_RULE_VERSION, CHECKER.LH9_RULE_VERSION, CHECKER.LH10_RULE_VERSION, CHECKER.LH11_RULE_VERSION]:
            with self.subTest(version=version):
                draft, state = self.model_question_fixture(text, legacy=True)
                state.update(rule_version=version, delivery_mode="main_only")
                self.assertIn("E_CURRENT_MODEL_BELOW_M2", self.codes(self.run_draft(draft, state)))

    def test_lh12_device_question_cannot_hide_following_performance_inference(self) -> None:
        for text, code in [("这台支持4K？那肯定很稳", "E_OBSERVED_PRODUCT_ASSERTION"), ("这台支持4K？那一定很稳", "E_OBSERVED_PRODUCT_ASSERTION"), ("这台支持4K？这段这么稳全靠这台", "E_OBSERVED_CURRENT_CAUSALITY")]:
            with self.subTest(text=text):
                draft, state = self.fixture((0, 0))
                draft = draft.replace("白纱只遮一半脸那格最喜欢", text)
                codes = self.codes(self.run_draft(draft, state))
                self.assertIn(code, codes)
                self.assertIn("E_SEED_CLAIM_MISSING", codes)
                self.assertIn("E_LH10_PRODUCT_CONNECTION_MISSING", codes)

    def test_lh12_implied_performance_needs_actual_device_antecedent(self) -> None:
        for text in ["这台支持4K吗？", "白纱旁边那只猫好淡定，那肯定很稳", "Pocket旁边那只猫好淡定，那肯定很稳", "这台支持4K？她肯定很稳"]:
            with self.subTest(text=text):
                draft, state = self.fixture((0, 0))
                draft = draft.replace("白纱只遮一半脸那格最喜欢", text)
                if "Pocket" in text:
                    self.allocation(state)["groups"][0]["product_connection"] = "相机旁的猫是讨论主体"
                self.assert_clean(self.run_draft(draft, state))


if __name__ == "__main__":
    unittest.main()
