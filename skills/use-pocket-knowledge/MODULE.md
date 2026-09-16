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

将 `<技能目录>` 替换为本次发现的 `MODULE.md` 所在目录的绝对路径；不要从当前工作目录猜原项目位置。查询只需Python 3.9+标准库，不需要社媒助手或重新采集。

重点资料包含Pocket4/Pocket4P及旧代，但仅说Pocket时不能默认型号。区分云台、镜头/焦段、变焦、跟随、拍摄模式、收音、导出与配件条件。不能从漂亮成片推断设备或参数。Pocket评论正文专属禁用Osmo，不能扩散至其他品线。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

## 卖点与详细场景选材

要理解产品为什么值得关注、适合在哪里使用时，按需读取[卖点与使用价值](knowledge/selling_points/guide.md)、[详细场景库](knowledge/use_cases/guide.md)及[选材入口](knowledge/TRAINING.md)，不只列参数。把官方能力、由此可能减少的麻烦、具体拍摄任务和成立条件连接起来；共有能力不宣称独家，选择4P的理由也不能简化成所有场景都更好。

```bash
python3 "<技能目录>/knowledge/scripts/pocket_materials.py" search '一个人旅行 架机拍自己' --model pocket_4 --kind scene
python3 "<技能目录>/knowledge/scripts/pocket_materials.py" search '人像 中焦 半身' --model pocket_4p --kind selling
python3 "<技能目录>/knowledge/scripts/pocket_materials.py" search 'PSP-001' --kind scene
```

先按当前问题选一两项；需要展开再用单个PSP卖点ID、PUC场景ID或PKF事实ID精查。卖点的使用价值是`editorial_interpretation`，详细场景是`editorial_hypothesis`；它们不增加真实用户样本。卡片保留取舍、不适合情况和可能的开口方向，不把字段拼成固定评论或要求每条都强调卖点。原话机制另查表达库；实际写作时按当前原帖和共享写手规则选择。

## 拍摄观感、使用习惯与个人审美

按需读[观感与表达入口](knowledge/aesthetics/README.md)，从当前帖的整体内容选择[作品材料](knowledge/aesthetics/works.md)、[偏好和使用阶段](knowledge/aesthetics/preferences.md)、[单组真实讨论](knowledge/aesthetics/discussions.md)或[原句反馈](knowledge/aesthetics/feedback.md)。不用一口气读取全部原始材料，也不以补充知识为由扩大采集。

完整作品、抽帧与作者文字分别标明实际读取范围；直出、机内风格、外部滤镜和调色注明来源，不从观感猜设置。本人审美只取本人明确材料，认可某句表达不等于认可对应产品效果或拥有那种经历。阶段按“刚到手、还在练手、平时会拍什么”等明说信息理解，C2缺父句不补成楼中楼。完整实拍作品和常用配件的持续感受仍有[待补项](knowledge/aesthetics/gaps.md)，不得用现有抽帧、文件在场或已保存链接冒充补齐。

材料可以完整，评论只取其中最值得说的一点；不把使用过程拼成“背景＋场景＋卖点＋总结”。保留成立的直接喜欢与自然长句，普通附和不必每次新增知识；实际稿件继续沿用当前共享写手要求。

## 产品、场景与表达分别使用

- **产品问答与比较**：读命中事实完整的型号、条件、用途、不可推断项、来源及核验日期，必要时看[两款按流程对照](knowledge/products/pocket4-vs-pocket4p.md)和[主题缺口](knowledge/products/topic-coverage.md)。`verified`是记录日期的官方核验，不是实机测试或永久有效；回答当前能力或写入稿件前核对当前官方资料。`pending`、官方冲突不得作肯定依据，封装日期不刷新事实日期。跟随启动、镜头切换、模式、收音、配件与素材导出分别核对，不能拿相邻模式拼成完整教程。
- **真实关注与口吻**：读[表达入口](knowledge/voice/README.md)及命中卡的处境、需求、熟练程度、态度、原话、父句和不可迁移项。`pattern`表示至少三篇独立作品的表达例证，`case`仅是个案；都不证明人口占比、普遍心理、购买转化或现实身份。第三方经历保持归属，不复制成说话者亲历。父句未知不补关系，未读图片/视频/声音不补成原帖证据。
- **使用动机与心理分析**：用已有场景和原话说明这个处境可能在意什么；推想明确标为编辑假设，并保留其他可能解释。没有心理调研或完整人群画像。按处境和取舍理解，不能仅凭年龄、职业等标签确定动机。

公共语料的当前数量、平台与批次范围以[动态覆盖](knowledge/COVERAGE.md)和[封装统计](knowledge/corpus-statistics.json)为准。历史学习/留出分组保持，停止附件不用于学习；用户新授权的研究批次独立记录，不能把旧材料补算为新批次成果。

比较需求可按需读[竞品与代际比较表达](knowledge/comparisons/README.md)，或查询 `search '旅行 携带' --model pocket_4 --competitor 手机`。专题保留继续使用其他设备、不升级与不同偏好；原话提到的产品名不自动成为已核型号，具体能力比较仍须核对双方当前官方来源。个案只用于理解开口理由与取舍，不转换为胜负结论或固定句式。

## 真实评论资料

用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](../read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。

## 需要写评论时

仅写评、回复、改写或案例任务才接入[共享消费者写手](../write-consumer-comments/MODULE.md)，补充[Pocket专属边界](../write-dji-pocket-comments/MODULE.md)的产品与命名部分；已读入口不回调，不进入旧写作分支。知识库提供少量相关事实、场景和表达观察，不另定评论数量、文风或对话模板。

新评论使用共享`training_fiction`规则。独立假想人物和经历只存在于该任务，不变成用户本人素材、产品事实或原帖证据；不能把公共原话改配为角色的经历。Pocket评论正文不使用Osmo，产品知识与官方来源名称可以保留。实际能力按当前证据绑定`product`来源与`product_fact`断言。两帖研究示例有额外经历限制，是有限历史对照，不给所有训练任务追加同一限制。

明确核验真实资料或复核旧稿时，才转Pocket写作入口的对应分支；核验不授权发布。读取真实社媒链接仍走共享层指向的统一社媒技能，本知识包不另建采集流程。

产品和表达查询独立运行；正式评论另依赖同机共享写手及Pocket写作入口。包是显式维护的快照，原项目更新后再按[封装维护说明](knowledge/PACKAGE.md)刷新，不承诺后台同步。
