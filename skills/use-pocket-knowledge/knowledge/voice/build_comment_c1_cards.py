#!/usr/bin/env python3
"""Build a small, source-checked C1 train-comment layer without copying records."""
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent.parent
PREFIX = "comment_c1_"


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path(value):
    p = Path(value)
    if p.is_absolute():
        return p
    for candidate in (ROOT / p, PROJECT / p):
        if candidate.is_file():
            return candidate
    raise ValueError("source path unavailable")


def rid(short):
    return "xiaohongshu:" + short


SPECS = [
    {
        "id": "comment_c1_001", "status": "pattern", "title": "想复现成片，先问清拍摄和导出路径",
        "situation": "评论者围绕作品或父句提到的成片发问，尚不能分清它怎样拍出或导出",
        "need": "确定图片、视频、实况和App导出之间具体走了哪一步",
        "stage": "asking_about_workflow", "stance": "好奇，并保留自己尚未弄清的部分",
        "expression_purpose": "把成片兴趣落在一个能回答的操作问题上",
        "mechanism": "问题具体到拍照片还是录视频、是否直接截图、有没有额外处理；有父句时接住对方刚说的步骤继续缩小问题，主评论也可直接提出路径疑问。",
        "mechanism_ids": ["6a02c0370000000029035819", "6a284cc4000000002702fee1", "6a827035000000001c010cba"],
        "contributions": {4: "接住导出设置的父句，区分照片与视频，并说明自己得到的结果没有动态。",
                          13: "接住视频截图App导出的回答，追问有没有后期，并保留自己结果模糊但原因未知。",
                          15: "主评论直接询问是否先录视频再截图成图片。"},
        "transferable": ["围绕前一句已有步骤问一个仍不明白的环节", "区分操作路径和结果，不替提问者诊断原因"],
        "not_transferable": ["各评论者自己没有动态或图片模糊的经历", "原帖实际画面和摄制设备", "父句关于实况、水印、App及固件的说法不能直接变成官方操作事实"],
        "tags": ["拍摄路径", "导出", "视频截图", "实况", "后期", "不知道原因", "追问"],
    },
    {
        "id": "comment_c1_002", "status": "pattern", "title": "用同感接住父句的偏好或处境",
        "situation": "父句已经说出一个纠结、偏好或使用落差，回复者发现有相似的当下感受",
        "need": "确认自己也有相似关注，或补一点自己的具体处境",
        "stage": "sharing_same_feeling", "stance": "同感；可以简短，也可以带有限自述",
        "expression_purpose": "维持同一个讨论点，让对方知道有人接住了这句话",
        "mechanism": "回复可短到一句我也是，也可把等待多久、用了几次等有限自述放在也字旁边；长度取决于本句有多少自己的内容，不固定增加参数、建议或购买结论。",
        "mechanism_ids": ["6a49239b0000000015008eb1", "6a674d660000000014038874", "6a901cbe0000000015011bb8"],
        "contributions": {2: "用俺也是承接外观与长焦之间的纠结。",
                          9: "用我也是承接冷白调偏好，未将偏好改写成客观优劣。",
                          16: "回应闲置的父句，补充等待一个月、只用一次的自述。"},
        "transferable": ["让简短认同仍能对上明确父句", "有自己的处境才补一句，不替角色添加经历"],
        "not_transferable": ["原评论者等货、买机、只用一次或闲置的经历", "不能据同感回复估算人群比例、型号闲置率或认定评论者为独立认证消费者"],
        "tags": ["同感", "简短回复", "偏好", "纠结", "闲置自述", "楼中楼"],
    },
    {
        "id": "comment_c1_003", "status": "case", "title": "听说可以保存参数，仍需要具体操作步骤",
        "situation": "教程帖下有人担心每次重新设置，听到可以保存后仍不知道怎么操作",
        "need": "把能不能保存的问题推进到如何操作；保留转述者尚未尝试的边界",
        "stage": "learning_operation", "stance": "求助与不确定的转述并存",
        "expression_purpose": "指出当前操作缺口，并承接对方能够提供何种说明",
        "mechanism": "根评论先问重复设置负担；一条回复明确据说、还没试过，另一条可以保存的回答又引出详细步骤请求，随后出现录视频说明的提议。只记录实际说出的推进，不假定说明已发送或问题已解决。",
        "mechanism_ids": ["6a1a3a67000000002900fbaa", "6a1d1f2c000000002b0037fe", "6a217c92000000002803ac4d", "6a2186ee0000000028031781"],
        "contributions": {5: "同一根线程实际出现参数复用疑问、未尝试的限定、详细操作请求及录视频说明的提议。"},
        "transferable": ["分开能不能做与不知道怎么做", "据说和没试过要保留", "把帮助方式写在对方具体请求之后"],
        "not_transferable": ["不能把保存参数及下次套用的评论说法直接当已核实功能", "不推断发言者年龄、技术身份或整体熟练度", "提议录视频不等于已经完成指导"],
        "tags": ["参数", "保存", "重复设置", "详细步骤", "据说", "没试过", "求助"],
    },
    {
        "id": "comment_c1_004", "status": "case", "title": "在外观和长焦之间纠结，用自己的用法解释取舍",
        "situation": "同一线程里先表达喜欢4的外观又想要4P长焦，后续有人说明自己目前的决定",
        "need": "把对两款的不同偏好连到平时怎样拍、已有设备能补什么",
        "stage": "comparing_options", "stance": "纠结之后给出个人用途范围内的取舍",
        "expression_purpose": "解释为什么自己这样选，而不是替所有人判断哪款更值得",
        "mechanism": "根评论用平时手机经常放大作为想要长焦的理由；后续回复用日常记录、偶尔出游和自己的手机仍有长焦说明个人选择。两条发言不合并成同一个人的转变。",
        "mechanism_ids": ["6a3a9114000000002a0270da", "6a49299b00000000150152be"],
        "contributions": {2: "一条明确双重偏好的根评论，与同线程中基于个人日常用途和现有手机的决定说明。"},
        "transferable": ["先给出正在拉扯的两点，再解释自己的使用需求", "将建议的范围限定在说话者表达的用途内"],
        "not_transferable": ["根评论和后续回复不视为同一个人的决策历程", "实际持有手机、使用习惯、购买决定不移植给写手", "原话关于4P体积、耗电及4的变焦是否够用不升级成客观性能结论"],
        "tags": ["Pocket4", "Pocket4P", "外观", "长焦", "手机", "日常记录", "用途取舍"],
    },
    {
        "id": "comment_c1_005", "status": "case", "title": "看到优惠价，继续追问门店操作和适用范围",
        "situation": "有人报出特定地区买价，回复者想在自己的时间安排内弄清怎么领、在哪买",
        "need": "确认优惠如何办理，以及不同门店反馈是否一致",
        "stage": "checking_purchase_conditions", "stance": "具体求助；有不同反馈时保留差异",
        "expression_purpose": "让价格讨论落到地点、操作和本人实际询问得到的条件",
        "mechanism": "低价自述引出带下周要用这一时限的操作询问；店员现场办理的回答又收到多家店不参与的不同自述。不能把其中任一句推广为所有地区、门店和时间通用。",
        "mechanism_ids": ["6a74c4bb0000000007014e2e", "6a787c71000000000300a7f2"],
        "contributions": {1: "同一优惠价线程内，明确步骤请求与不同门店反馈之间有实际直接父句关系。"},
        "transferable": ["把价格疑问具体到适用地点、办理方式和时间", "遇到不同信息时说明自己问到的范围"],
        "not_transferable": ["评论中的价钱、国补、店员操作与门店参与范围不当作当前政策或购买建议", "下周要用和询问多家店属于原发言者的自述，不转移给新角色"],
        "tags": ["价格", "优惠", "门店", "操作步骤", "适用范围", "时间限制", "追问"],
    },
]


