---
name: write-pocket-seeding-comments
description: 兼容调用名：仅用户显式指定时把Pocket任务交给唯一总控；不独立采集、写作、执行旧检查器或交付。
---


入口版本：`2026-09-15-CW5.4.2-SHARED-POCKET-ROUTER`。写评、改写和案例演示统一作为`training_fiction`培训教育稿，先读取[跨产品评论写手能力库](/Users/luocaihua/.codex/skills/write-consumer-comments/MODULE.md)，表达版本以该文件当前内容为准，使用其选材、人物、种草、表达与教学诊断，以及数量、格式、互动和训练检查规则。本项目和其他项目共用同一份表达能力，不在此处复制第二套写法。原帖属于同场景实拍、成片对照、排名横测或使用后取舍时，按共享当前横测分支处理；Pocket作为目标产品时至少一条主评明确点名大疆或准确型号，竞品只作参照；普通选购求助不误判为横测

识别目标品线`pocket`，保留用户明确型号、原帖材料、数量、写稿/改稿/审核意图。将这些信息交给[唯一总控](../write-consumer-training-comments/SKILL.md)，本入口结束。

- `product_line`为`pocket`；本入口只处理Pocket，其他产品直接调用共享库或对应产品入口
- 可使用Pocket、大疆Pocket及准确的连写型号；同帖多条主评点名时变换清晰的全称和简称，不固定排列，不为变化猜代际。只有Pocket评论正文禁止Osmo。型号由当前目标、原帖或假想角色明确设定，角色型号不证明原片设备型号
- 按当前材料从[个人Pocket知识索引](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/INDEX.md)检索产品、场景与真实表达，涉及硬件、参数、模式、配件或价格时按来源定位核对当前官方资料；共享库的[产品路由](/Users/luocaihua/.codex/skills/write-consumer-comments/references/product-routing.md)接入同一知识源，已读不回调完整入口或旧写作流程。原帖画面与产品功能分别核验，不把旋转、跟随、后期剪辑或不同代际混用
- [产品依据](references/product-facts.md)是当前知识库与事实接口的索引；其中知识卡和旧claim各自的核验日期不自动成为今日核验。训练人物不写入[已确认本人素材](references/project-context.md)或知识库

按需取[卖点与使用价值](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/selling_points/guide.md)和[详细场景选材](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/use_cases/guide.md)，先看当前帖的触发线索，再选相关任务、取舍和产品依据；用途是编辑解释，场景是假设，不给每条评论分配固定卖点槽位

## 按当前帖调用Pocket知识

读当前帖证据，确定目标型号、场景与开口理由后，使用个人技能内脚本的绝对路径按具体问题检索，不依赖当前工作目录：

```bash
python3 /Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/scripts/pocket_library.py brief '独自旅行 跟随 架机' --model pocket_4 --platform xiaohongshu
```

主库聚焦Pocket4/Pocket4P；型号不明可省略`--model`，平台按当前帖填写。选择少量相关事实、场景和表达材料，保留ID、来源、使用条件与不可推断项，形成写作参考。默认排除holdout；`pending`只作待核项，`case`只作个案，`pattern`保留至少3个独立作品的实际支持范围，`editorial_hypothesis`是编辑假设，不是用户研究。知识卡与历史语料均不能充当当前帖证据

统一简报同时调用原事实/表达与卖点/详细场景检索，按问题附上观感、比较、明确反馈和上下文入口；不要求每层都有结果，也不把所有结果写进正文。单项深查仍可用原`pocket_knowledge.py search`与`pocket_materials.py search`，它们共享同一维护数据。日常完整导航见[统一知识入口](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/START.md)。

培训正文中的产品断言按共享[训练契约](/Users/luocaihua/.codex/skills/write-consumer-comments/references/training-contract.md)绑定实际核验的`product`来源与`product_fact`断言；检索中的`claim_id`和登记提示供LH13旧审查接口使用，不是共享培训流程的注册门槛。公共语料和历史本人素材保留真实归属，不能改标为假想资料或移植为训练人物的经历。独立训练人物只存在于训练state；本次知识库研究与[对照验收](/Users/luocaihua/Documents/ChatGPT/op/knowledge/pocket/evaluation/README.md)仍按研究约定追溯实际第一人称经历，不用虚构经历补研究材料

[原项目知识库](/Users/luocaihua/Documents/ChatGPT/op/knowledge/pocket/INDEX.md)继续作为维护源，更新后显式刷新个人技能快照；跨项目读取不依赖本项目目录。纯产品、需求或表达材料分析可直接调用[个人Pocket知识技能](/Users/luocaihua/.codex/skills/use-pocket-knowledge/MODULE.md)，实际写评仍回到同一共享写手，已读入口不循环加载

拍摄观感、个人审美、使用习惯与实际接话可按需读[观感与表达](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/aesthetics/README.md)，只取与当前整帖有关的一组；完整作品、有限抽帧、作者原话和用户表达反馈分别使用，未补齐项不充当已读效果。

## 训练与旧稿复核

训练稿允许假想购买、持有、使用、关系和主观感受，真实链接、真实素材或用户表示自己用过都不切换写作模式。使用共享`check_training_comments.py`与训练状态，不调用旧LH13真实性检查去要求假想人物提供真实来源，也不把新训练检查通过叫作旧版strict通过

只有用户明确要求对真实消费者资料、本人亲历进行专门核验或复核旧LH13稿时，才对该核验／审查任务使用`content_mode=real_material`并读取[旧真实材料流程](references/legacy-real-material-workflow.md)，继续使用原脚本、模板和证据规则。旧文件保持其原有语义，不为通过而改标training_fiction，核验与审查均不授权发布

[旧11帖稿件](assets/accepted-comments.md)、旧状态和旧审稿记录保留用于历史复核。后续用户已指出其中有设计对话的问题，不能沿用“通过”结论把它们当成新版正面范文

主页／新品预写和逐句详略校准使用共享[2026-09-15学习经验](/Users/luocaihua/.codex/skills/write-consumer-comments/references/calibration-20260915/learning.md)。白色Pocket4P本批数量、禁提和同单元格布局只在对应任务生效；其他品线不继承
