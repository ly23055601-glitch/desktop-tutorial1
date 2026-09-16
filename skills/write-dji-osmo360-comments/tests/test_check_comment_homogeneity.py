#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_comment_homogeneity.py"


def valid_draft(heading: str = "## 1｜https://example.com/post") -> str:
    return "\n".join(
        [
            heading,
            "1.清晨在校园操场慢跑时，Osmo360能把人物和周围环境一起留下，后期再切前后视角就从容多了，看得有点想入",
            "↳跑起来最怕只剩一张正脸",
            "↳还能看看身后的同学有没有跟上",
            "2.傍晚在校园天台合影时，这台全景机能从高处收进更完整的环境，这种用法确实心动",
            "↳人多的时候普通镜头很容易顾此失彼",
            "↳这个角度把晚霞也留下了",
            "3.夜里跑道灯刚亮的那一刻太有青春片的感觉了",
            "↳放学后的校园真的自带氛围",
            "↳最后那个回头很自然",
            "",
        ]
    )


class CheckerTests(unittest.TestCase):
    def run_checker(
        self,
        draft: str,
        baseline: str | None = None,
        extra_args: list[str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            draft_path = root / "draft.md"
            draft_path.write_text(draft, encoding="utf-8")
            command = [
                sys.executable,
                str(SCRIPT),
                str(draft_path),
                "--product-policy",
                "strict",
                "--format",
                "json",
            ]
            if baseline is not None:
                baseline_path = root / "baseline.md"
                baseline_path.write_text(baseline, encoding="utf-8")
                command.extend(["--baseline", str(baseline_path)])
            command.extend(extra_args or [])
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            return result, json.loads(result.stdout)

    def test_compact_numbered_and_reply_lines_parse(self) -> None:
        result, report = self.run_checker(valid_draft())

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["metrics"]["links"], 1)
        self.assertEqual(report["metrics"]["main_comments"], 3)
        self.assertEqual(report["metrics"]["replies"], 6)
        self.assertEqual(report["metrics"]["product_slot_patterns"], {"PPC": 1})
        self.assertNotIn("E_BODY_SPACE", {item["code"] for item in report["diagnostics"]})

    def test_legacy_spaced_markers_still_parse(self) -> None:
        draft = valid_draft().replace("1.清晨", "1. 清晨").replace("↳跑起来", "↳ 跑起来")
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["metrics"]["main_comments"], 3)
        self.assertEqual(report["metrics"]["replies"], 6)

    def test_ascii_and_fullwidth_spaces_in_bodies_are_errors(self) -> None:
        draft = valid_draft().replace("清晨在校园", "清晨 在校园").replace("跑起来最怕", "跑起来　最怕")
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 1)
        issues = [item for item in report["diagnostics"] if item["code"] == "E_BODY_SPACE"]
        self.assertEqual(len(issues), 2)
        self.assertEqual(
            {(item["half_width_spaces"], item["full_width_spaces"]) for item in issues},
            {(1, 0), (0, 1)},
        )

    def test_ascii_and_fullwidth_trailing_spaces_are_errors(self) -> None:
        draft = valid_draft().replace("有点想入\n", "有点想入 \n").replace(
            "跑起来最怕只剩一张正脸\n",
            "跑起来最怕只剩一张正脸　\n",
        )
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 1)
        issues = [item for item in report["diagnostics"] if item["code"] == "E_BODY_SPACE"]
        self.assertEqual(len(issues), 2)
        self.assertEqual(
            {(item["half_width_spaces"], item["full_width_spaces"]) for item in issues},
            {(1, 0), (0, 1)},
        )

    def test_heading_spaces_are_exempt(self) -> None:
        _result, report = self.run_checker(valid_draft("##　1　｜　https://example.com/post"))

        self.assertNotIn("E_BODY_SPACE", {item["code"] for item in report["diagnostics"]})
        self.assertEqual(report["metrics"]["links"], 1)

    def test_old_baseline_is_not_space_audited(self) -> None:
        baseline = "\n".join(
            [
                "## 9｜https://example.com/old",
                "1.旧稿 可以保留原有空格",
                "↳旧 回复不按新规则追溯",
                "↳这是另一条旧回复",
                "2.完全不同的历史句子",
                "↳历史回复甲",
                "↳历史回复乙",
                "3.历史内容互动句子",
                "↳内容回复甲",
                "↳内容回复乙",
                "",
            ]
        )
        result, report = self.run_checker(valid_draft(), baseline)

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("E_BODY_SPACE", {item["code"] for item in report["diagnostics"]})

    def test_product_slots_are_fixed_to_ppc(self) -> None:
        draft = valid_draft().replace(
            "1.清晨在校园操场慢跑时，Osmo360能把人物和周围环境一起留下，后期再切前后视角就从容多了，看得有点想入",
            "1.清晨校园操场上的脚步声一出来就很有代入感",
        ).replace(
            "3.夜里跑道灯刚亮的那一刻太有青春片的感觉了",
            "3.夜里在校园跑道冲刺时，大疆360能把人物和环境一起留住，看完真的被种草了",
        )
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 1)
        self.assertIn("E_PRODUCT_SLOT_ORDER", {item["code"] for item in report["diagnostics"]})

    def test_product_main_count_is_exactly_two(self) -> None:
        draft = valid_draft().replace(
            "1.清晨在校园操场慢跑时，Osmo360能把人物和周围环境一起留下，后期再切前后视角就从容多了，看得有点想入",
            "1.清晨校园操场上的脚步声一出来就很有代入感",
        )
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 1)
        self.assertIn("E_PRODUCT_MAIN_COUNT", {item["code"] for item in report["diagnostics"]})

    def test_two_product_mains_need_different_names(self) -> None:
        result, report = self.run_checker(valid_draft().replace("这台全景机", "Osmo360"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("E_PRODUCT_TERM_REPEAT", {item["code"] for item in report["diagnostics"]})

    def test_generic_feature_word_is_not_a_second_product_name(self) -> None:
        draft = valid_draft().replace(
            "后期再切前后视角就从容多了",
            "回去再从全景素材里切前后视角就从容多了",
        )
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("E_PRODUCT_STACK", {item["code"] for item in report["diagnostics"]})

    def test_unique_second_generation_id_allows_normalized_name(self) -> None:
        draft = valid_draft().replace("Osmo360能", "Osmo360II能")
        result, report = self.run_checker(draft, extra_args=["--allow-second-gen-id", "1"])

        self.assertEqual(result.returncode, 0, result.stdout)
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertNotIn("E_SECOND_GEN_EVIDENCE", codes)
        self.assertNotIn("E_SECOND_GEN_NAME_FORMAT", codes)

    def test_nonstandard_second_generation_name_is_rejected(self) -> None:
        for name in ("第二代", "2代", "Ⅱ", "II", "Osmo360IIPro", "Osmo360III"):
            with self.subTest(name=name):
                draft = valid_draft().replace("↳跑起来最怕", f"↳{name}跑起来最怕")
                result, report = self.run_checker(draft, extra_args=["--allow-second-gen-id", "1"])

                self.assertEqual(result.returncode, 1)
                self.assertIn("E_SECOND_GEN_NAME_FORMAT", {item["code"] for item in report["diagnostics"]})

    def test_unapproved_second_generation_claim_is_rejected(self) -> None:
        draft = valid_draft().replace("↳跑起来最怕", "↳这台二代跑起来最怕")
        result, report = self.run_checker(draft)

        self.assertEqual(result.returncode, 1)
        self.assertIn("E_SECOND_GEN_EVIDENCE", {item["code"] for item in report["diagnostics"]})

    def test_ambiguous_second_generation_id_does_not_grant_access(self) -> None:
        first = valid_draft().replace("Osmo360能", "Osmo360II能")
        second = valid_draft("## 1｜https://example.com/second").replace("Osmo360能", "Osmo360II能")
        result, report = self.run_checker(
            first + "\n" + second,
            extra_args=["--allow-second-gen-id", "1"],
        )

        self.assertEqual(result.returncode, 1)
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertIn("E_SECOND_GEN_ALLOW_ID_AMBIGUOUS", codes)
        self.assertIn("E_SECOND_GEN_EVIDENCE", codes)


if __name__ == "__main__":
    unittest.main()
