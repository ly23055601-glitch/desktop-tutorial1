---
name: use-nano-knowledge
description: 仅由总控S2派单或显式知识查询读取Osmo Nano事实、场景与表达资料；返回来源和缺口，不启动采集、写作或质检。
---


# S2 Osmo Nano知识

输入具体问题、品线/型号、S1材料范围与本轮已有事实包。只查相关资料，完成后返回总控；用户只问知识时返回分析即可。product_line=`nano`。

| 当前任务 | 入口与输出 |
|---|---|
| 产品是什么、如何使用、条件与误区 | 从[产品索引](knowledge/INDEX.md)检索少量事实；回答保留具体组件、模式、固件、条件和来源 |
| 补充卖点、细化场景、为培训文案选材 | 从[卖点与场景专题](knowledge/TRAINING.md)进入18组卖点、54个细分兴趣与60张细场景卡，按当前片段和人物关注点检索；可用[卖点反查场景](knowledge/selling-points/scenario-map.md)寻找不同任务，阅读适合／不适合信号及关联事实条件 |
| 佩戴体验、第一视角观看感受、真实使用阶段与原句 | 读[体验材料](knowledge/experience/README.md)，按原帖子类型检索作品、原话与设备／处理说明；区分作者自述、实际视觉证据、真实回复及其缺口。用户表达偏好单查[原句反馈](knowledge/experience/feedback.md) |
| 还有哪些可能使用的人群 | 读[人群分析方法](references/audience-guide.md)，按拍摄任务和需求扩展；不要把身份直接等同于需求或购买意愿 |
| 深入理解角色动机、犹豫和表达 | 从[角色需求假设](references/audience-hypotheses.jsonl)选取或新建分析角度，结合当前材料解释心理如何影响措辞；这些是假设，不是用户研究结论 |
| 真实评论资料 | 用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。 |
| 写或改 Nano 主评论、回复、批量培训稿 | 完成必要产品检索后，使用[共享消费者写手](/Users/luocaihua/.codex/skills/write-consumer-comments/MODULE.md)；数量、人物、互动、表达、训练状态和检查均由它负责 |

- [事实索引](knowledge/INDEX.md)
- [卖点与细场景](knowledge/TRAINING.md)
- [卖点反查](knowledge/selling-points/scenario-map.md)
- [体验](knowledge/experience/README.md)
- [人群假设](references/audience-guide.md)
- [缺口](knowledge/GAPS.md)

可选本地查询脚本：`scripts/find_material.py`，先查脚本用法，路径以本技能目录为基准。无Python时直接阅读索引与命中记录。完整知识、场景、来源和原话仍在包内，不要一次全读。

## 型号与证据

区分主相机、图传模块、配件、佩戴方式、固件、录制与导出。双手入镜不证明佩戴方式；不能借用Pocket机械云台或跟随能力，免手持不代表全程免操作。

保留fact_id、claim、准确型号/组件、conditions、限制、source、checked_at与status。verified只表示记录日期的核验，不是实测或永久有效；写入当前产品结论前按实际条件复核官方依据，不能把封装日期写成核验日期。来源不可读则标明历史快照；pending/conflict只能作为缺口，没命中不等于不支持。

原话保持作者归属与完整父句/来源范围；第三方自述不是当前说话者亲历。场景/用途价值/心理推演明确是编辑假设，不冒充人群调研、占比或产品承诺。抽帧、历史稿、用户偏爱不能证明设备参数。

Nano 的准确名称可以包含 Osmo。保留主相机与多功能图传模块、内置录制与卡导出、各麦克风型号及固件的区别；不继承 Pocket 的命名禁词、机械云台或跟随能力。不能因第一视角、免手持等构想推导全程不用操作、任意佩戴可靠或自动拍好。

## 培训与校准

- 新写、改写与案例演示保持 `training_fiction`。具体人物经历保存在当批训练输出，不写入产品事实库。分析方法与需求假设存本技能的 references，不冒充官方资料。
- [现有 10 类心理表达示例](../../../outputs/nano/2026-09-06-audience-psychology/analysis.md)仅供解释方法，状态仍为 `pending_user_calibration`。不得复制成通用答案，也不得因本次封装或自动检查通过而改为用户认可范文。
- 实际产品断言按共享训练契约绑定当前核验的 `product` 来源和 `product_fact` 断言；知识 ID 只用于检索追溯，不替代证据或引入旧审查 claim 注册流程。
- 明确要求真实材料核验或旧稿审查时，进入[Nano 个人入口](/Users/luocaihua/.codex/skills/write-dji-nano-comments/MODULE.md)的对应分支，保留材料性质；不把旧稿重标为训练稿。所有分支均不授权发布。

## 调用关系

自然语言可说“调用 Nano 能力库”“调用 Nano 卖点与场景库”“这个 Nano 场景还能写哪些关注点”；显式调用为 `$use-nano-knowledge`，项目产品代码为 `ow`。[项目写手入口](../../writer-core/adapters/op/write-consumer-training-comments.md)和本项目直接调用 `$write-dji-nano-comments` 的任务也使用这里的 Nano 资料。已经从项目写手入口进入时，不回调入口，直接继续共享写手；知识索引和共享库已读的部分不循环加载。

维护与验收见[封装验收记录](knowledge/evaluation/packaging-acceptance.md)。修改事实遵循知识库维护规则；新增角色假设保留假设来源和待校准状态，用户明确确认的反馈才按其授权范围更新。
