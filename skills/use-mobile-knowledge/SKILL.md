---
name: use-mobile-knowledge
description: 仅由总控S2派单或显式知识查询读取Osmo Mobile / DJI OM事实、场景与表达资料；返回来源和缺口，不启动采集、写作或质检。
---


# S2 Osmo Mobile / DJI OM知识

输入具体问题、品线/型号、S1材料范围与本轮已有事实包。只查相关资料，完成后返回总控；用户只问知识时返回分析即可。product_line=`osmo_mobile`。

## 按需检索

- [事实索引](knowledge/INDEX.md)
- [卖点](knowledge/selling_points/guide.md)
- [场景](knowledge/use_cases/guide.md)
- [体验材料](knowledge/experience_materials/guide.md)
- [角色心理](knowledge/audiences/guide.md)

可选本地查询脚本：`knowledge/scripts/query.py`，先查脚本用法，路径以本技能目录为基准。无Python时直接阅读索引与命中记录。完整知识、场景、来源和原话仍在包内，不要一次全读。

## 型号与证据

资料包括8P、8及旧代，不能默认最新款。区分手机、云台、App、系统、配件、固件与跟随路径；快门控制不等于跟拍，能安装不等于完整兼容。保留Osmo名称，不继承Pocket禁词。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

返回少量相关事实、可选兴趣点、命中来源与未解决事项。资料内涉及其他技能的旧指引仅作历史上下文；本阶段不执行跨技能路由。若需要新原帖材料，返回missing_evidence给总控，不自行重开S1；需要成稿则返回facts_ready，不自行调用写手。
