---
name: use-mobile-knowledge
description: 仅由总控S2派单或显式知识查询读取Osmo Mobile / DJI OM事实、场景与表达资料；返回来源和缺口，不启动采集、写作或质检。
---


# S2 Osmo Mobile / DJI OM知识

输入具体问题、品线/型号、S1材料范围与本轮已有事实包。只查相关资料，完成后返回总控；用户只问知识时返回分析即可。product_line=`osmo_mobile`。

- **产品问答、兼容、型号比较**：从[知识库索引](knowledge/INDEX.md)取相关事实与兼容记录，再查相关缺口。无需先加载写手。
- **卖点、产品优势和用户价值**：从[卖点指南](knowledge/selling_points/guide.md)按准确型号取相关卡，结合拍摄任务和角色解释用途；能力来自已核事实，用户价值保持编辑推演。卡片通过事实编号链接完整条件，不把卖点标题当作无条件能力，也不把分析顺序写成固定评论句式。
- **使用场景发散、卖点如何使用及培训选材**：查[详细场景库](knowledge/use_cases/guide.md)或[按卖点反查场景](knowledge/use_cases/selling-point-map.md)，取发生时刻、拍摄难点、人物取舍和相关表达方向。需要交给写手时按[选材接入说明](knowledge/use_cases/WRITER_HANDOFF.md)保留资料性质；这些字段不是成稿步骤，虚构细节只进当批人物状态。
- **手机拍法发生什么变化、真实使用感受及接话学习**：读[拍法与表达材料](knowledge/experience_materials/guide.md)，区分同手机的过程与成片、实际手机／App／配件组合、公开自述、完整讨论范围和用户反馈。先查材料状态与缺口；编辑指南、旧款讨论、部分父句或待采集链接不补成当前型号完整实拍。材料可以完整，具体评论只取当前最值得说的兴趣，不拼接整段使用流程。
- **使用人群、动机和心理表达分析**：先读[角色心理指南](knowledge/audiences/guide.md)的方法与角色概览，再按角色ID／关键词取当前相关卡片和依据，不要求每次全读；需要产品能力解释时再关联事实。一般分析不必要求用户先选型号，涉及具体能力时再细分型号与组合。
- **真实评论资料**：用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](../read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。
- **主评论、回复、改写、培训案例或批量风格校准**：检索少量相关产品事实、必要卖点及角色线索，随后进入[共享消费者写手](../write-consumer-comments/MODULE.md)。若当前项目已有写手入口且已经读过，继续同一共享流程，不回调项目入口或 Mobile 写作入口。`product_line=osmo_mobile`，新稿保持 `content_mode=training_fiction`。
- **明确的真实资料核验或旧稿审查**：使用[Mobile 原有审查入口](../write-dji-osmo-mobile-comments/MODULE.md)对应分支，仍以本库及当前官方依据核对产品。旧稿不改标训练稿；审查不授权发布。

- [事实索引](knowledge/INDEX.md)
- [卖点](knowledge/selling_points/guide.md)
- [场景](knowledge/use_cases/guide.md)
- [体验材料](knowledge/experience_materials/guide.md)
- [角色心理](knowledge/audiences/guide.md)

可选本地查询脚本：`knowledge/scripts/query.py`，先查脚本用法，路径以本技能目录为基准。无Python时直接阅读索引与命中记录。完整知识、场景、来源和原话仍在包内，不要一次全读。

## 型号与证据

从本次发现的 `MODULE.md` 所在目录定位 `knowledge/`，不要从当前工作目录猜 op 路径。可用 `rg` 查完整 JSONL；具体命令见[索引](knowledge/INDEX.md#本地检索)。[事实检索脚本](knowledge/scripts/query.py)支持精确型号、事实编号与关键词，并同时返回相关型号缺口；[场景检索脚本](knowledge/scripts/use_cases.py)的query子命令支持场景编号、型号、关键词和卖点编号，展开完整依据与缺口。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

返回少量相关事实、可选兴趣点、命中来源与未解决事项。资料内涉及其他技能的旧指引仅作历史上下文；本阶段不执行跨技能路由。若需要新原帖材料，返回missing_evidence给总控，不自行重开S1；需要成稿则返回facts_ready，不自行调用写手。
