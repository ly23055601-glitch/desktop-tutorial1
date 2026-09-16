---
name: write-dji-pocket-comments
description: Draft or revise DJI Pocket consumer-comment training fiction through the shared consumer-writing skill, with Pocket-specific names and product facts. Also route explicit real-material verification or legacy draft review to the preserved workflow. Training and review only, never publishing.
---

# DJI Pocket 消费者评论入口

## 默认训练路由

写评、改写和案例演示统一作为培训教育稿，使用`content_mode=training_fiction`、`product_line=pocket`。先读取[共享消费者写作](../../writer-core/core/write-consumer-comments/MODULE.md)，由共享层统一负责选材、人物、种草、表达与教学诊断，以及主评与回复数量、格式、材料读取及训练检查。真实链接、真实素材或用户表示自己用过，都不切换写作模式；已读证据包直接复用。

本层只补充目标产品、称呼、产品事实与专属原帖证据。训练允许的购买、持有、使用、关系和主观感受设定按共享层执行；这些设定不构成真实产品参数或原帖事实的证据。涉及实时社媒读取时执行共享层指向的[统一社媒读取技能](../read-social-links-with-social-helper/MODULE.md)。

理解当前材料、目标型号和开口理由后，直接按[个人Pocket知识索引](../use-pocket-knowledge/knowledge/INDEX.md)检索相关产品事实、场景与有来源的表达材料；检索方式和证据边界见[产品知识](references/product-knowledge.md)。主库聚焦Pocket4/Pocket4P，其他代际须另核对应资料。已从知识入口或共享写手进入时只取必要资料，不回调完整入口。产品问答或知识分析可单独使用[个人Pocket知识技能](../use-pocket-knowledge/MODULE.md)。

按需取[卖点与使用价值](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/selling_points/guide.md)和[详细场景选材](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/use_cases/guide.md)，先看当前帖的触发线索，再选相关任务、取舍和产品依据；用途是编辑解释，场景是假设，不给每条评论分配固定卖点槽位

拍摄观感、个人审美、使用习惯与实际接话可按需读[观感与表达](../use-pocket-knowledge/knowledge/aesthetics/README.md)，只取与当前整帖有关的一组；完整作品、有限抽帧、作者原话和用户表达反馈分别使用，未补齐项不充当已读效果。

## 产品专属边界

- 目标是DJI Pocket口袋云台相机；不把Action、Nano、360、OM或RS的产品能力当作Pocket功能。
- 先区分原帖拍摄设备与训练角色持有或想买的设备。角色设定不证明原帖使用了同一型号。
- 型号已明确时，按对应代际使用`Pocket4`、`p4`、`大疆Pocket4`，`Pocket4P`、`4p`、`大疆Pocket4P`，或`Pocket3`、`p3`、`大疆Pocket3`等已有称呼；型号不明时用`Pocket`、`大疆Pocket`、`DJIPocket`。同帖多条主评点名时变换清晰的全称和简称，不固定排列，也不为换称呼猜代际。
- **Pocket评论与回复正文不用`Osmo`及其大小写变体**；产品知识和来源名称可保留官方拼写。此命名约束仅属于Pocket。
- 涉及功能、参数、价格、套装、兼容或竞品比较时，读取[产品知识](references/product-knowledge.md)的产品事实部分，并按当日官方来源核验。历史快照与[事实注册表](references/product-claims.json)保留为核验线索，不自动证明当前事实。
- 三轴机械云台、光学镜头切换、数码变焦、拍摄模式及成片效果分别核验；不能从漂亮成片或水印直接推出型号、已用功能或产品因果。

## 按需资料与兼容模式

旧LH写作参考、`product-seeding.md`、个人材料状态和同质化脚本均只在下述真实材料／旧稿模式按需使用；训练不加载其中的表达配额、经历限制或状态契约。

产品资料只消费型号、机制、参数、核验入口和事实条件；其中任何旧数量、先强卖点、固定槽位、结尾、角色经历或可迁移文风要求均不覆盖共享层，也不沿产品资料回读完整旧入口。

只有用户明确要求对真实消费者资料、本人亲历进行专门核验或复核旧稿时，才对该核验／审查任务使用`content_mode=real_material`并读取[保留的真实材料与旧稿流程](references/legacy-real-material-workflow.md)。旧稿不为通过审查而重标为训练稿，核验与审查均不授权发布。原脚本、测试、状态模板和事实注册表保持原状，供其兼容流程使用；`training_fiction`使用共享层训练检查，不调用旧真实性严格检查器。
