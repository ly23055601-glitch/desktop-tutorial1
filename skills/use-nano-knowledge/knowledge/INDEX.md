# DJI Osmo Nano 产品知识库

本库服务 op 项目的评论与内容培训。首版核验日期 **2026-09-06**，**2026-09-07**扩充卖点与细场景并补充10-bit事实。当前为 **81 条事实（79 条已核、2 条待核）、8 个官方来源、7 张基础场景卡、14 组常见问答**；另有 **18 组卖点与使用价值、80 张培训细场景卡、54 个卖点细分兴趣**。事实实际核验日期逐条保留，编辑扩充不等于全部产品资料重新核验。

**2026-09-08**新增28张细场景卡与54个卖点兴趣解释；**2026-09-09**再新增20张具体取舍卡，并为18组卖点补充“何时有用／何时价值下降／观察什么”。新增卡保留拍后观看价值和使用阶段角度，均为编辑推演。同日另补[16件公开作品与原话](experience/README.md)、其中1件的[4组真实主评与回复](experience/discussions.md)，以及[15条真实材料选材路径](experience/selection-map.md)和用户明确表达反馈。它们独立于官方事实和假设卡；同源佩戴与拍后评价、明确购前原话和被否定旧句仍待补，视频阅读范围按件记录，不能将入库数量当作完整体验证据数量。

## 从这里开始

| 想解决的问题 | 阅读入口 |
|---|---|
| 了解产品、组件和能力边界 | [产品事实阅读版](products/guide.md) |
| 看10个主题目前覆盖到哪里 | [主题覆盖表](products/topic-coverage.md) |
| 查常见误区和具体问题 | [常见问题](products/faq.md) |
| 从拍摄任务找到相关知识 | [7类场景解释](scenarios/guide.md) |
| 详细发散卖点、使用场景和培训文案关注点 | [卖点与场景选材专题](TRAINING.md) |
| 查某个卖点的使用价值与不适合情况 | [18组卖点](selling-points/guide.md) |
| 从已选卖点反查不同拍摄任务 | [卖点反查场景](selling-points/scenario-map.md) |
| 从具体生活片段找到多种表达方向 | [80张细场景卡](scenarios/training-guide.md) |
| 查真实佩戴、观看感受、使用阶段及原句 | [体验材料与当前缺口](experience/README.md)、[16件公开作品](experience/cases.md)、[用户原句反馈](experience/feedback.md)；来源与阅读范围随件保留 |
| 分析潜在人群、使用心理与培训表达 | [Nano产品与人群能力入口](../../.agents/skills/use-nano-knowledge/SKILL.md)；角色需求假设独立于官方事实 |
| 回查官方网页、手册和版本 | [来源台账](sources/README.md) |
| 查看冲突和未覆盖问题 | [缺口清单](GAPS.md) |
| 更新字段、来源与阅读版 | [维护说明](MAINTENANCE.md) |
| 查看这次实际验收 | [验收记录](evaluation/acceptance.md) |
| 查看跨对话调用与封装验收 | [封装验收记录](evaluation/packaging-acceptance.md) |
| 查看最新场景深化的检查与调用 | [9月8日深化验收](evaluation/scenario-deepening-acceptance.md) |
| 查看前一轮卖点与细场景扩充的检查及试写 | [9月7日扩充验收](evaluation/material-expansion-acceptance.md) |

主相机与多功能图传模块分别承担不同能力。正式部件名使用官网中文称呼；不能把主相机的52克、防水与组合设备的续航、屏幕混在一句无条件描述里。产品名称可用 Nano、Osmo Nano，评论正文的英文连写仍按共用写手库处理。

## 写作调用

1. 先读当前帖子或训练命题，判断确有必要回应的事情。
2. 从主题、问答或关键词找到少量相关事实与场景，读取完整条目的组件、条件、不可推论和来源。
3. 产品事实进入正文前，按引用的来源定位核对当前官方资料；固件、价格、套装与兼容性按使用当日核验。已核日期不自动更新。
4. 按[项目写手入口](../../.agents/skills/write-consumer-training-comments/SKILL.md)继续由共用写手库完成表达；已从该入口进入时，无需重新加载本索引或产品入口。训练状态使用已有的 `product` 来源和 `product_fact` 断言，不引入旧审查claim注册门槛。

在本项目其他对话中可说“调用 Nano 能力库”，或显式调用 `$use-nano-knowledge`。直接调用 `$write-dji-nano-comments` 时，本项目 [AGENTS.md](../../AGENTS.md) 同样路由到 [Nano能力入口](../../.agents/skills/use-nano-knowledge/SKILL.md)。知识库补充产品依据，人群心理假设由能力入口独立管理，写法继续由共享能力维护。

从项目根目录可用关键词查找；`rg`命中的JSONL一行就是完整条目，不裁掉条件：

```sh
rg -n '续航|200分钟|16:9' knowledge/nano/products/facts.jsonl
rg -n '骑行|佩戴|导出' knowledge/nano/scenarios/cards.jsonl
rg -n 'NANO-AUD-007' knowledge/nano/products/facts.jsonl
```

关键词结果可能含 `pending`；选择产品依据时只用 `verified`，待核项只提示问题。场景卡均为 `editorial_hypothesis`，不能当作真实用户反馈。产品能力不证明当前帖子使用了该设备或启用了某模式。

本库不收录假想角色经历、成品评论或未经读取的社媒内容。评论培训保持 `training_fiction`，人物仅存训练状态。后续若需要读取抖音、小红书、B站，仍将本次完整链接集合交给统一社媒读取技能，不另建采集流程。
