#!/usr/bin/env python3
"""Build readable scenario guides from the maintained JSONL cards."""
import json
from pathlib import Path
import mic_writing_scenarios as scenes


def build_selling_point_map(directory, rows, selling_data):
    links = {}
    for family, filename in zip(scenes.FAMILIES, scenes.FILES):
        markdown = Path(filename).with_suffix(".md").name
        for row in rows:
            if row["family"] != family:
                continue
            for route in row["routes"]:
                for point_id in route["selling_point_ids"]:
                    links.setdefault(point_id, []).append(
                        f"[{row['id']} · {row['title']}]({markdown}#{row['id'].lower()})")
    lines = ["# 从 Mic 卖点反查详细场景", "", scenes.LABEL, "",
             "从一个感兴趣的卖点找不同任务。这里的关联来自场景候选路线，不能证明原帖展示了该功能或使用者有这种心理。",
             "阅读单卡可看适用条件；命令检索会展开准确型号的事实、限制、来源及原核验日期。更深入的用途解读见[需求与价值发散](../selling_points/value-expansion.md)。", "",
             "```bash",
             "python3 knowledge/mic/scripts/mic_writing_scenarios.py --selling-point MIC3-SP003 --limit 20",
             "python3 knowledge/mic/scripts/mic_writing_scenarios.py '回听' --selling-point M2S-SP002 --model mic_mini_2s --format json",
             "```", "",
             "个人入口对应 `mic.py scenes --selling-point 编号`。卖点、问题、型号与类别同时给出时取交集；交集为空就返回空结果，不借另一型号的场景。未列场景仅表示编辑关联缺口，不表示功能不支持。", ""]
    for model, name in scenes.MODEL_NAMES.items():
        lines += ["## " + name, ""]
        for point in selling_data["cards"]:
            if model not in point["models"]:
                continue
            lines += [f"### {point['id']} · {point['title']}", "",
                      "\n".join("- " + link for link in links.get(point["id"], [])) or "暂无关联详细卡，可先查看底层卖点条件。", ""]
    (directory / "selling-point-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    root = scenes.ROOT
    rows, errors = scenes.load(root)
    data, _ = scenes.product.load(root)
    selling_data, _ = scenes.selling.load(root)
    audiences = scenes.product.index([json.loads(line) for line in (root / "audience/cards.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()])
    report = scenes.audit(rows, errors, selling_data, data, audiences)
    if not report["ok"] or report["unavailable_routes"]:
        raise SystemExit(json.dumps(report, ensure_ascii=False, indent=2))
    directory = root / "writing_scenarios"
    intro = ["# Mic 详细使用场景与培训选材", "", scenes.LABEL, "",
             f"本版 {report['cards']} 张详细场景卡、{report['routes']} 条分型号候选路线，涵盖创作与学习、交流与生活记录、商业与团队协作。关联现有卖点、事实与角色资料；具体假想人物及经历在后续写作任务中建立。", "",
             "## 先从发生的事情进入", "",
             "查场景时可以直接说动作和时刻，例如手上拿着工具还要讲解、异地搭档分别录声音、节目临时增加嘉宾、收工后把录音交给不同剪辑人员。先理解当前任务，再选择有依据的卖点和关注点。", "",
             "每卡按需查阅：具体时刻、用户任务、可能心理与取舍、原帖可触发线索、分型号方案及限制、可取表达角度、不适用情形和可继续扩展的变化轴。这是资料结构，不是评论句式；不用把每个字段写进一条评论。", "",
             "已知卖点时使用[卖点反查场景](selling-point-map.md)；想深入理解相同能力为什么吸引不同使用者，按需查看[需求与价值发散](../selling_points/value-expansion.md)。这些资料只提供取材选择，具体评论只取当前最值得说的一点。", "",
             "## 场景目录", "", "| 场景 | 要完成的任务 | 可考虑的型号 |", "|---|---|---|"]
    for family, filename in zip(scenes.FAMILIES, scenes.FILES):
        group = [row for row in rows if row["family"] == family]
        markdown = Path(filename).with_suffix(".md").name
        detail = ["# " + family, "", scenes.LABEL, "", "从[总指南](guide.md)选择任务；完整底层依据可通过 `scenes` 命令展开。", ""]
        for row in group:
            models = "、".join(scenes.MODEL_NAMES[route["model"]] for route in row["routes"])
            intro.append(f"| [{row['id']} · {row['title']}]({markdown}#{row['id'].lower()}) | {row['user_task'].replace('|', '／')} | {models} |")
            body = scenes.render_card(row, include_evidence=False)
            first, rest = body.split("\n", 1)
            detail += [f"## {row['id']}", "", f"**{row['title']}**", rest, ""]
            for route in row["routes"]:
                selected = scenes.search([row], selling_data, data, audiences, model=route["model"], limit=1)["results"][0]["routes"][0]
                references = "; ".join(f["id"] for f in selected["evidence"])
                dates = ", ".join(sorted({r["checked_at"] for r in selected["reviews"]}))
                detail += [f"{scenes.MODEL_NAMES[route['model']]} 依据：{references}；卖点复核：{dates}。", ""]
                for source in selected["sources"]:
                    detail += [f"- [{source['id']}]({source['url']}) · {source['locator']} · 原来源核验 {source['checked_at']}"]
                detail.append("")
        (directory / markdown).write_text("\n".join(detail) + "\n", encoding="utf-8")
    intro += ["", "## 同一个卖点怎样继续发散", "",
              "| 可以改变的变量 | 具体变化 | 可能改变的关注点 |", "|---|---|---|",
              "| 时间阶段 | 第一次试录、形成固定习惯、临时增加任务、准备交接 | 学会开始、保留节奏、重新配接、让接手者看懂 |",
              "| 谁操作设备 | 自己边拍边讲、朋友协助、轮换主持、拍摄与剪辑分工 | 能否兼顾动作、需要多少配合、现场谁确认、文件怎样交 |",
              "| 素材去向 | 当场直播、之后剪视频、只留声音、交给两种后期 | 实际输入、可编辑文件、声音的个人意义、处理版取舍 |",
              "| 人数与空间 | 一人示范、两人对话、四人讨论、异地各自录制 | 手是否空闲、谁的声道、接口限制、后期如何对齐 |",
              "| 设备与已有习惯 | 现有手机、兼容 DJI 机身、已有两支旧麦、共用一套设备 | 新增配件、直连取舍、明确复用方向、清点与设置交接 |",
              "| 此刻感兴趣的东西 | 操作细节、穿搭、声音偏好、某个片段、好奇一个功能 | 不必统一写成害怕返工、终于安心或准备购买 |", "",
              "这些变量用来改变任务或人物关注点，不是批量替换地名、亲友称谓与产品名。变化后仍要检查当前原帖能否接住该联想。", "",
              "## 后续培训文案怎样取用", "",
              "原帖不必直接展示麦克风功能，生活动作、合作方式或对声音的关注也可以引出使用联想；不能声称看到了实际未出现的设备、操作或音轨。", "",
              "1. 有原帖时先确认其实际文字、画面和必要音轨，按统一社媒读取流程获取材料；没有原帖时明确设合成训练命题。`post_cues` 只提示可能值得观察的线索，不能当作采集证据。",
              "2. 按当前问题查少量场景，选择自己有话可说的关注点；不把角色职业等同心理，也不必把所有条件塞进正文。",
              "3. 确定型号和连接路线，核对当前产品依据。知识库只提供能力条件；假想使用感受不能证明未知兼容、真实原片听感或客观性能。",
              "4. 需要主评、回复或案例时交共享写手当前规则完成。人物与假想经历放进具体任务的 personas；对外培训标识、数量、格式、来源与检查都由共享层处理。",
              "5. 检查同帖和跨帖是否只是反复同一个动机或购买结尾。保留成立的表达，不为展示场景库而强行讲全参数、补问题或安排回复收尾。", "",
              "这里没有新建一套文风，也没有把任何示例当作已获用户认可的范文。当前只提供选材资料，未生成实际评论批次。", "",
              "## 检索示例", "", "在项目根目录运行：", "", "```bash",
              "python3 knowledge/mic/scripts/mic_writing_scenarios.py '手上拿着工具还要讲解' --model mic_mini_2s --limit 2",
              "python3 knowledge/mic/scripts/mic_writing_scenarios.py '异地播客各自保存声音' --format json",
              "python3 knowledge/mic/scripts/mic_writing_scenarios.py --family '商业与团队协作' --model mic_3", "```", "",
              "个人技能入口为 `scripts/mic.py scenes`。支持中文问题或场景 ID、`--model`、`--family`、`--selling-point`、`--limit` 和 Markdown／JSON。结果只保留所选型号与卖点交集的路线，展开关联卖点、事实、条件、来源及核验日期；底层依据失效的路线单列待核。", "",
              "本层依赖[卖点指南](../selling_points/guide.md)与[角色心理](../audience/guide.md)；需要设备操作问答时仍使用[原技术场景](../scenarios/guide.md)。结构定义见 [SCHEMA](../SCHEMA.md)。事实和卖点日期沿用实际核验记录，场景推演没有伪装为新一轮官方或消费者核验。"]
    (directory / "guide.md").write_text("\n".join(intro) + "\n", encoding="utf-8")
    build_selling_point_map(directory, rows, selling_data)
    print(json.dumps({"ok": True, "cards": report["cards"], "routes": report["routes"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
