#!/usr/bin/env python3
"""Rebuild the isolated historical language corpus, without collecting social links.

Only the three explicitly listed learning files are read. Old holdouts, authored
drafts and acceptance states are not comment corpus inputs.
"""
from __future__ import annotations

import hashlib
import json
import re
import argparse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "outputs/pocket-lh12-validation/research"
OUT = ROOT / "knowledge/pocket"
PLATFORMS = ("douyin", "xiaohongshu", "bilibili")
READ_SCOPE = "exported_post_text_and_comment_text_only; no_video_image_or_audio_review"
COMMON_LIMITATIONS = [
    "历史可见评论导出，不认证作者为真人、消费经历真实或不存在商业关系",
    "未核验评论排名及置顶；点赞只表示导出的评论点赞量",
    "本次仅迁移导出文字，未观看原作视频或图片、未听音轨",
    "网友参数、效果、价格和兼容说法不是官方产品事实",
    "split=legacy，不计入150篇新作品、新语料覆盖或新盲测",
]


def dump_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def models_in(text, allow_short=False):
    found = set()
    for m in re.finditer(r"(?<![a-z0-9])pocket[\s_-]*([1-4])([\s_-]*(?:pro|p))?(?![a-z0-9])", text, re.I):
        found.add("pocket_" + m[1] + ("p" if m[1] == "4" and m[2] else ""))
    if allow_short:
        for m in re.finditer(r"(?<![a-z0-9])p([1-4])(p)?(?![a-z0-9])", text, re.I):
            found.add("pocket_" + m[1] + ("p" if m[1] == "4" and m[2] else ""))
        if re.search(r"(?<![a-z0-9])4p(?![a-z0-9])", text, re.I):
            found.add("pocket_4p")
        if re.search(r"(?<![a-z0-9])4\s*(?:和|与|、|/)\s*4p(?![a-z0-9])", text, re.I):
            found.add("pocket_4")
    return sorted(found)


def work_model(fields):
    candidates = []
    for name, basis in (("视频标题", "post_title"), ("笔记标题", "post_title"),
                        ("视频描述", "post_description"), ("笔记内容", "post_description"),
                        ("视频话题", "post_tag"), ("笔记话题", "post_tag")):
        text = str(fields.get(name) or "")
        # Hashtags inside a description remain tag evidence, not a device claim.
        prose = text.split("#", 1)[0] if basis == "post_description" else text
        for model in models_in(prose):
            candidates.append({"model_id": model, "basis": basis, "field": name})
        if basis == "post_description" and "#" in text:
            for model in models_in(text.split("#", 1)[1]):
                candidates.append({"model_id": model, "basis": "post_tag", "field": name})
    ids = sorted({c["model_id"] for c in candidates})
    if len(ids) == 1:
        chosen = next(c for c in candidates if c["basis"] != "post_tag") if any(c["basis"] != "post_tag" for c in candidates) else candidates[0]
        return ids[0], chosen["basis"], candidates
    return "unknown", "multiple_post_models" if ids else "not_established_in_exported_post_text", candidates


