---
name: use-pocket-knowledge
description: 调用 DJI Pocket 产品知识、卖点、使用场景、拍摄观感与真实表达，重点 Pocket4、Pocket4P。用于“调用Pocket知识库”“Pocket卖点”“Pocket使用场景”、个人审美、使用习惯、型号比较及 op 产品路径；需要评论时接入共享写手。
---

# Pocket 产品与用户表达能力

本技能自带知识资料和必要来源，可在其他项目或对话独立使用，无需读取原项目或历史聊天。重点是Pocket4、Pocket4P；旧代资料用于辨认型号和比较，不能混为两款当前人群。先按任务取用[知识索引](knowledge/INDEX.md)。

日常先用[统一入口](knowledge/START.md)，将产品、场景、真实表达、审美、比较、反馈与[已确认上下文](knowledge/context/README.md)连起来。它们仍各有唯一维护表，资料类型与实时技能路由登记在[能力目录](knowledge/library.json)；不从归档聊天或旧通过记录恢复写法。

需要围绕一个问题形成完整写作参考时，先运行统一简报；只查单项事实或原检索时，保留下节的`pocket_knowledge.py search`。统一简报不自动写稿、采集、核验官网或把场景假设当亲历。

```bash
python3 "<技能目录>/knowledge/scripts/pocket_library.py" brief '独自旅行 人像 跟随' --model pocket_4p
python3 "<技能目录>/knowledge/scripts/pocket_library.py" brief '同场景 不换 取舍' --model pocket_4p --competitor Pocket3
```

## 按问题检索

将 `<技能目录>` 替换为本次发现的 `MODULE.md` 所在目录的绝对路径；不要从当前工作目录猜原项目位置。查询只需Python 3.9+标准库，不需要社媒助手或重新采集。

```bash
python3 "<技能目录>/knowledge/scripts/pocket_knowledge.py" search '独自拍摄 跟随' --model pocket_4
python3 "<技能目录>/knowledge/scripts/pocket_knowledge.py" search '人物 中焦 收音' --model pocket_4p
python3 "<技能目录>/knowledge/scripts/pocket_knowledge.py" search '收纳 麻烦 闲置' --platform xiaohongshu
```

通常先读默认Markdown简报；需要结构化处理时才加`--format json`并将完整输出保存文件，避免关联来源展开占满上下文。完整事实ID每次查一个，不把多个ID拼成关键词；多个问题分开按需查。

型号可用`pocket_1/2/3/4/4p`或明确的Pocket4、Pocket4P；只有Pocket时省略型号，不默认最新款。默认每类返回少量结果，holdout排除；若没回答具体问题，换成具体操作或用事实ID检索。零结果不是不支持。`resolved_source_path`指向包内依据；原字段仍记录采集时路径。其他归档路径用`resolve-source '原路径'`定位。

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
