---
name: write-consumer-training-comments
description: Route consumer comment training in the op project through the shared cross-product writing library. Use for main comments, replies, case demonstrations and batch style calibration for any product, including requests to call the project writing library. Training and review only, never publishing.
---

# 项目写手能力库｜跨产品培训评论

入口版本：`2026-09-15-CW5.4.2-SHARED-ROUTER`。本入口供op项目内各任务共用，只确定调用路径；表达版本以共享库当前`SKILL.md`为准，能力与反馈集中维护，不依赖本对话历史

## 调用路径

- Pocket任务先读取[项目Pocket入口](../write-pocket-seeding-comments/SKILL.md)，由它进入共享库并保留Pocket命名、型号和事实要求
- Nano任务先读取[本项目Nano能力入口](../use-nano-knowledge/SKILL.md)，根据当前帖子或训练命题检索产品事实、[卖点与细场景选材](../../../knowledge/nano/TRAINING.md)、[真实体验与原句](../../../knowledge/nano/experience/README.md)及必要的角色心理假设，再进入[共享消费者写作能力](/Users/luocaihua/.codex/skills/write-consumer-comments/SKILL.md)。直接调用Nano个人技能时同样使用本地资料；已读入口不回调，不复制另一套写法。引用保留事实ID、组件、条件、来源和核验日期，待核项不得写成肯定能力；心理假设不冒充用户研究，训练示例不自动成为认可案例。实际产品断言按共享训练契约绑定当前核验的`product`来源与`product_fact`断言
- Mobile任务先读取[个人Mobile产品与人群能力入口](/Users/luocaihua/.codex/skills/use-mobile-knowledge/SKILL.md)，按具体型号检索事实、兼容条件和场景，按需取产品卖点、[详细场景选材](/Users/luocaihua/.codex/skills/use-mobile-knowledge/knowledge/use_cases/guide.md)与角色心理假设，再进入共享消费者写作能力。直接调用`$write-dji-osmo-mobile-comments`使用同一资料，保留个人入口产品边界。引用携带事实ID、设备组合、路径、条件、来源及核验日期；`pending/conflict`不作肯定依据，实际产品断言绑定当前核验的`product`来源与`product_fact`断言。已读入口不回调；角色心理、场景推演与待校准示例不当作原帖、真实体验或认可范文
- Mic任务先读取[个人 Mic 产品与人群能力入口](/Users/luocaihua/.codex/skills/use-mic-knowledge/SKILL.md)，按精确型号和问题检索独立快照中的事实、连接条件、场景或心理假设，再进入[共享消费者写作能力](/Users/luocaihua/.codex/skills/write-consumer-comments/SKILL.md)。直接调用 Mic 个人技能也使用同一资料，已读入口不回调；[项目维护源](../../../knowledge/mic/INDEX.md)用于明确维护知识库的任务。保留事实 ID、发射／接收部件、连接方式、条件、来源和核验日期；待核／冲突不得写成肯定能力，内录与接收输出分别核验。心理资料不冒充调研或认可案例；实际产品断言绑定当前核验的`product`来源与`product_fact`，知识 ID 不替代核验
- Osmo 360任务先进入[项目Osmo 360知识入口](../use-osmo360-knowledge/SKILL.md)，按具体型号检索[本项目360知识库](../../../knowledge/osmo360/INDEX.md)，需要人群分析时读取[心理假设指南](../use-osmo360-knowledge/references/audience-guide.md)，再进入[共享消费者写作能力](/Users/luocaihua/.codex/skills/write-consumer-comments/SKILL.md)。直接调用360个人技能也使用这些本地资料，并保留个人入口边界；不回调本入口，已读资料不重复加载。区分两代、全景与平面导出；保留事实ID、条件、来源和核验日期，待核／冲突不作肯定能力。产品断言绑定当前实际核验的`product`来源与`product_fact`，心理假设、人物经历和待校准示例不当作事实或认可范文
- 其他产品读取[共享消费者写作能力](/Users/luocaihua/.codex/skills/write-consumer-comments/SKILL.md)，按其中的产品路由使用对应资料；没有专属产品技能也可使用共享库
- 用户明确调用某个产品技能时读取该入口，它提供产品要求，写法仍使用同一共享库。本入口不回调自身，也不复制旧产品流程的数量、对话或经历限制

## 横测链接路由（CW5.4.2）

原帖明确出现两台及以上设备的实际对照、同场景实拍比较、可核验的排名／名次，或使用后对不同设备的取舍时，进入共享横测分支。先确认对照对象、场景和比较依据确实在原帖证据中，再分别核验每个产品型号、能力与使用条件；横测的消费者表达以任务指定产品为种草中心，至少一条主评明确点出目标品牌或型号，竞品只作必要参照，不写成等量推荐。只有单纯求助、咨询或想了解差异而没有实际对照证据的帖子，不触发横测分支，按普通产品语境处理，不补造对照、排名或使用后结论。

写评、改写及案例演示统一按`training_fiction`培训教育用途处理。真实链接和真实材料提供选材依据，不使新稿切换为实际生产。真实资料、本人亲历核验或旧稿审查依共享库和产品入口的审查分支处理，保留原材料性质

Osmo 360（项目代码`oq`）选材可查[卖点与用户价值专题](../../../knowledge/osmo360/selling-points.md)，按原帖任务、精确型号和人物关注点取相关条目。具体事件与文案切口可查[48张场景卡](../../../knowledge/osmo360/scenario-bank.md)及[选材矩阵](../../../knowledge/osmo360/training/scenario-to-copy.md)，读取单卡时保留适用的后期前提；SC素材不是原帖证据或固定句式。专题的用户收益是编辑解释，心理关联是待验证假设；它们不替代产品证据，也不要求每条评论带齐参数或推荐结论。原始事实与条件仍回到知识卡及实际读取的官方来源。

五品线补充原话、完整讨论、使用阶段与逐句反馈时，读取[共享体验材料指南](/Users/luocaihua/.codex/skills/write-consumer-comments/references/experience-materials.md)。360空间视角／拍后选择可查[产品侧体验材料](../../../knowledge/osmo360/training/experience-materials.md)，Mic实际声音／佩戴连接可查[产品侧体验材料](../../../knowledge/mic/training/experience-materials.md)；优先方向不限制其他卖点。知识维护和材料整理不登记为每日新稿，数量和写法仍使用共享当前入口。


主页／新品预写和逐句详略校准使用共享[2026-09-15学习经验](/Users/luocaihua/.codex/skills/write-consumer-comments/references/calibration-20260915/learning.md)。白色Pocket4P本批数量、禁提和同单元格布局只在对应任务生效；其他品线不继承

## 材料与交付

需要读取新抖音、小红书、B站链接时，按共享库调用[统一社媒读取技能](/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/SKILL.md)，一次性交入本次完整链接集合；本入口不另建采集流程。已有充分材料直接按共享库处理

选材、消费者表达、人物设定、种草、主评与回复数量、格式、事实分离、教学诊断和最终检查，全部使用共享库当前规则。最终编号稿、训练状态与检查记录按当批保存，教学说明按需另存；历史稿件和通过记录不自动成为用户认可案例

可直接说“调用写手能力库”或“按项目写手标准”，也可调用`$write-consumer-training-comments`。原`$write-consumer-comments`及各产品调用名继续可用