def migrate():
    works, records, refs = [], [], {}
    for platform in PLATFORMS:
        source_path = BASE / f"{platform}-learning.json"
        source_relative = str(source_path.relative_to(ROOT))
        data = json.loads(source_path.read_text())
        assert len(data) == 6
        for wi, original_work in enumerate(data):
            fields = original_work["post_fields"]
            model, basis, declarations = work_model(fields)
            work_id = original_work["workId"]
            original_metadata = {k: v for k, v in original_work.items() if k != "comments"}
            work = {
                "id": original_work["id"], "work_id": work_id, "platform": platform,
                "url": original_work["url"],
                "title": fields.get("视频标题") or fields.get("笔记标题") or original_work.get("title_hint"),
                "model_id": model, "model_basis": basis, "model_declarations": declarations,
                "source_path": source_relative, "source_locator": {"json_pointer": f"/{wi}"},
                "source_sha256": digest(source_path),
                "collected_at": original_work.get("capture_start"),
                "capture_end": original_work.get("capture_end"),
                "read_scope": READ_SCOPE, "timestamp_timezone": "not_recorded_in_export",
                "split": "legacy", "source_kind": "historical_social_helper_export",
                "counts": {"comments": len(original_work["comments"]), "roots": original_work["main_comments"], "replies": original_work["subcomments"]},
                "limitations": COMMON_LIMITATIONS + ["帖子型号仅表明原作者文字/标签关联，不证明拍摄设备、具体功能演示或任一评论者的持有型号", "每帖约20条含回复，可能集中于少数根线程，不能代表平台或使用人群"],
                "post_fields": fields, "original_metadata": original_metadata,
            }
            works.append(work)
            for ci, comment in enumerate(original_work["comments"]):
                n = comment["normalized"]
                record_id = f"legacy:{platform}:{n['comment_id']}"
                namespace = f"legacy:{platform}:"
                available_text = n["text"] or ""
                mentions = models_in(available_text, allow_short=bool(declarations) or "pocket" in available_text.lower())
                if len(mentions) == 1:
                    comment_model, comment_basis = mentions[0], "comment_explicit_model_or_contextual_shorthand"
                elif len(mentions) > 1:
                    comment_model, comment_basis = "unknown", "multiple_comment_models"
                else:
                    comment_model, comment_basis = model, "post_context:" + basis if model != "unknown" else "not_established"
                limitations = list(COMMON_LIMITATIONS)
                if n["text"] is None:
                    limitations.append("原导出文字为空，保留图片链接但未读取图片；不能据本记录提炼文字或图像内容")
                if comment_basis.startswith("post_context:"):
                    limitations.append("model_id来自帖子上下文，不代表评论者拥有、使用或正在指称该型号")
                elif mentions:
                    limitations.append("型号是评论原文提及或有Pocket语境的简称，不认证型号能力或购买/使用经历")
                if n["thread_role"] == "reply" and not n.get("direct_parent_comment_id"):
                    limitations.append("缺少直接父句；只保留根线程，不按相邻行、@文字或语义推造回复关系")
                record = {
                    "id": record_id, "comment_id": n["comment_id"], "work_id": work_id,
                    "legacy_work_id": original_work["id"], "platform": platform,
                    "model_id": comment_model, "model_basis": comment_basis,
                    "work_model_id": model, "mentioned_model_ids": mentions,
                    "text": n["text"], "text_status": "absent_in_export" if n["text"] is None else "available",
                    "parent_id": namespace + n["direct_parent_comment_id"] if n.get("direct_parent_comment_id") else None,
                    "root_id": namespace + n["root_comment_id"] if n.get("root_comment_id") else None,
                    "thread_role": n["thread_role"], "parent_basis": n["direct_parent_basis"],
                    "source_path": source_relative,
                    "source_locator": {"json_pointer": f"/{wi}/comments/{ci}", "original_file": comment["source_file"], "sheet": comment["source_sheet"], "row": comment["source_row"]},
                    "source_sha256": digest(source_path),
                    "collected_at": n["captured_at"], "created_at": n.get("comment_created_at"),
                    "read_scope": READ_SCOPE, "timestamp_timezone": "not_recorded_in_export",
                    "split": "legacy", "source_kind": "historical_social_helper_export",
                    "limitations": limitations, "original_normalized": n,
                }
                records.append(record)
                refs[original_work["id"] + ":r" + str(comment["source_row"])] = record
    assert len(works) == 18 and len(records) == 372
    assert Counter(r["thread_role"] for r in records) == {"root": 75, "reply": 297}
    assert len({r["id"] for r in records}) == 372
    byid = {r["id"]: r for r in records}
    for r in records:
        if r["parent_id"]:
            assert r["parent_id"] in byid and byid[r["parent_id"]]["work_id"] == r["work_id"]
        if r["root_id"]:
            assert r["root_id"] in byid and byid[r["root_id"]]["work_id"] == r["work_id"]
    dump_jsonl(OUT / "voice/works.jsonl", works)
    records_path = OUT / "voice/records.jsonl"
    non_legacy = []
    if records_path.exists():
        non_legacy = [json.loads(line) for line in records_path.read_text().splitlines() if line.strip()]
        non_legacy = [record for record in non_legacy if record.get("split") != "legacy"]
    dump_jsonl(records_path, records + non_legacy)
    return works, records, refs


