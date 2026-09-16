---
name: use-pocket-knowledge
description: 仅由总控S2派单或显式知识查询读取Pocket事实、场景与表达资料；返回来源和缺口，不启动采集、写作或质检。
---


# S2 Pocket知识

输入具体问题、品线/型号、S1材料范围与本轮已有事实包。只查相关资料，完成后返回总控；用户只问知识时返回分析即可。product_line=`pocket`。

## 按需检索

- [事实索引](knowledge/INDEX.md)
- [统一资料入口](knowledge/START.md)
- [卖点](knowledge/selling_points/guide.md)
- [详细场景](knowledge/use_cases/guide.md)
- [观感与审美](knowledge/aesthetics/README.md)
- [真实表达](knowledge/voice/README.md)
- [比较](knowledge/comparisons/README.md)

可选本地查询脚本：`knowledge/scripts/pocket_knowledge.py`，先查脚本用法，路径以本技能目录为基准。无Python时直接阅读索引与命中记录。完整知识、场景、来源和原话仍在包内，不要一次全读。

## 型号与证据

重点资料包含Pocket4/Pocket4P及旧代，但仅说Pocket时不能默认型号。区分云台、镜头/焦段、变焦、跟随、拍摄模式、收音、导出与配件条件。不能从漂亮成片推断设备或参数。Pocket评论正文专属禁用Osmo，不能扩散至其他品线。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

返回少量相关事实、可选兴趣点、命中来源与未解决事项。资料内涉及其他技能的旧指引仅作历史上下文；本阶段不执行跨技能路由。若需要新原帖材料，返回missing_evidence给总控，不自行重开S1；需要成稿则返回facts_ready，不自行调用写手。
