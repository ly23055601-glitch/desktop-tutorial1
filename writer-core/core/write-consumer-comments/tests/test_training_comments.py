"""Boundary tests for the lightweight training-fiction protocol (stdlib only)."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_training_comments.py"
SPEC = importlib.util.spec_from_file_location("check_training_comments", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class TrainingChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state_path = self.root / "state.json"
        (self.root / "post.md").write_text("合成测试材料：画面是一只猫趴在窗边\n仅有画面，没有音轨\n", encoding="utf-8")
        (self.root / "product.md").write_text("单元测试资料，不代表任何现实型号参数：测试参数为2\n", encoding="utf-8")
        self.state = {"content_mode": "training_fiction", "draft": "draft.md", "draft_sha256": "", "posts": []}
        self.sections = []
        self.add_post([0, 1])

    def add_post(self, reply_counts, product_line="pocket"):
        number = len(self.sections) + 1
        title = f"合成材料case-{number}"
        comments, reply_context = {}, {}
        personas = {"A": "假想消费者，喜欢拍家里的日常"}
        for m, reply_count in enumerate(reply_counts, 1):
            cid = str(m)
            comments[cid] = f"第{m}条这个角度看着还挺舒服"
            for r in range(1, reply_count + 1):
                rid = f"{m}.{r}"
                comments[rid] = f"第{r}条我也注意到这个了"
                speaker = f"person-{m}-{r}"
                personas[speaker] = "假想消费者，有自己闲聊的兴趣点"
                parent = cid if r == 1 else f"{m}.{r - 1}"
                reply_context[rid] = {"speaker": speaker, "parent_id": parent, "parent_speaker": "A" if r == 1 else f"person-{m}-{r - 1}", "parent_text": comments[parent]}
        self.sections.append({"number": number, "title": title, "comments": comments})
        self.state["posts"].append({
            "section": number, "id": f"test-material-{number}", "title": title, "product_line": product_line,
            "sources": {
                "original": {"kind": "synthetic_post", "path": "post.md", "description": "合成测试夹具，不是现实平台证据"},
                "spec": {"kind": "product", "path": "product.md", "description": "仅用于检查引用机制的测试资料"}
            },
            "english_aliases": [], "personas": personas, "reply_context": reply_context, "assertions": []
        })

    def save(self, mutate_md=None, bind=True, profile="legacy"):
        lines = [f"# {CHECKER.LABEL}", ""]
        for section in self.sections:
            lines.append(f"## {section['number']}｜{section['title']}")
            for cid, body in section["comments"].items():
                lines.append(f"    - {body}" if "." in cid else f"{cid}. {body}")
            lines.append("")
        text = "\n".join(lines)
        if mutate_md:
            text = mutate_md(text)
        (self.root / "draft.md").write_text(text, encoding="utf-8")
        if bind:
            self.state["draft_sha256"] = hashlib.sha256((self.root / "draft.md").read_bytes()).hexdigest()
        self.state_path.write_text(json.dumps(self.state, ensure_ascii=False), encoding="utf-8")
        return CHECKER.check_state(self.state_path, profile=profile)

    def assert_issue(self, fragment, **save_args):
        errors = self.save(**save_args)
        self.assertTrue(any(fragment in e for e in errors), errors)

    def assertion(self, kind="post_fact", source="original", text="猫趴在窗边", quote="画面是一只猫趴在窗边"):
        self.sections[0]["comments"]["1"] = text
        self.state["posts"][0]["assertions"] = [{"comment_id": "1", "text": text, "kind": kind, "evidence": [{"source": source, "quote": quote}]}]

    def test_mixed_two_three_four_mains_and_zero_to_four_replies(self):
        self.add_post([2, 3, 4], "mic")
        self.add_post([0, 4, 1, 2], "osmo360")
        self.assertEqual([], self.save())

    def test_fictional_purchase_relationship_and_use_need_no_real_user_source(self):
        self.sections[0]["comments"]["1"] = "我去年就买了，平时和我妈出门会轮着拿，握着挺顺手"
        self.state["posts"][0]["assertions"] = [{"comment_id": "1", "text": "我去年就买了", "kind": "fictional_experience", "evidence": []}]
        self.assertEqual([], self.save())

    def test_fictional_experience_cannot_claim_real_evidence(self):
        self.assertion(kind="fictional_experience")
        self.assert_issue("假想经历evidence须为空")

    def test_fact_quotes_bind_to_body_and_same_post_file(self):
        self.assertion()
        self.assertEqual([], self.save())
        self.state["posts"][0]["assertions"][0]["text"] = "另一条不存在的正文"
        self.assert_issue("绑定最终正文")

    def test_product_fact_requires_product_source(self):
        self.assertion(kind="product_fact", source="spec", text="测试参数为2", quote="测试参数为2")
        self.assertEqual([], self.save())
        self.state["posts"][0]["assertions"][0]["evidence"][0]["source"] = "original"
        self.assert_issue("来源类型混用")

    def test_post_fact_cannot_use_product_source(self):
        self.assertion(source="spec", quote="测试参数为2")
        self.assert_issue("来源类型混用")

    def test_persona_cannot_be_registered_as_original_source(self):
        self.state["posts"][0]["sources"]["original"]["kind"] = "persona"
        self.assert_issue("人物设定不能作为来源")

    def test_product_source_cannot_point_to_training_state(self):
        self.assertion(kind="product_fact", source="spec", text="测试参数为2", quote="测试参数为2")
        self.state["posts"][0]["personas"]["A"] = "假想人物相信测试参数为2"
        self.state["posts"][0]["sources"]["spec"]["path"] = "state.json"
        self.assert_issue("训练state或最终draft不能作为事实来源自证")

    def test_product_source_cannot_point_to_final_draft(self):
        self.assertion(kind="product_fact", source="spec", text="测试参数为2", quote="测试参数为2")
        self.state["posts"][0]["sources"]["spec"]["path"] = "draft.md"
        self.assert_issue("训练state或最终draft不能作为事实来源自证")

    def test_other_post_source_is_not_in_scope(self):
        self.add_post([0, 0])
        self.state["posts"][1]["sources"]["other_post"] = self.state["posts"][1]["sources"].pop("original")
        self.assertion(source="other_post")
        self.assert_issue("未在本帖登记")

    def test_quote_must_exist_in_actual_file(self):
        self.assertion(quote="这个片段从未出现在文件里")
        self.assert_issue("quote不在本帖来源")

    def test_visual_post_evidence_is_accepted_but_not_product_proof(self):
        source = self.state["posts"][0]["sources"]["original"]
        source.update(kind="post", description="用户提供截图画面描述，无音轨，不推测参数")
        self.assertion()
        self.assertEqual([], self.save())
        self.state["posts"][0]["assertions"][0]["kind"] = "product_fact"
        self.assert_issue("来源类型混用")

    def test_synthetic_original_must_be_explicit(self):
        self.state["posts"][0]["sources"]["original"]["description"] = "来自现实平台"
        self.assert_issue("明示合成")

    def test_marker_missing_and_duplicate_fail(self):
        self.assert_issue("恰好出现一次", mutate_md=lambda text: text.replace(CHECKER.LABEL, "草稿"))
        self.assert_issue("恰好出现一次", mutate_md=lambda text: CHECKER.LABEL + "\n" + text)

    def test_missing_and_stale_hash_fail(self):
        self.state.pop("draft_sha256")
        self.assert_issue("draft_sha256", bind=False)
        self.assertEqual([], self.save())
        self.sections[0]["comments"]["1"] += "啊"
        self.assert_issue("draft_sha256", bind=False)

    def test_periods_are_rejected_but_numbering_decimals_urls_are_allowed(self):
        self.sections[0]["comments"]["1"] = "2.5这个数写在https://example.com/post/1.2里"
        self.assertEqual([], self.save())
        self.sections[0]["comments"]["1"] += "。"
        self.assert_issue("正文含句号")
        self.sections[0]["comments"]["1"] = "我去看了https://example.com."
        self.assert_issue("正文含句号")

    def test_english_aliases_reject_internal_spaces(self):
        self.state["posts"][0]["english_aliases"] = ["DJIPocket3"]
        self.sections[0]["comments"]["1"] = "DJIPocket3这大小看着还挺舒服"
        self.assertEqual([], self.save())
        self.sections[0]["comments"]["1"] = "DJI Pocket 3这大小看着还挺舒服"
        self.assert_issue("无空格别名")

    def test_pocket_osmo_rule_does_not_spread_to_om_or_360(self):
        self.add_post([0, 0], "osmo_mobile")
        self.add_post([0, 0], "osmo360")
        self.sections[1]["comments"]["1"] = "OsmoMobile7看着还挺舒服"
        self.sections[2]["comments"]["1"] = "Osmo360看着还挺舒服"
        self.state["posts"][1]["english_aliases"] = ["OsmoMobile7"]
        self.state["posts"][2]["english_aliases"] = ["Osmo360"]
        self.assertEqual([], self.save())
        self.sections[0]["comments"]["1"] = "OsmoPocket3看着还挺舒服"
        self.assert_issue("Pocket正文禁用Osmo")

    def test_real_mode_never_passes_training_checker(self):
        self.state["content_mode"] = "real_consumer"
        self.assert_issue("真实消费者模式不能通过")

    def test_reply_must_preserve_actual_parent_and_speaker(self):
        context = self.state["posts"][0]["reply_context"]["2.1"]
        context["parent_text"] = "旧稿的父句"
        self.assert_issue("逐字保留直接父句")
        context["parent_text"] = self.sections[0]["comments"]["2"]
        context["speaker"] = "未定义人物"
        self.assert_issue("须对应personas")

    def test_reply_cannot_point_to_another_main(self):
        context = self.state["posts"][0]["reply_context"]["2.1"]
        context.update(parent_id="1", parent_text=self.sections[0]["comments"]["1"])
        self.assert_issue("同楼较早评论")

    def test_reply_context_cannot_be_omitted(self):
        self.state["posts"][0]["reply_context"] = {}
        self.assert_issue("完整且仅映射实际回复")

    def test_heading_and_state_must_correspond(self):
        self.state["posts"][0]["title"] = "其他材料"
        self.assert_issue("title必须精确对应")
        self.state["posts"][0]["section"] = 2
        self.assert_issue("一一对应")

    def test_too_few_mains_and_too_many_replies_fail(self):
        self.sections = []
        self.state["posts"] = []
        self.add_post([5])
        errors = self.save()
        self.assertTrue(any("2–4条主评" in e for e in errors), errors)
        self.assertTrue(any("0–4条" in e for e in errors), errors)

    def test_bad_numbering_and_unparsed_body_fail(self):
        self.assert_issue("连续编号", mutate_md=lambda text: text.replace("2. 第2条", "3. 第2条"))
        self.assert_issue("四空格缩进", mutate_md=lambda text: text + "\n这行无编号正文不能被跳过")

    def test_paths_are_relative_to_state_not_cwd(self):
        self.assertEqual([], self.save())
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.state_path), "--json"], cwd=SCRIPT.parent, capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["structure_ok"])
        self.assertTrue(report["semantic_review_required"])
        self.assertEqual("training_fiction_structure_only", report["scope"])

    def test_template_is_one_unfinished_structure_example(self):
        template = json.loads((SCRIPT.parents[1] / "assets/training-state.template.json").read_text())
        self.assertEqual(1, len(template["posts"]))
        self.assertNotIn("passed", json.dumps(template))
        self.assertNotRegex(template["draft_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual({}, template["posts"][0]["personas"])
        self.assertEqual({}, template["posts"][0]["reply_context"])
        self.assertEqual([], template["posts"][0]["assertions"])

    def test_numeric_id_reports_error_without_crashing(self):
        self.state["posts"][0]["id"] = 123
        self.assert_issue("id必须是原帖ID或明确的用户材料ID")

    def test_invalid_json_reports_error_without_crashing(self):
        self.state_path.write_text('{"bad":', encoding="utf-8")
        errors = CHECKER.check_state(self.state_path)
        self.assertTrue(any("无法读取state" in e for e in errors), errors)

    def test_malformed_kind_reports_error_without_crashing(self):
        self.state["posts"][0]["sources"]["original"]["kind"] = []
        self.assert_issue("kind只允许")
        self.assertion(kind=[])
        self.assert_issue("无效kind")

    def set_reply_counts(self, counts):
        self.sections = []
        self.state["posts"] = []
        self.add_post(counts)

    def test_cw5_accepts_five_and_eight_replies_with_two_to_four_mains(self):
        for counts in ([5, 0], [0, 8, 4], [5, 0, 8, 1]):
            with self.subTest(counts=counts):
                self.set_reply_counts(counts)
                self.assertEqual([], self.save(profile="cw5"))

    def test_cw5_does_not_impose_two_long_group_maximum(self):
        self.set_reply_counts([5, 6, 8])
        self.assertEqual([], self.save(profile="cw5"))

    def test_cw5_rejects_nine_replies(self):
        self.set_reply_counts([9, 0, 1])
        self.assert_issue("回复须为0–8条", profile="cw5")

    def test_cw5_requires_a_long_group_in_every_post(self):
        self.set_reply_counts([5, 0])
        self.add_post([4, 3, 0])
        errors = self.save(profile="cw5")
        self.assertEqual(["第2帖：CW5至少一组主评须有5–8条回复"], errors)

    def test_cw5_preserves_two_to_four_main_limits(self):
        for counts in ([5], [5, 0, 0, 0, 0]):
            with self.subTest(counts=counts):
                self.set_reply_counts(counts)
                self.assert_issue("2–4条主评", profile="cw5")

    def test_legacy_and_default_reject_five_replies(self):
        self.set_reply_counts([5, 0])
        self.assert_issue("回复须为0–4条")
        self.assertEqual(self.save(profile="legacy"), CHECKER.check_state(self.state_path))
        self.assertEqual([], self.save(profile="cw5"))

    def test_cw5_accepts_branches_repeat_speakers_and_nonadjacent_parents(self):
        self.set_reply_counts([8, 0, 1])
        post = self.state["posts"][0]
        comments = self.sections[0]["comments"]
        post["personas"].update(B="假想消费者，关心自己的拍摄用途", C="假想消费者，分享自己的操作习惯")
        # B/C independently reply to the main; A/B return to earlier branches.
        turns = [("B", "1", "A"), ("C", "1", "A"), ("A", "1.1", "B"),
                 ("B", "1.3", "A"), ("A", "1.2", "C"), ("C", "1.5", "A"),
                 ("B", "1", "A"), ("C", "1.4", "B")]
        for r, (speaker, parent, parent_speaker) in enumerate(turns, 1):
            post["reply_context"][f"1.{r}"] = {
                "speaker": speaker, "parent_id": parent,
                "parent_speaker": parent_speaker, "parent_text": comments[parent]
            }
        self.assertEqual([], self.save(profile="cw5"))

    def test_cw5_late_reply_facts_keep_source_type_quote_and_body_checks(self):
        for r in range(5, 9):
            with self.subTest(reply=r):
                self.set_reply_counts([8, 0])
                post = self.state["posts"][0]
                comments = self.sections[0]["comments"]
                cid = f"1.{r}"
                comments[cid] = "测试参数为2"
                if r < 8:
                    post["reply_context"][f"1.{r + 1}"]["parent_text"] = comments[cid]
                assertion = {"comment_id": cid, "text": "测试参数为2", "kind": "product_fact",
                             "evidence": [{"source": "spec", "quote": "测试参数为2"}]}
                post["assertions"] = [assertion]
                self.assertEqual([], self.save(profile="cw5"))
                assertion["evidence"][0]["source"] = "original"
                self.assert_issue("来源类型混用", profile="cw5")
                assertion["evidence"][0]["source"] = "spec"
                assertion["evidence"][0]["quote"] = "不存在的产品资料原句"
                self.assert_issue("quote不在本帖来源", profile="cw5")
                assertion["evidence"][0]["quote"] = "测试参数为2"
                assertion["text"] = "未出现在回复里的断言"
                self.assert_issue("绑定最终正文", profile="cw5")
                assertion["text"] = "测试参数为2"
                assertion["evidence"] = []
                self.assert_issue("事实断言缺少证据", profile="cw5")

    def test_cw5_late_reply_source_must_exist_in_this_post(self):
        self.set_reply_counts([8, 0])
        self.add_post([5, 0])
        self.state["posts"][1]["sources"]["other_post"] = self.state["posts"][1]["sources"].pop("original")
        post = self.state["posts"][0]
        post["assertions"] = [{"comment_id": "1.8", "text": self.sections[0]["comments"]["1.8"],
                               "kind": "post_fact", "evidence": [{"source": "other_post", "quote": "画面是一只猫趴在窗边"}]}]
        self.assert_issue("未在本帖登记", profile="cw5")
        post["assertions"][0]["evidence"][0]["source"] = "original"
        post["sources"]["original"]["path"] = "missing.md"
        self.assert_issue("文件不存在", profile="cw5")

    def test_cw5_late_reply_context_and_people_are_checked(self):
        for r in range(5, 9):
            with self.subTest(reply=r):
                self.set_reply_counts([8, 0])
                context = self.state["posts"][0]["reply_context"]
                cid = f"1.{r}"
                info = context[cid]
                original = dict(info)
                info["speaker"] = "未定义人物"
                self.assert_issue("须对应personas", profile="cw5")
                info.update(original)
                info["parent_speaker"] = "A"
                self.assert_issue("说话者映射冲突", profile="cw5")
                info.update(original)
                info["parent_text"] = "旧稿父句"
                self.assert_issue("逐字保留直接父句", profile="cw5")
                info.update(original)
                info.update(parent_id="2", parent_text=self.sections[0]["comments"]["2"])
                self.assert_issue("同楼较早评论", profile="cw5")
                info.update(original)
                info.update(parent_id=cid, parent_text=self.sections[0]["comments"][cid])
                self.assert_issue("同楼较早评论", profile="cw5")
                info.update(original)
                if r < 8:
                    info.update(parent_id=f"1.{r + 1}", parent_text=self.sections[0]["comments"][f"1.{r + 1}"])
                    self.assert_issue("同楼较早评论", profile="cw5")
                    info.update(original)
                del context[cid]
                self.assert_issue("完整且仅映射实际回复", profile="cw5")

    def test_cw5_late_reply_does_not_skip_text_or_hash_checks(self):
        self.set_reply_counts([8, 0])
        self.assertEqual([], self.save(profile="cw5"))
        self.sections[0]["comments"]["1.8"] += "。"
        self.assert_issue("正文含句号", profile="cw5")
        self.sections[0]["comments"]["1.8"] = "改后的末条回复"
        self.assert_issue("draft_sha256", bind=False, profile="cw5")

    def test_cw5_still_rejects_real_consumer_mode(self):
        self.set_reply_counts([5, 0])
        self.state["content_mode"] = "real_consumer"
        self.assert_issue("真实消费者模式不能通过", profile="cw5")

    def test_cli_reports_selected_profile_and_keeps_legacy_default(self):
        self.set_reply_counts([5, 0])
        self.assertEqual([], self.save(profile="cw5"))
        for args, expected_profile, expected_code in (([], "legacy", 1), (["--profile", "legacy"], "legacy", 1), (["--profile", "cw5"], "cw5", 0)):
            with self.subTest(profile=expected_profile, args=args):
                result = subprocess.run([sys.executable, str(SCRIPT), str(self.state_path), "--json", *args], capture_output=True, text=True, check=False)
                self.assertEqual(expected_code, result.returncode, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(expected_profile, report["profile"])
                self.assertEqual(expected_code == 0, report["structure_ok"])
                self.assertTrue(report["semantic_review_required"])
                self.assertEqual("training_fiction_structure_only", report["scope"])

    def test_unknown_profile_fails_in_api_and_cli(self):
        self.assertEqual([], self.save())
        self.assertTrue(any("不支持的检查profile" in e for e in CHECKER.check_state(self.state_path, profile="future")))
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.state_path), "--profile", "future"], capture_output=True, text=True, check=False)
        self.assertEqual(2, result.returncode)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