COMMON_LIMITATIONS = [
    "只读取本批实际导出的train评论文字及线程字段；图片、连续视频、音轨和设备UI均未读取。",
    "commenter_identity_unverified：本批评论者author_id为空；昵称不作为个人身份、独立消费者或亲历认证。",
    "pattern的作者去重指作品发布账号；至少3独立作品和3个可核对作品作者，不表示3位已认证消费者、人口比例或商业独立性。",
    "stage只表示这句话呈现的处境，不推断人口身份、职业、年龄或长期熟练度。",
    "第一人称保持原评论者归属，只证明其写过这段话；公共原话不能替换成写手的经历。",
    "父句仅按实际parent_id定位同work的评论；root_id只作根线程，不据相邻行或昵称补父句。",
    "作品主型号是讨论对象，不证明每位评论者持有该型号；比较帖中的旧型号和4P提及保留原义。",
    "评论中的产品、参数、价格、补贴和效果说法不自动成为事实；写入新文稿需另核官方来源与条件。",
]


def build():
    if any("C2" in c.get("evidence_batches", []) for c in rows(ROOT / "voice/cards.jsonl") if c["id"].startswith(PREFIX)):
        raise ValueError("C1 rebuild refused: later C2 evidence exists; use the versioned C2 builder instead")
    comment_path = ROOT / "corpus/comments.jsonl"
    # Split filtering happens before selecting or displaying any comment text.
    train = {r["id"]: r for r in rows(comment_path) if r.get("split") == "train" and r.get("material_kind", "comment") == "comment"}
    works = {w["work_id"]: w for w in rows(ROOT / "corpus/works.jsonl") if w.get("split") == "train"}
    eligible = {wid for wid, w in works.items() if w.get("status") == "success" and w.get("model_id") in {"pocket_4", "pocket_4p"} and w.get("sampling_status") != "excluded" and w.get("author_id")}
    reviewed = {identifier: r for identifier, r in train.items() if r["work_id"] in eligible and works[r["work_id"]].get("input_order") <= 20}
    norm_cache = {}

    def verify(identifier):
        if identifier not in reviewed:
            raise ValueError("support is not an eligible C1 train comment: " + identifier)
        r = reviewed[identifier]
        if not isinstance(r.get("text"), str) or not r["text"].strip():
            raise ValueError("support text absent: " + identifier)
        occurrences = r.get("source_occurrences", [])
        if not occurrences:
            raise ValueError("source occurrences absent: " + identifier)
        for occurrence in occurrences:
            np = path(occurrence["normalized_path"])
            if sha(np) != occurrence["normalized_sha256"]:
                raise ValueError("normalized source hash changed")
            if np not in norm_cache:
                norm_cache[np] = {n: item for n, line in enumerate(np.read_text(encoding="utf-8").splitlines(), 1)
                                  if line.strip() for item in [json.loads(line)] if item.get("split") == "train"}
            actual = norm_cache[np].get(occurrence["normalized_line"])
            if not actual:
                raise ValueError("train source line missing")
            for field in ("id", "work_id", "platform", "split", "text", "parent_id", "root_id", "thread_role"):
                if actual.get(field) != r.get(field):
                    raise ValueError("actual source mismatch: " + field)
            if sha(path(occurrence["source_path"])) != occurrence["source_sha256"] or actual["source_locator"] != occurrence["source_locator"]:
                raise ValueError("raw source provenance mismatch")
        return r

    def complete_context(mechanism_ids):
        found = set()
        for identifier in mechanism_ids:
            seen = set()
            current = identifier
            while current:
                if current in seen:
                    raise ValueError("thread cycle")
                seen.add(current)
                r = verify(current)
                if r["work_id"] != verify(identifier)["work_id"]:
                    raise ValueError("cross-work parent")
                found.add(current)
                parent = r.get("parent_id")
                if r.get("thread_role") == "reply" and not parent:
                    raise ValueError("selected reply has no explicit parent")
                current = parent
            root = r
            if root.get("thread_role") != "root" or root.get("root_id") not in {None, root["id"]}:
                raise ValueError("actual root not resolved")
            for node in seen:
                if reviewed[node].get("root_id") not in {None, root["id"]}:
                    raise ValueError("root mismatch")
        return sorted(found, key=lambda x: (works[reviewed[x]["work_id"]]["input_order"], reviewed[x]["source_occurrences"][0]["normalized_line"]))

    cards = []
    for spec in SPECS:
        mechanism_ids = [rid(x) for x in spec["mechanism_ids"]]
        support_ids = complete_context(mechanism_ids)
        support_works = sorted({reviewed[x]["work_id"] for x in mechanism_ids}, key=lambda wid: works[wid]["input_order"])
        author_ids = sorted({works[wid]["author_id"] for wid in support_works})
        if spec["status"] == "pattern" and (len(support_works) < 3 or len(author_ids) < 3):
            raise ValueError("pattern needs three independent works and work authors")
        if max(Counter(works[wid]["author_id"] for wid in support_works).values()) > 2:
            raise ValueError("work-author cap exceeded")
        card = {k: v for k, v in spec.items() if k not in {"mechanism_ids", "contributions"}}
        excerpts, links = [], []
        for identifier in support_ids:
            r = verify(identifier)
            occurrence = r["source_occurrences"][0]
            column = r["source_columns"]["text"]["column"]
            excerpts.append({"record_id": identifier, "field": "text", "quote": r["text"], "char_start": 0,
                             "char_end": len(r["text"]), "offset_convention": "zero_based_unicode_codepoints_end_exclusive",
                             "evidence_role": "mechanism" if identifier in mechanism_ids else "actual_parent_or_root_context",
                             "source_path": str(path(occurrence["normalized_path"])),
                             "source_locator": {"line": occurrence["normalized_line"], "json_pointer": "/text",
                                                "original_file": occurrence["source_path"], **occurrence["source_locator"],
                                                "column": column, "cell": f"{column}{occurrence['source_locator']['row']}"},
                             "source_sha256": occurrence["normalized_sha256"], "raw_source_sha256": occurrence["source_sha256"]})
            if r.get("parent_id"):
                parent = verify(r["parent_id"])
                links.append({"record_id": identifier, "parent_id": parent["id"], "root_id": r.get("root_id"),
                              "basis": "exported_reference_id_and_actual_same_work_records",
                              "reply_text": r["text"], "parent_text": parent["text"],
                              "reply_source_locator": excerpts[-1]["source_locator"],
                              "parent_source_occurrences": parent["source_occurrences"]})
        card.update({"experience_level": "只判断句中显露的操作疑问与表述边界，实际熟练度未认证",
                     "source_kind": "public_comment", "material_kind": "comment", "speaker_scope": "comment_author",
                     "response_context": "真实评论根句或明确父句；具体承接关系见thread_links，不从帖子自述推回复关系",
                     "stage_scope": "expressed_situation_not_person_identity", "split": "train",
                     "model_ids": sorted({works[wid]["model_id"] for wid in support_works}),
                     "evidence_refs": support_ids, "mechanism_evidence_refs": mechanism_ids,
                     "work_ids": support_works, "author_ids": author_ids, "author_scope": "work_publisher_accounts",
                     "commenter_identity_unverified": True,
                     "evidence_excerpts": excerpts, "thread_links": links,
                     "support_members": [{"work_id": wid, "input_order": works[wid]["input_order"],
                                          "author_id": works[wid]["author_id"], "author_scope": "work_publisher_account",
                                          "model_id": works[wid]["model_id"],
                                          "record_ids": [x for x in mechanism_ids if reviewed[x]["work_id"] == wid],
                                          "context_record_ids": [x for x in support_ids if reviewed[x]["work_id"] == wid and x not in mechanism_ids],
                                          "contribution": spec["contributions"][works[wid]["input_order"]]} for wid in support_works],
                     "support_counts": {"independent_works": len(support_works), "distinct_work_publisher_accounts": len(author_ids),
                                        "comment_records_including_context": len(support_ids), "mechanism_comment_records": len(mechanism_ids),
                                        "independently_verified_commenter_accounts": 0},
                     "analysis_basis": "editorial_synthesis_of_actual_train_comment_text_and_explicit_parent_relations",
                     "limitations": COMMON_LIMITATIONS, "checked_at": date.today().isoformat(),
                     "independent_review_status": "pending", "new_comment_records_created": 0})
        cards.append(card)

    card_path = ROOT / "voice/cards.jsonl"
    existing = [r for r in rows(card_path) if not r["id"].startswith(PREFIX)]
    card_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in existing + cards), encoding="utf-8")
    scene_specs = {
        "scenario_002": (["comment_c1_002"], ["6a81e14e000000002902ebe3", "6a901cbe0000000015011bb8"],
                         "仅input16中有限的闲置自述与同感回应；不证明不会使用是唯一原因，不估计闲置比例。"),
        "scenario_003": (["comment_c1_001"], ["6a276b9d000000002702baaa", "6a284cc4000000002702fee1"],
                         "仅input13中接住App视频截图回答、继续询问后期处理与模糊原因的个案；不是App能力或模糊原因核验。"),
        "scenario_004": (["comment_c1_004"], ["6a3a9114000000002a0270da", "6a49299b00000000150152be"],
                         "input2评论把4/4P取舍连到日常手机放大、外观和已有设备；两段属于不同发言位置，不合并为同一个人的亲历。"),
        "scenario_005": (["comment_c1_001", "comment_c1_003"], ["6a02c0370000000029035819", "6a284cc4000000002702fee1", "6a827035000000001c010cba", "6a217c92000000002803ac4d"],
                         "三个独立作品支持拍摄/导出路径疑问；另一个教程线程提供需要详细步骤的个案。只知道评论者如何问，未读原片或验证回答。"),
        "scenario_009": (["comment_c1_004"], ["6a3a9114000000002a0270da", "6a49299b00000000150152be"],
                         "补充4/4P外观、长焦和个人用途之间的有限取舍表达；原场景仍为editorial_hypothesis，不升级为群体偏好或型号性能比较结论。"),
    }
    scene_path = ROOT / "scenarios/cards.jsonl"
    scenes = rows(scene_path)
    for scene in scenes:
        if scene["id"] not in scene_specs:
            continue
        card_ids, short_ids, scope = scene_specs[scene["id"]]
        refs = [rid(x) for x in short_ids]
        scene["voice_card_ids"] = list(dict.fromkeys(scene.get("voice_card_ids", []) + card_ids))
        existing_support = scene.get("new_public_comment_support", [])
        if not isinstance(existing_support, list):
            existing_support = [existing_support]
        scene["new_public_comment_support"] = [s for s in existing_support if s.get("batch_id") != "C1"] + [{
            "batch_id": "C1", "source_kind": "public_comment", "split": "train", "speaker_scope": "comment_author",
            "voice_card_ids": card_ids, "evidence_refs": refs,
            "work_ids": sorted({reviewed[x]["work_id"] for x in refs}), "scope": scope,
            "basis_status": "actual_train_comment_support_separate_from_original_scenario_and_product_basis",
            "product_capabilities_confirmed_by_comments": False, "commenter_identity_unverified": True,
            "checked_at": date.today().isoformat()}]
    scene_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in scenes), encoding="utf-8")
    all_refs = {ref for c in cards for ref in c["evidence_refs"]}
    all_works = {reviewed[ref]["work_id"] for ref in all_refs}
    report = {"source_kind": "public_comment", "batch": "C1", "split": "train", "reviewed_train_records": len(reviewed),
              "reviewed_work_orders": sorted(works[wid]["input_order"] for wid in {r['work_id'] for r in reviewed.values()}),
              "excluded_before_text_analysis": {"unknown_model_input_orders": [3], "sampling_excluded_input_orders": [7, 17, 18], "all_holdout": True},
              "new_cards": len(cards), "new_patterns": sum(c["status"] == "pattern" for c in cards),
              "new_cases": sum(c["status"] == "case" for c in cards), "unique_referenced_comments": len(all_refs),
              "unique_referenced_works": len(all_works), "distinct_work_publisher_accounts": len({works[wid]['author_id'] for wid in all_works}),
              "exact_quote_occurrences": sum(len(c["evidence_excerpts"]) for c in cards),
              "verified_direct_parent_pairs_including_reuse": sum(len(c["thread_links"]) for c in cards),
              "unique_verified_direct_parent_pairs": len({(link["record_id"], link["parent_id"]) for c in cards for link in c["thread_links"]}),
              "new_records_created": 0, "new_main_comment_count_contribution": 0, "existing_comment_ids_reused": True,
              "commenter_identity_unverified": True, "all_selected_parent_chains_resolve_to_actual_root": True,
              "source_snapshot": {"comments": sha(comment_path), "works": sha(ROOT / 'corpus/works.jsonl'), "cards": sha(card_path)},
              "independent_review_status": "pending", "limitations": COMMON_LIMITATIONS}
    report["scenario_ids_with_new_comment_support"] = sorted(scene_specs)
    report["scenario_original_basis_changed"] = False
    (ROOT / "voice/comment-c1-build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("reviewed_train_records", "new_cards", "new_patterns", "new_cases", "unique_referenced_comments",
                                            "unique_referenced_works", "exact_quote_occurrences", "verified_direct_parent_pairs_including_reuse", "new_records_created")}, ensure_ascii=False))


if __name__ == "__main__":
    build()