def make_cards(refs):
    cards = []

    def card(number, title, situation, need, level, stance, purpose, mechanism, evidence, transferable, prohibited, tags):
        evidence_refs = [refs[x]["id"] for x in evidence.split()]
        work_ids = sorted({refs[x]["work_id"] for x in evidence.split()})
        cards.append({
            "id": f"voice_{number:03d}", "title": title, "situation": situation, "need": need,
            "experience_level": level, "stance": stance, "expression_purpose": purpose,
            "mechanism": mechanism, "evidence_refs": evidence_refs, "work_ids": work_ids,
            "status": "pattern" if len(work_ids) >= 3 else "case",
            "transferable": transferable, "not_transferable": prohibited, "tags": tags,
            "source_kind": "editorial_synthesis_of_legacy_visible_comments", "split": "legacy",
            "evidence_locators": evidence.split(),
            "limitations": ["本卡是有来源的编辑归纳，不是用户人口画像、平台规律或效果承诺", "pattern只表示至少3个独立作品有例证，不表示统计代表性"],
        })

    card(1, "用一个动作说出愿望与现实的落差", "已经有表达愿望，但某个实际环节让它没有发生", "把卡点说具体，不补一段人生感悟", "各来源不同；DY01自述不会用，BL01未确认熟练度", "无奈、轻微自嘲或困惑", "表达实际阻碍", "往返、忘拍、找不回设置、勉强消耗这些动作本身承担情绪；不替来源补原因", "DY01:r2 BL01:r15 XHS02:r38 BL06:r127", ["从有材料的一次动作或眼下困难开口", "省掉重复解释落差的总结"], ["网友的购买、出行、设置和家务经历", "把不会用归咎于已核实的产品缺陷", "给不同角色分配同一段亲历"], ["行为落差", "使用意愿", "具体困难", "轻微自嘲"])
    card(2, "下一句追问刚出现的缺口", "父句给出部分信息，但留下一个更小的新问题", "把一件事问清楚", "未知；不能因提问自动定义为新手", "好奇或求助", "追问新信息", "回应刚出现的工具、模式或行程范围；父句已回答的部分不重新设问", "XHS04:r75 XHS04:r76 XHS04:r77 BL01:r2 BL01:r4 BL01:r5 XHS02:r22 XHS02:r23 XHS02:r28", ["定位直接父句中刚出现的词或限制", "每轮只处理当前最具体的问题"], ["按相邻行把BL01:r4误接到r3；它明确回复r2", "模拟来源博主的答复", "把网友模式与剪辑说法当产品教程"], ["楼中楼", "追问", "父句", "信息缺口"])
    card(3, "回答够用就停", "一个小问题、愿望或玩笑已得到对应回应", "完成当前一轮，不为数量延长", "未知", "直接、附和或轻松", "短答完成交流", "回答范围与父句问题一样小，得到足够信息后无需再解释意义", "DY03:r45 DY03:r46 BL03:r57 BL03:r58 XHS05:r91 XHS05:r92 BL05:r92 BL05:r93", ["允许一条回复或不再延长", "让短句有清晰的父句对象"], ["固定复制存着、附议或术语答案", "将采集到的结尾声称为真实线程永久结束", "把剪辑术语当已验证教学"], ["楼中楼", "短答", "及时结束", "不凑数量"])
    card(4, "用语气转弯接住当下感受", "对方解释、感叹或流露遗憾后", "给出一个有回应的反应", "未知", "轻微自嘲、关照或释然", "情绪回应", "回应保持话题连续，语气轻轻转换，而不是继续讲道理或强行加购买意图", "DY02:r23 DY02:r24 DY06:r107 DY06:r108 XHS05:r99 XHS05:r100", ["回应前一句当下的情绪", "有语境才使用轻微反转"], ["把学废了等词变成批量口头禅", "继承博主身份或长期生活经历", "给来源评论里的感受补造成片声音证据"], ["情绪", "语气转弯", "轻反应", "楼中楼"])
    card(5, "让上下文承担已经说过的词", "作品或直接父句已经给出对象", "减少重复而保持指代清楚", "未知", "直接或接梗", "省略与补充", "只补范围、差别或刚改变的部分；同一人自补与他人答复分别记录", "XHS04:r73 XHS04:r74 XHS06:r109 XHS06:r110 BL04:r65 BL04:r66", ["删去上下文已明确的对象", "保留理解必需的指代"], ["把XHS04同一人的自补写成他人回应", "把XHS06的一代二代归为Pocket代际", "借用来源的圈内熟人关系"], ["省略", "上下文", "直接父句", "指代"])
    card(6, "同一作品里的开口理由可以不同", "同一内容触发不同关注点", "选择彼此独立的具体兴趣", "各句未知，不人为分配人设", "好奇、喜欢、感慨或具体需求", "表达目的多样", "关注实际用途、制作方式、观看感受或一个细节；差异来自想说的事，不是换产品称呼", "BL03:r46 BL03:r57 XHS05:r83 XHS05:r89 XHS05:r97 XHS05:r99 BL06:r119 BL06:r125 BL06:r127", ["先并排比较每条为什么开口", "按本帖材料支持度决定条数"], ["强制每帖覆盖本卡所有目的", "无证据复述声音、画面或家庭情况", "把无关细节夸赞自动认定为Pocket种草"], ["多样性", "开口理由", "同帖差异", "兴趣"])
    card(7, "接住建议也可以保留自己的取舍", "有人提出替代方案或解决办法", "说清自己此刻更在意什么", "来源不同，未独立核验实际经验", "有保留或温和分歧", "回应后转换取舍", "仍谈父句的问题，但补出自己的限制；不必每次接受建议，也不升级为争吵", "BL06:r119 BL06:r120 BL06:r121 BL02:r23 BL02:r24 BL02:r25", ["在有据的需求上表达偏好", "保留温和的观点差别"], ["移用储物空间、手机稳定器使用经历", "把网友画质比较变成事实", "为像评论区而制造较真或攻击"], ["取舍", "温和分歧", "替代方案", "楼中楼"])
    card(8, "拍了素材却卡在后期流程", "来源评论明确求助剪辑、色彩还原和使用设备", "知道下一步该怎么处理素材", "来源评论者自称新手；未独立核验", "想学又被不同说法弄糊涂", "明确操作卡点", "把宽泛的不会用缩小为具体软件、色彩处理或终端问题；回复先处理其中一个", "BL01:r2 BL01:r3 BL01:r4 BL01:r5", ["从原帖和真实材料确认具体卡点", "分开拍摄、调色和导出问题"], ["给新角色赋予刚买相机或拥有iPad的经历", "把网友的软件兼容说法当现行事实", "模拟博主承诺再做一期教程"], ["后期", "剪辑", "色彩", "上手", "求助"])
    card(9, "把替代设备讨论落回自己的需求", "有人把Pocket与手机及稳定器比较", "明确比较的是便携、准备步骤还是别的需求", "来源自述有使用经验，未认证", "对替代方案有不同偏好", "解释选择标准", "承认方案可能成立，再说明自己关心的具体使用环节；不以未经核实的参数胜负收尾", "BL02:r23 BL02:r24 BL02:r25 BL03:r46", ["先问或确认实际拍摄任务", "按官方核实能力再回答适用性"], ["照搬手机消息干扰或使用不便的亲历", "继承评论价格、画质和生态断言", "把所有人都说成需要同一个产品"], ["手机对比", "选择标准", "便携", "需求"])
    card(10, "需要腾出手时先问能否这样拍", "来源评论想在爬山时减少手持负担", "了解可行的固定或携带方式", "未知", "具体好奇", "用途可行性提问", "用一个真实活动和操作限制提出问题；疑问本身不证明方案安全、可行或官方支持", "BL03:r46", ["保留问题形式", "以当前官方配件和使用边界回答"], ["把帽子、肩带挂载写成官方推荐", "把愿望写成已经成功的使用经历", "类推到剧烈运动或极端环境"], ["爬山", "固定机位", "腾出手", "配件", "可行性"])
    card(11, "找不到操作方式时问具体一步", "来源评论谈云台指向和模式切换的困惑", "找到可理解的下一步操作", "部分来源自述刚上手，其他未知", "困惑或求助", "描述控制困难", "先明确哪里不符合预期、在问哪种模式；不把上手困难直接写成型号故障", "XHS02:r22 XHS02:r23 XHS02:r28 XHS02:r38", ["保留原话的具体困难", "写作时让官方说明和来源体验各自归位"], ["复制网友的模式能力断言", "继承刚拿到手的个人经历", "将未知代际自动标为Pocket3或最新一代"], ["云台", "操作", "模式", "上手", "具体问题"])
    card(12, "从喜欢成片走到具体制作问题", "看到作品后对拍法或处理步骤产生兴趣", "了解一个能尝试的制作环节", "各来源不同；只按明确自述识别", "好奇或求助", "制作兴趣", "从泛泛的好看转成关于片头、调色、剪辑终端或录制节奏的具体问题", "XHS05:r91 BL03:r57 BL01:r2 XHS06:r113 XHS06:r114", ["选择原帖没有回答的具体环节", "把需要产品核验的功能与一般制作问题分开"], ["重问原文已经给出的答案", "据评论问题反推自己看过原片", "把编辑或剪辑效果写成相机一键能力"], ["拍摄流程", "成片兴趣", "调色", "片头", "剪辑"])
    dump_jsonl(OUT / "voice/cards.jsonl", cards)
    return cards


