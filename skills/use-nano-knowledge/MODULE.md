---
name: use-nano-knowledge
description: Use the op project's DJI Osmo Nano facts, selling points, scenarios, real experience sources and audience reasoning for product questions and consumer-comment training. Trigger on Nano能力库, Nano卖点, Nano使用场景, 佩戴体验, 第一视角观看感受, 人群心理 or the ow product route. Keep facts, source quotations, inferred value and fictional training separate; route actual comments through the shared writer.
---

# Nano 产品与人群能力库

版本：`2026-09-08-NANO-4`。供本项目各对话直接调用，无需读取建库聊天。根据当前问题选择下面的资料，不必每次通读所有文件。

## 按问题取用

| 当前任务 | 入口与输出 |
|---|---|
| 产品是什么、如何使用、条件与误区 | 从[产品索引](knowledge/INDEX.md)检索少量事实；回答保留具体组件、模式、固件、条件和来源 |
| 补充卖点、细化场景、为培训文案选材 | 从[卖点与场景专题](knowledge/TRAINING.md)进入18组卖点、54个细分兴趣与60张细场景卡，按当前片段和人物关注点检索；可用[卖点反查场景](knowledge/selling-points/scenario-map.md)寻找不同任务，阅读适合／不适合信号及关联事实条件 |
| 佩戴体验、第一视角观看感受、真实使用阶段与原句 | 读[体验材料](knowledge/experience/README.md)，按原帖子类型检索作品、原话与设备／处理说明；区分作者自述、实际视觉证据、真实回复及其缺口。用户表达偏好单查[原句反馈](knowledge/experience/feedback.md) |
| 还有哪些可能使用的人群 | 读[人群分析方法](references/audience-guide.md)，按拍摄任务和需求扩展；不要把身份直接等同于需求或购买意愿 |
| 深入理解角色动机、犹豫和表达 | 从[角色需求假设](references/audience-hypotheses.jsonl)选取或新建分析角度，结合当前材料解释心理如何影响措辞；这些是假设，不是用户研究结论 |
| 真实评论资料 | 用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](/Users/luocaihua/.codex/skills/read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。 |
| 写或改 Nano 主评论、回复、批量培训稿 | 完成必要产品检索后，使用[共享消费者写手](/Users/luocaihua/.codex/skills/write-consumer-comments/MODULE.md)；数量、人物、互动、表达、训练状态和检查均由它负责 |

仅问产品时直接回答产品；仅分析心理时不强制生成评论批次。需要短句解释表达差别时，遵循共享写手的表达原则，并明确为培训用假想示例。正式评论批次才按共享训练契约保存完整人物、来源、断言、稿件和检查记录。

## 取证与分析

1. 先理解当前问题、帖子或训练命题。提取具体事件、拍给谁、想留下什么和实际顾虑；未给出的背景可作明确标注的编辑假设。若本次要读取新社媒链接，依项目及共享库的统一采集规则处理，不在这里建立采集流程。
2. 产品问题用知识索引、主题与关键词检索；人群问题用角色假设的关键词与分析方法检索。卖点与细场景可用 `scripts/find_material.py` 搜关键词或ID，返回完整卡片、关联事实和来源，不能把相关度当作适用或推荐结论。角色可以重叠、动机可以冲突，现有角色与场景都只是起点，不是固定人设名单或评论模板。
3. 读取关联事实的完整条目，保留事实 ID、组件、条件、不可推论、来源定位和核验日期。`pending` 只说明待核；角色的 `related_fact_ids` 仅提供查询方向，不证明设备满足了该角色需求。
4. 产品断言进入正文前核对当前官方来源；价格、套装、固件与兼容性按使用当日核验。历史核验日期不自动变为今天。资料冲突进入[待核清单](knowledge/GAPS.md)，不自行选一个说法写成确定能力。
5. 将“官方事实”“编辑推演的动机”“假想人物的表达”分别呈现。心理分析回到具体事件与使用前、使用中或使用后的行为，不以身份、年龄、性别推断统一心理，不编造人群规模或真实反馈。

使用真实体验资料时，保留其原帖、原话定位、实际回复关系和阅读范围。完整媒体文件存在不等于已经完整视听，抽帧不证明声音；公开评测正文不称未经润色的口述。佩戴位置、固定方法、佩戴感受和回看感受分别核实，双手入镜不能证明某种佩戴方式。使用阶段依据本人线索，未知不补；个案不升级为人群规律。收录沿用[共享体验材料规则](/Users/luocaihua/.codex/skills/write-consumer-comments/references/experience-materials.md)，不另建采集流程。材料可以完整，评论只取最值得说的一点，不把资料字段拼成正文。

新增场景附带可选的拍后观看价值与使用阶段角度，卖点附带可分别使用的兴趣点；先挑一项相关内容，不把各阶段或兴趣串成固定正文。直接欣赏已看过的效果可以独立成立，技术归因另核。

卖点卡的使用价值是 `editorial_interpretation`，细场景与心理是 `editorial_hypothesis`；卡片编写日期不替代事实核验日期。按当前帖子选择有用的少量关注点，允许不采用卡片或扩展新任务；不要把卡片字段变成每条评论必须包含的句式。品类共有能力不直接当成Nano独家或竞品缺失，具体竞争判断另需可比证据。

Nano 的准确名称可以包含 Osmo。保留主相机与多功能图传模块、内置录制与卡导出、各麦克风型号及固件的区别；不继承 Pocket 的命名禁词、机械云台或跟随能力。不能因第一视角、免手持等构想推导全程不用操作、任意佩戴可靠或自动拍好。

## 培训与校准

- 新写、改写与案例演示保持 `training_fiction`。具体人物经历保存在当批训练输出，不写入产品事实库。分析方法与需求假设存本技能的 references，不冒充官方资料。
- [现有 10 类心理表达示例](../../../outputs/nano/2026-09-06-audience-psychology/analysis.md)仅供解释方法，状态仍为 `pending_user_calibration`。不得复制成通用答案，也不得因本次封装或自动检查通过而改为用户认可范文。
- 实际产品断言按共享训练契约绑定当前核验的 `product` 来源和 `product_fact` 断言；知识 ID 只用于检索追溯，不替代证据或引入旧审查 claim 注册流程。
- 明确要求真实材料核验或旧稿审查时，进入[Nano 个人入口](/Users/luocaihua/.codex/skills/write-dji-nano-comments/MODULE.md)的对应分支，保留材料性质；不把旧稿重标为训练稿。所有分支均不授权发布。

## 调用关系

自然语言可说“调用 Nano 能力库”“调用 Nano 卖点与场景库”“这个 Nano 场景还能写哪些关注点”；显式调用为 `$use-nano-knowledge`，项目产品代码为 `ow`。[项目写手入口](../../writer-core/adapters/op/write-consumer-training-comments.md)和本项目直接调用 `$write-dji-nano-comments` 的任务也使用这里的 Nano 资料。已经从项目写手入口进入时，不回调入口，直接继续共享写手；知识索引和共享库已读的部分不循环加载。

维护与验收见[封装验收记录](knowledge/evaluation/packaging-acceptance.md)。修改事实遵循知识库维护规则；新增角色假设保留假设来源和待校准状态，用户明确确认的反馈才按其授权范围更新。
