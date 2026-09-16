#!/usr/bin/env python3
"""Extend C1 mechanisms with actual C2 train comments whose thread role is unknown."""
from collections import Counter
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent.parent
BATCH = "xiaohongshu-comments-02"
CHANGED = {"comment_c1_001", "comment_c1_003", "comment_c1_004"}
ADDITIONAL_LIMITS = [
    "C2导出没有根评论或引用关系字段；C2记录thread_role=unknown、parent_id/root_id=null，不称主评、回复承接或已证对话。",
    "C2摘句只支持单句中的观点、问题或建议；不据语气、昵称、相邻行或帖子内容补父句。",
    "评论者身份、实际持有、个人经历、商业独立性与建议效果未认证；产品、环境与效果说法不当官方事实。",
]
EXTENSIONS = {
    "comment_c1_001": {
        "ids": ["6a7ac5f400000000100132c2", "6a1421d2000000002902c07b", "6a1560f6000000002a007222"],
        "scope": "仅补充参数适用拍照模式、是否由视频截取及App传到手机的独立问题；不新增回复承接证据。",
        "contributions": {23: "独立评论询问参数是否用于拍照。", 24: "独立评论分别询问视频截取和App传到手机路径，未证明两句存在对话关系。"},
        "updates": {"transferable": ["有可核对父句时，围绕其中已有步骤问一个仍不明白的环节", "区分操作路径和结果，不替提问者诊断原因"]},
    },
    "comment_c1_003": {
        "ids": ["6a7aea47000000002b02a463"],
        "scope": "只补充每次是否重新调参数的顾虑；C1的听说能保存后仍需步骤仅由原有明确线程支持。",
        "contributions": {23: "单句问每次拍摄是否需要重新调；没有父句或后续回答。"},
    },
    "comment_c1_004": {
        "ids": ["6a4cf3fe0000000015009660", "6a3b43c5000000002b0037d4", "6a8b37000000000015010578", "6a52611900000000050150b6"],
        "scope": "三个新增Pocket4P讨论作品分别出现旅行用途、自述新手且不看价格、排除价格后关注发热或人像的单句选择问题。",
        "contributions": {31: "去英国旅游这一具体用途与4/4P选择放在同一句。", 34: "自述新手并排除价格，限定自己需要的推荐。", 38: "两条独立评论分别排除价格后关注发热、人像表现；不合并为同一个人的偏好。"},
        "updates": {
            "title": "比较4与4P，先说自己的用途和取舍条件", "status": "pattern",
            "situation": "评论者选择4或4P时，将犹豫连到自己的用途、已有设备或更在意的条件",
            "need": "让推荐或个人决定围绕实际拍什么、在意什么和哪些条件暂不考虑",
            "stance": "带着具体偏好或限制比较，不只问哪台更强",
            "expression_purpose": "让推荐问题或个人决定与本句提出的用途和条件对应",
            "mechanism": "先交代日常用途、旅行安排、已有手机，或明确暂不考虑价格而关注发热、人像等条件，再提出选择疑问或说明个人取舍。C1保留实际线程中的表达，C2仅支持独立评论提出的条件；各条发言不拼成同一人的决策历程。",
            "transferable": ["说清决定与自己的哪项用途有关", "明确更在意什么、哪些条件暂不考虑，让问题可以被具体回答"],
            "tags": ["Pocket4", "Pocket4P", "外观", "长焦", "手机", "旅行", "人像", "发热关注", "不看价格", "用途取舍"],
        },
    },
}
NEW = [
    {
        "id": "comment_c2_001", "status": "case", "title": "把出片压力缩小到先熟悉的步骤和日常场景",
        "situation": "评论中有人建议刚接触设备时先熟悉基础操作，再从常见日常拍摄开始",
        "need": "给开始练习的人一个较具体、较小的起点",
        "experience_level": "只是评论中的建议，不认证建议者熟练度或接收者身份",
        "stage": "suggesting_a_small_practice_step", "stance": "建议先熟悉和尝试",
        "expression_purpose": "把抽象的出大片要求拆成基础功能或几个日常拍摄对象",
        "mechanism": "一篇作品下的评论提出先熟悉基础参数和功能；另一篇的评论明确到广角与中焦切换，或吃饭、散步、通勤这些场景。只学习建议怎样落地，不把建议写成已经有效的学习路线。",
        "ids": ["6a4cc43e000000002b02bc03", "6a5cf40c0000000029035a7e", "6a624b60000000002a02f139"],
        "quotes": {"6a4cc43e000000002b02bc03": "我觉得先不要着急刚到手就想出大片，先熟悉一下基础参数和功能吧"},
        "contributions": {38: "评论提出先熟悉基础参数和功能；不采纳其中对作者新手身份或图片光线的判断。", 40: "独立评论把练习起点具体到镜头切换和吃饭、散步、通勤。"},
        "transferable": ["建议具体到当前可以练的一步或一种日常场景", "区分提出建议与证明建议有效"],
        "not_transferable": ["不能认定作者是新手或实际画面光线差", "不承诺多用就一定拍出大片", "未观看示例，不认定双摄切换操作方式或任何成片效果"],
        "tags": ["Pocket4P", "基础操作", "练习", "日常记录", "镜头切换", "吃饭", "散步", "通勤"],
    },
    {
        "id": "comment_c2_002", "status": "case", "title": "交代手里只有机器，让配件问题更具体",
        "situation": "一条评论说自己只有机器，尚不知道还有哪些配件需要考虑",
        "need": "弄清当前已有东西与可能需要补充的东西之间的差距",
        "experience_level": "仅来自句中对现有物品的自述，不推断长期熟练度",
        "stage": "asking_about_accessory_needs", "stance": "具体求助",
        "expression_purpose": "提供现有配置，让配件问题有明确起点",
        "mechanism": "同一句先问有什么需要买的配件，再交代目前只有机器；这条实际缺口比泛泛问配件推荐更具体，但没有说明拍摄场景或预算，仍不能直接替其列必买清单。",
        "ids": ["6a8e9f490000000014033eb1"], "contributions": {37: "仅有机器这一自述和配件疑问在同一句，未见可核对父句或回复。"},
        "transferable": ["提问时交代已经有什么", "现有条件不足时保留未知，不直接罗列必买配件"],
        "not_transferable": ["只有机器是原发言者自述，不转移给写手", "不能推定已购套餐、实际持有型号或具体使用场景", "不把任何配件当作已证明必需或兼容"],
        "tags": ["Pocket4P", "配件", "现有配置", "只有机器", "需要什么", "求助"],
    },
]


