---
name: dji-nano-comment-adapter
version: CW5.4.2-portable
product_line: nano
description: Lightweight DJI Osmo Nano adapter for the shared consumer-comment training skill
---

# DJI Osmo Nano 产品适配入口

先读取包内共享写手规则：`../../../core/write-consumer-comments/SKILL.md`

本入口只补 Osmo Nano 的命名、佩戴和视角证据边界。评论是培训用假想消费者草稿，不用于发布；Pocket 的命名禁词不适用于本产品。

## 产品范围

- 目标为 DJI Osmo Nano，正文可用 `Nano`、`OsmoNano` 或 `DJIOsmoNano`
- 不把 Pocket、Action、360 或 Mobile 的云台、镜头、跟随、防水和续航能力移植到 Nano
- 佩戴方式、安装动作、第一视角、录制结果和耐候表现只按当前原帖或官方资料确认

## 事实资料接口

按当前任务填充 `facts.template.json`，每条能力保留适用组件、条件、来源和核验日期。功能、参数、固件、售价、配件和兼容性缺少证据时，只能写成兴趣或待确认问题；训练人物的使用感受不等于产品事实。

画面只能证明当前展示，不能自动外推普遍稳定性、画质、收音或耐候表现。抽帧不能代替未取得的完整叙事、对白或拍摄条件。

## 交给共享写手

整帖理解优先于某一帧。根据作者是在展示佩戴、记录第一视角、分享玩法还是求助，选择消费者真正想尝试的视角、佩戴习惯或操作感受。简短偏好可以停下，不强加完整户外故事或参数清单。
