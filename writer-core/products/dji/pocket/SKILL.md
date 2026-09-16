---
name: dji-pocket-comment-adapter
version: CW5.4.2-portable
product_line: pocket
description: Lightweight DJI Pocket adapter for the shared consumer-comment training skill
---

# DJI Pocket 产品适配入口

先读取包内共享写手规则：`../../../core/write-consumer-comments/SKILL.md`

本入口只负责 Pocket 的型号、命名和事实边界，不复制写作逻辑，也不把历史案例当成产品事实。评论均为培训用假想消费者草稿，不用于发布。

## 产品范围

- 目标为 DJI Pocket 口袋云台相机及任务中明确的具体代际
- 型号未确认时只使用 `Pocket`、`大疆Pocket` 或 `DJIPocket`
- 型号确认后再使用对应全称或清晰简称，例如 `Pocket4`、`p4`、`Pocket4P`、`4p`、`Pocket3`、`p3`
- Pocket 正文和回复不使用 `Osmo` 及其大小写变体，这条限制不扩展到其他产品入口
- 不把 Action、Nano、360、Mobile 或 RS 的功能移植为 Pocket 能力

## 事实资料接口

按当前任务只载入 `facts.template.json` 中有来源、有适用型号和条件的条目。实际资料可由宿主 AI、用户提供的官方页面、说明书或当前产品知识库填入；本轻量包不内置大体量知识库。

每条产品断言至少保留：`claim`、`model`、`conditions`、`source`、`checked_at` 和 `evidence_level`。漂亮成片、训练人物经历或抽帧不能单独证明型号、功能、参数或产品因果。

涉及云台、镜头、变焦、模式、成片效果、价格、套装、兼容或竞品比较时，先核对具体型号和使用条件；待核项只能写成兴趣、期待或问题，不能写成肯定事实。

## 交给共享写手

先理解整帖，再从产品与原帖的实际联系中选消费者关注点。直接喜欢画面、联想到场景、分享假想使用感受、表达外观或操作偏好都可以成立；不要为了植入强加购买故事、教程追问或完整参数表。产品资料、原帖证据和 `training_fiction` 人物设定分开保存。
