---
name: use-osmo360-knowledge
description: 仅由总控S2派单或显式知识查询读取Osmo 360事实、场景与表达资料；返回来源和缺口，不启动采集、写作或质检。
---


# S2 Osmo 360知识

输入具体问题、品线/型号、S1材料范围与本轮已有事实包。只查相关资料，完成后返回总控；用户只问知识时返回分析即可。product_line=`osmo360`。

- **功能问答、两代差异、拍摄后期、竞品比较或培训**：先读[知识库索引](knowledge/INDEX.md)，再查相关型号、模块和事实卡。无需通读全部资料。
- **产品卖点、用户价值、这个角色适合讲什么或是否值得升级**：读[卖点与用户价值](knowledge/selling-points.md)，按五组主题、具体型号或角色任务找条目，再打开所引事实卡及相关心理假设。先说明能帮助完成什么、为什么可能有价值，再保留成立条件与价值不成立的情况。品类原理、本机能力、已证实差异分别表达；某代未确认不等于不支持。
- **使用场景更详细、发散卖点或为后续培训文案选材**：查[48张详细场景卡](knowledge/scenario-bank.md)，按具体事件选择SC，再由[任务变化与选材矩阵](knowledge/training/scenario-to-copy.md)反查主SP及H假设。读取单卡同时保留所在文件顶部的适用后期前提；材料允许发散，功能不扩展。只要选材时不自动生成消费者评论，不把144个角度当固定写作配额。
- **补充真实使用体验、空间视角与拍后选择材料、原话或完整讨论**：读[360体验材料指南](knowledge/training/experience-materials.md)和[现有材料盘点](knowledge/materials/STATUS.md)，关联同一原片、实际导出、已知处理与本人偏好；缺失不由成片倒推。该方向不限制其他卖点，材料完整不等于评论必须复述过程。这里只整理材料时不进入每日新稿统计。
- **谁会用、为什么买、为什么搁置、使用心理或表达分析**：读[人群与心理使用指南](references/audience-guide.md)，组合场景、需求假设、使用阶段及后期投入；需要解释产品如何帮助时再查精确型号的事实卡。
- **真实评论资料**：用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。
- **主评论、回复、改写或案例示范**：先读[项目共用写手入口](../../writer-core/adapters/op/write-consumer-training-comments.md)，由共享消费者写作技能承担表达与检查；本库提供产品事实及角色假设。用户调用[360个人入口](/Users/luocaihua/.codex/skills/write-dji-osmo360-comments/MODULE.md)时保留其型号与证据边界。已读取的入口不循环加载，不复制另一套写作规则。
- **验收或维护**：按[维护说明](knowledge/MAINTENANCE.md)复核变化项，运行现有检索审计；心理假设与训练稿另行检查，不写进官方事实卡。

- [事实索引](knowledge/INDEX.md)
- [卖点](knowledge/selling-points.md)
- [场景卡](knowledge/scenario-bank.md)
- [选材矩阵](knowledge/training/scenario-to-copy.md)
- [体验](knowledge/training/experience-materials.md)
- [人群假设](references/audience-guide.md)

可选本地查询脚本：`knowledge/scripts/knowledge.py`，先查脚本用法，路径以本技能目录为基准。无Python时直接阅读索引与命中记录。完整知识、场景、来源和原话仍在包内，不要一次全读。

## 型号与证据

区分Osmo360与Osmo360II及竞品，不能仅因提到360默认II。全景球面规格和平面导出、防水和水下拼接、拍摄和后期效果分别核验；没有同条件证据不判竞品胜负。保留Osmo名称。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

返回少量相关事实、可选兴趣点、命中来源与未解决事项。资料内涉及其他技能的旧指引仅作历史上下文；本阶段不执行跨技能路由。若需要新原帖材料，返回missing_evidence给总控，不自行重开S1；需要成稿则返回facts_ready，不自行调用写手。