def read_rows(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_rows(p, values):
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in values), encoding="utf-8")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def resolve(value):
    p = Path(value)
    for q in ([p] if p.is_absolute() else [ROOT / p, PROJECT / p]):
        if q.is_file():
            return q.resolve()
    raise ValueError("source missing")


def build():
    cp, wp = ROOT / "corpus/comments.jsonl", ROOT / "corpus/works.jsonl"
    train = {r["id"]: r for r in read_rows(cp) if r.get("split") == "train" and r.get("material_kind") == "comment"}
    works = {w["work_id"]: w for w in read_rows(wp) if w.get("split") == "train"}
    eligible = {wid for wid, w in works.items() if w.get("status") == "success" and w.get("model_id") in {"pocket_4", "pocket_4p"} and w.get("sampling_status") != "excluded" and w.get("author_id")}
    reviewed = {i: r for i, r in train.items() if r["work_id"] in eligible and any(o.get("batch_id") == BATCH for o in r.get("source_occurrences", []))}
    cache = {}

    def verify(short):
        identifier = "xiaohongshu:" + short
        r = reviewed[identifier]
        assert r.get("thread_role") == "unknown" and r.get("parent_id") is None and r.get("root_id") is None
        assert isinstance(r.get("text"), str) and r["text"].strip()
        o = next(o for o in r["source_occurrences"] if o.get("batch_id") == BATCH)
        np = resolve(o["normalized_path"])
        assert sha(np) == o["normalized_sha256"] and sha(resolve(o["source_path"])) == o["source_sha256"]
        if np not in cache:
            cache[np] = {n: x for n, l in enumerate(np.read_text(encoding="utf-8").splitlines(), 1) if l.strip()
                         for x in [json.loads(l)] if x.get("split") == "train"}
        actual = cache[np][o["normalized_line"]]
        for key in ("id", "work_id", "split", "text", "parent_id", "root_id", "thread_role", "source_locator"):
            assert actual.get(key) == r.get(key), key
        return r, o

    def excerpt(short, selected_quote=None):
        r, o = verify(short)
        quote = selected_quote or r["text"]
        start = r["text"].index(quote)
        column = r["source_columns"]["text"]["column"]
        return {"record_id": r["id"], "field": "text", "quote": quote, "char_start": start, "char_end": start + len(quote),
                "offset_convention": "zero_based_unicode_codepoints_end_exclusive", "evidence_role": "independent_comment_expression_only",
                "batch_id": "C2", "thread_role": "unknown", "parent_id": None, "root_id": None,
                "source_path": str(resolve(o["normalized_path"])), "source_sha256": o["normalized_sha256"],
                "raw_source_sha256": o["source_sha256"],
                "source_locator": {"line": o["normalized_line"], "json_pointer": "/text", "original_file": o["source_path"],
                                   **o["source_locator"], "column": column, "cell": f"{column}{o['source_locator']['row']}"}}

    def enrich(card, spec):
        excerpts = [excerpt(short, spec.get("quotes", {}).get(short)) for short in spec["ids"]]
        refs = [e["record_id"] for e in excerpts]
        card["evidence_excerpts"] = card.get("evidence_excerpts", []) + excerpts
        card["evidence_refs"] = list(dict.fromkeys(card.get("evidence_refs", []) + refs))
        card["mechanism_evidence_refs"] = list(dict.fromkeys(card.get("mechanism_evidence_refs", []) + refs))
        wids = sorted({train[x]["work_id"] for x in card["evidence_refs"]}, key=lambda wid: works[wid]["input_order"])
        card["work_ids"] = wids
        card["author_ids"] = sorted({works[wid]["author_id"] for wid in wids})
        card["model_ids"] = sorted({works[wid]["model_id"] for wid in wids})
        card["support_members"] = card.get("support_members", []) + [
            {"work_id": wid, "input_order": works[wid]["input_order"], "author_id": works[wid]["author_id"],
             "author_scope": "work_publisher_account", "model_id": works[wid]["model_id"], "batch_id": "C2",
             "record_ids": [i for i in refs if train[i]["work_id"] == wid], "context_record_ids": [],
             "thread_scope": "independent_comment_expression_only; unknown_root_or_reply",
             "contribution": spec["contributions"][works[wid]["input_order"]]}
            for wid in sorted({reviewed[i]["work_id"] for i in refs}, key=lambda x: works[x]["input_order"])]
        card["support_counts"] = {"independent_works": len(wids), "distinct_work_publisher_accounts": len(card["author_ids"]),
                                  "comment_records_including_context": len(card["evidence_refs"]),
                                  "mechanism_comment_records": len(card["mechanism_evidence_refs"]),
                                  "independently_verified_commenter_accounts": 0,
                                  "c2_independent_comment_records": len(refs), "c2_verified_parent_pairs": 0}
        card["commenter_identity_unverified"] = True
        card["author_scope"] = "work_publisher_accounts"
        card["split"] = "train"
        card["source_kind"] = "public_comment"
        card["material_kind"] = "comment"
        card["speaker_scope"] = "comment_author"
        card["stage_scope"] = "expressed_situation_not_person_identity"
        card["checked_at"] = date.today().isoformat()
        card["previous_independent_review_ref"] = card.pop("independent_review_ref", None)
        card["independent_review_status"] = "pending"
        card["limitations"] = list(dict.fromkeys(card.get("limitations", []) + ADDITIONAL_LIMITS))
        card["new_comment_records_created"] = 0
        if card["status"] == "pattern":
            assert len(wids) >= 3 and len(card["author_ids"]) >= 3
        assert max(Counter(works[wid]["author_id"] for wid in wids).values()) <= 2
        return card

    card_path = ROOT / "voice/cards.jsonl"
    current = read_rows(card_path)
    assert not any(set(c.get("evidence_batches", [])) - {"C1", "C2"} for c in current if c["id"] in CHANGED or c["id"].startswith("comment_c2_")), "later extensions exist"
    base_path = ROOT / "voice/revisions/comment-c1-before-c2.jsonl"
    if not base_path.exists():
        base_path.parent.mkdir(parents=True, exist_ok=True)
        assert all("C2" not in c.get("evidence_batches", []) for c in current if c["id"] in CHANGED)
        write_rows(base_path, [c for c in current if c["id"] in CHANGED])
    baseline = {c["id"]: c for c in read_rows(base_path)}
    updates = {}
    for identifier, spec in EXTENSIONS.items():
        card = deepcopy(baseline[identifier])
        card.update(spec.get("updates", {}))
        card["evidence_batches"] = ["C1", "C2"]
        card["evidence_extensions"] = [{"batch_id": "C2", "scope": spec["scope"], "root_reply_relationships_available": False}]
        card["response_context"] = "C1关系仅由既有thread_links支持；C2为独立评论文字，根/回复角色未知，不能推定父句或承接关系"
        card["analysis_basis"] = "editorial_synthesis_with_separate_C1_thread_and_C2_independent_comment_scopes"
        updates[identifier] = enrich(card, spec)
    for spec in NEW:
        card = {k: v for k, v in spec.items() if k not in {"ids", "quotes", "contributions"}}
        card.update(evidence_batches=["C2"], thread_links=[], response_context="独立评论文字；root/reply角色未知，没有可核对父句",
                    analysis_basis="editorial_synthesis_of_actual_train_comment_text_without_thread_inference")
        updates[card["id"]] = enrich(card, spec)
    out = [updates.pop(c["id"], c) for c in current if not c["id"].startswith("comment_c2_")]
    out += list(updates.values())
    write_rows(card_path, out)

    scene_specs = {
        "scenario_002": (["comment_c2_001"], ["6a5cf40c0000000029035a7e", "6a624b60000000002a02f139"], "只支持把开始使用的建议具体到基础切换和常拍日常；不证明采纳、学习效果或闲置原因。"),
        "scenario_003": (["comment_c1_001"], ["6a1421d2000000002902c07b", "6a1560f6000000002a007222"], "仅补充视频截取与App传到手机的独立路径问题，不能当作已核对回复或实际导出能力。"),
        "scenario_005": (["comment_c1_001", "comment_c1_003"], ["6a7ac5f400000000100132c2", "6a7aea47000000002b02a463"], "仅补充参数适用于拍照吗、是否每次重新调的独立疑问；没有父句或回复结果。"),
        "scenario_009": (["comment_c1_004"], ["6a4cf3fe0000000015009660", "6a3b43c5000000002b0037d4", "6a8b37000000000015010578", "6a52611900000000050150b6"], "三个4P讨论作品给出旅行、经验自述及排除价格后关注发热/人像的选择条件。原场景仍editorial_hypothesis，不认证性能、群体偏好或购买建议。"),
    }
    scene_path = ROOT / "scenarios/cards.jsonl"
    scenes = read_rows(scene_path)
    for scene in scenes:
        if scene["id"] == "scenario_006":
            scene["new_public_comment_support"] = [p for p in scene.get("new_public_comment_support", []) if p.get("batch_id") != "C2"]
            if not scene["new_public_comment_support"]:
                scene.pop("new_public_comment_support", None)
            scene["voice_card_ids"] = [i for i in scene.get("voice_card_ids", []) if i != "comment_c2_002"]
        if scene["id"] not in scene_specs:
            continue
        ids, shorts, scope = scene_specs[scene["id"]]
        refs = [verify(x)[0]["id"] for x in shorts]
        scene["voice_card_ids"] = list(dict.fromkeys(scene.get("voice_card_ids", []) + ids))
        previous = scene.get("new_public_comment_support", [])
        scene["new_public_comment_support"] = [p for p in previous if p.get("batch_id") != "C2"] + [{
            "batch_id": "C2", "source_kind": "public_comment", "split": "train", "speaker_scope": "comment_author",
            "voice_card_ids": ids, "evidence_refs": refs, "work_ids": sorted({reviewed[x]["work_id"] for x in refs}),
            "thread_role": "unknown", "verified_parent_pairs": 0, "scope": scope,
            "basis_status": "independent_comment_text_separate_from_original_scenario_and_product_basis",
            "product_capabilities_confirmed_by_comments": False, "commenter_identity_unverified": True, "checked_at": date.today().isoformat()}]
    write_rows(scene_path, scenes)
    touched = [c for c in out if c["id"] in CHANGED or c["id"].startswith("comment_c2_")]
    c2refs = {e["record_id"] for c in touched for e in c["evidence_excerpts"] if e.get("batch_id") == "C2"}
    c2works = {reviewed[x]["work_id"] for x in c2refs}
    report = {"batch_id": "C2", "split": "train", "reviewed_records": len(reviewed),
              "reviewed_work_count": len({r['work_id'] for r in reviewed.values()}),
              "reviewed_records_by_model": dict(Counter(works[r['work_id']]['model_id'] for r in reviewed.values())),
              "excluded_before_text_analysis": {"unknown_model_input_orders": [22], "missing_export_input_orders": [21], "all_holdout": True},
              "extended_card_ids": sorted(CHANGED), "new_card_ids": [s['id'] for s in NEW],
              "status_change": {"comment_c1_004": {"from": "case", "to": "pattern", "basis": "four_independent_works_and_publishers_with_explicit_choice_conditions"}},
              "c2_unique_support_comments": len(c2refs), "c2_unique_support_works": len(c2works),
              "c2_distinct_work_publishers": len({works[wid]['author_id'] for wid in c2works}),
              "c2_support_by_model": dict(Counter(works[reviewed[x]['work_id']]['model_id'] for x in c2refs)),
              "c2_thread_role": "unknown", "new_verified_parent_pairs": 0, "new_records_created": 0,
              "new_main_comment_count_contribution": 0, "scenario_ids_with_new_support": sorted(scene_specs),
              "scenario_original_basis_changed": False, "independent_review_status": "pending",
              "source_hashes": {"comments": sha(cp), "works": sha(wp), "cards": sha(card_path), "c1_reviewed_base": sha(base_path)},
              "limitations": ADDITIONAL_LIMITS}
    (ROOT / "voice/comment-c2-build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("reviewed_records", "reviewed_work_count", "extended_card_ids", "new_card_ids", "c2_unique_support_comments", "c2_unique_support_works", "c2_support_by_model", "new_verified_parent_pairs", "new_records_created")}, ensure_ascii=False))


if __name__ == "__main__":
    build()