def make_scenarios(works):
    by_legacy = {w["id"]: w for w in works}
    scenarios = []

    def scenario(number, title, scene, need, workflow, voice, basis, source_works, limits, tags):
        scenarios.append({
            "id": f"scenario_{number:03d}", "title": title, "scene": scene, "need": need,
            "workflow": workflow, "product_fact_ids": [], "voice_card_ids": [f"voice_{x:03d}" for x in voice],
            "basis": basis, "evidence_work_ids": [by_legacy[x]["work_id"] for x in source_works],
            "target_models": ["pocket_4", "pocket_4p"],
            "source_post_locators": [{"work_id": by_legacy[x]["work_id"], "source_path": by_legacy[x]["source_path"], "json_pointer": by_legacy[x]["source_locator"]["json_pointer"] + "/post_fields"} for x in source_works],
            "limitations": limits + ["workflow是供写手组织需求的步骤；未作为实操教程核验", "target_models是本库写作服务目标，不证明历史来源使用这些型号，也不概括Pocket4/4P使用人群", "产品连接尚待核验与登记；空product_fact_ids不代表任何代际自动适用"],
            "tags": tags, "source_kind": "editorial_synthesis" if basis == "evidence" else "editorial_planning",
            "split": "legacy" if basis == "evidence" else "editorial", "product_link_status": "pending_official_fact_mapping",
        })

    scenario(1, "独自旅行又想留下自己", "独自旅行自拍与机位选择", "把自己拍进旅行，同时尽量少打断游玩", ["确认想记录的活动与是否需要本人入镜", "区分手持、固定机位和自拍的需要", "核对代际、配件与相关功能再讨论具体拍法", "把拍摄与继续游玩的取舍说具体"], [1, 10, 12], "evidence", ["BL01", "BL03"], ["独自旅行主题来自作者导出正文；未核验视频中的实际布机位方式", "不把一个人的自拍愿望说成原片确由独自跟随完成"], ["旅行", "独自拍摄", "机位", "拍摄与游玩"])
    scenario(2, "设备有了，却总是拿出又收回", "随身记录与频繁收纳", "减少开始拍摄的心理或操作负担", ["分清不会操作、不想显眼与担心收纳的不同困难", "核实当前帖子具体触发哪一个困难", "选择一个有据的愿望或问题", "产品操作建议另查对应型号官方说明"], [1, 11], "evidence", ["DY01", "XHS02"], ["已有设备、闲置、担心云台等均是来源自述，不分配给新角色", "不将两帖体验归纳为所有用户或所有代际的产品缺陷"], ["日常记录", "携带", "收纳", "上手"])
    scenario(3, "素材拍好了，下一步怎么剪", "剪辑终端、色彩处理与导出", "找到能开始的一段后期流程", ["确认素材模式与希望使用的终端", "区分剪辑、还原色彩和导出问题", "核验软件、格式和代际兼容性", "只回答本轮最具体的问题"], [2, 8, 12], "evidence", ["BL01"], ["单一作品案例；不能据此概括所有新手", "评论里的4K、10bit、软件兼容与iPad经历尚不是官方事实"], ["素材", "后期", "剪辑", "色彩", "导出"])
    scenario(4, "手机和Pocket，先想清要拍什么", "拍摄设备选择与替代方案", "按实际用途确定在意的环节", ["明确当前使用任务", "确认便携、准备步骤、画面或收音中最在意的一项", "按具体代际与官方条件核对", "给有条件的选择理由"], [7, 9], "evidence", ["BL02", "BL03"], ["来源含争论；仅保留需求表达，不继承攻击、价格或性能优劣断言", "缺少覆盖不同代际和相同条件的比较证据"], ["购前", "手机对比", "选择", "使用取舍"])
    scenario(5, "喜欢一个片段，想问它怎么完成", "成片引发的制作兴趣", "找到一个原帖未说明的可尝试环节", ["确认已实际看到或读到的作品内容", "先排除原帖已经回答的问题", "区分拍摄、后期与配件的作用", "追问父句刚带来的新信息"], [2, 6, 12], "evidence", ["XHS05", "XHS06", "BL03"], ["本批没有完整观看原片；只能先登记评论者曾提出的问题", "通用制作问题不自动等于Pocket功能"], ["制作兴趣", "成片", "追问", "内容锚点"])
    scenario(6, "想腾出手，先确认固定方式", "爬山时的拍摄与携带", "了解减少手持是否可行", ["明确活动强度与要腾出手的原因", "区分收纳、固定拍摄和运动拍摄", "查官方支持的配件、安装方式与边界", "把未核实方案保留为问题"], [10], "evidence", ["BL03"], ["只有一条明确需求例证", "不能由帽子或肩带提问推出其安全性、稳定效果或官方支持"], ["爬山", "配件", "固定", "使用边界"])
    scenario(7, "记录孩子或宠物的日常", "亲子或宠物的移动主体", "想留住短暂反应与互动", ["补采明确作品语境与真实需求", "识别距离、移动方式与拍摄者是否也入镜", "按对应型号核查跟随、对焦、收音和使用边界", "有证据后再归纳表达卡"], [2, 6], "editorial_hypothesis", [], ["这是待采样场景，18帖历史语料没有形成该场景的可靠成组证据", "不预设评论者是家长、养宠者，也不承诺跟随结果"], ["待补证", "亲子", "宠物", "移动主体"])
    scenario(8, "晚上或室内记录生活", "室内、低照度与人像记录", "看清人物并保留当时氛围", ["补采具体光线、动作与已读媒体范围", "区分曝光、画面效果、补光和后期因素", "核实对应型号及模式的条件", "只把得到支持的条件写进表达"], [6, 12], "editorial_hypothesis", [], ["本卡不是从夜景成片实测得到的结论", "不将明亮样片或网友夸赞变成所有光线下的性能承诺"], ["待补证", "室内", "夜间", "低光", "人像"])
    scenario(9, "Pocket4和Pocket4P，按需求比较", "主款之间的用途选择", "明确哪项差异与自己的拍摄任务有关", ["确认要拍摄的主体、场景与实际限制", "分别检索Pocket4和Pocket4P的官方事实及条件", "只讨论会改变本次选择的差异", "用新采样验证对应使用者怎样表达顾虑与偏好"], [7, 9], "editorial_hypothesis", [], ["历史样本未形成Pocket4/4P比较使用者的代表性语料", "不能把来源对其他代际或未来型号的期待作为主款实际表现", "不预设评论者持有任一型号或有换机经历"], ["待补证", "Pocket4", "Pocket4P", "型号选择", "使用需求"])
    scenario(10, "拍下来了，也想把声音听清楚", "说话、环境声与拍摄现场", "确认需要保留谁的声音及哪些环境声", ["补采带有可听证据或完整转写的作品", "分清人物说话、环境声和后期配乐", "核实内录、外接设备与型号兼容", "具体回应声音需求"], [2, 12], "editorial_hypothesis", [], ["历史研究未听音轨；评论提到声音不证明当前已听过或核验收音", "不推断素材使用了某款麦克风"], ["待补证", "收音", "环境声", "口播"])
    dump_jsonl(OUT / "scenarios/cards.jsonl", scenarios)
    return scenarios


def make_feedback():
    context = ".agents/skills/write-pocket-seeding-comments/references/project-context.md"
    quote = "我自己本身就有pocket，也有使用过的，所以你也可以轻微写用过的感受的"
    assert quote in (ROOT / context).read_text()
    records = [{
        "id": "feedback_legacy_personal_owner_20260905", "date": "2026-09-05",
        "source_kind": "explicit_user_statement_preserved_in_project_reference",
        "source_path": context, "source_locator": {"heading": "本项目已确认的本人素材", "quote_line": 7},
        "source_sha256": digest(ROOT / context), "quote": quote,
        "subject": "current_project_user", "type": "personal_material_and_limited_writing_authorization",
        "confirmed": ["当前项目用户拥有并使用过Pocket产品线设备"],
        "unknown": ["具体代际", "套装及颜色", "购入时间", "使用频率", "拍摄习惯", "具体使用场景", "满意点与问题"],
        "application": ["仅用于当前用户本人备选稿", "具体使用感受需要对应的真实材料"],
        "not_authorized": ["给其他角色分配设备持有或使用经历", "由拥有设备推导具体旅行、长期体验或产品实测结论"],
        "evidence_status": "user_quote_preserved_in_project_document; original_chat_not_reopened",
        "split": "legacy", "acceptance_verdict": None,
    }]
    dump_jsonl(OUT / "feedback/records.jsonl", records)
    sources = [
        {"id": "feedback_source_user_material", "source_path": context, "source_kind": "preserved_user_statement", "use": "确认本人素材及其范围", "is_platform_comment_corpus": False, "is_user_acceptance_of_generated_drafts": False},
        {"id": "feedback_source_project_skill", "source_path": ".agents/skills/write-pocket-seeding-comments/MODULE.md", "source_kind": "project_writing_rule", "use": "继续作为op项目写作与验收规则入口", "is_platform_comment_corpus": False, "is_user_acceptance_of_generated_drafts": False},
        {"id": "feedback_source_writing_examples", "source_path": ".agents/skills/write-pocket-seeding-comments/references/writing-and-examples.md", "source_kind": "editorial_rules_and_authored_examples", "use": "学习项目要求及例句成立的理由，不视作真实消费者互动", "is_platform_comment_corpus": False, "is_user_acceptance_of_generated_drafts": False},
        {"id": "feedback_source_accepted_draft", "source_path": ".agents/skills/write-pocket-seeding-comments/assets/accepted-comments.md", "source_kind": "authored_draft_with_historical_agent_review", "use": "历史写作基线；不能推导新稿通过或新增用户认可", "is_platform_comment_corpus": False, "is_user_acceptance_of_generated_drafts": False},
        {"id": "feedback_source_acceptance_record", "source_path": "outputs/pocket-project-acceptance/验收记录.md", "source_kind": "historical_agent_acceptance_record", "use": "保留历史检查范围；不继承到本轮知识库或新写稿", "is_platform_comment_corpus": False, "is_user_acceptance_of_generated_drafts": False},
    ]
    for source in sources:
        assert (ROOT / source["source_path"]).exists()
        source["source_sha256"] = digest(ROOT / source["source_path"])
    dump_jsonl(OUT / "feedback/source-register.jsonl", sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild-editorial", action="store_true", help="显式重建表达卡、场景卡和历史反馈；会覆盖这些文件中的后续编辑")
    args = parser.parse_args()
    works, records, refs = migrate()
    cards_path = OUT / "voice/cards.jsonl"
    scenarios_path = OUT / "scenarios/cards.jsonl"
    cards = make_cards(refs) if args.rebuild_editorial or not cards_path.exists() else [json.loads(x) for x in cards_path.read_text().splitlines() if x.strip()]
    scenarios = make_scenarios(works) if args.rebuild_editorial or not scenarios_path.exists() else [json.loads(x) for x in scenarios_path.read_text().splitlines() if x.strip()]
    if args.rebuild_editorial or not (OUT / "feedback/records.jsonl").exists():
        make_feedback()
    stats = {
        "split": "legacy", "works": len(works), "comments": len(records),
        "roots": sum(r["thread_role"] == "root" for r in records),
        "replies": sum(r["thread_role"] == "reply" for r in records),
        "text_records": sum(r["text"] is not None for r in records),
        "records_without_text": sum(r["text"] is None for r in records),
        "known_direct_parents": sum(bool(r["parent_id"]) for r in records),
        "replies_without_direct_parent": sum(r["thread_role"] == "reply" and r["parent_id"] is None for r in records),
        "new_work_count_contribution": 0, "new_holdout_count_contribution": 0,
        "works_by_platform": dict(Counter(w["platform"] for w in works)),
        "comments_by_platform": dict(Counter(r["platform"] for r in records)),
        "works_by_model": dict(Counter(w["model_id"] for w in works)),
        "voice_cards": sum(c.get("split") == "legacy" for c in cards), "voice_card_statuses": dict(Counter(c["status"] for c in cards if c.get("split") == "legacy")),
        "scenario_cards": len(scenarios), "scenario_bases": dict(Counter(s["basis"] for s in scenarios)),
        "explicit_user_feedback_records": 1,
    }
    (OUT / "voice/legacy-migration-report.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
