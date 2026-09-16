---
name: dji-osmo360-comment-adapter
version: CW5.4.2-portable
product_line: osmo360
description: Lightweight DJI Osmo 360 adapter for the shared consumer-comment training skill
---

# DJI Osmo 360 产品适配入口

先读取包内共享写手规则：`../../../core/write-consumer-comments/MODULE.md`

本入口只补 Osmo 360 的代际、全景／平面和后期证据边界。评论是培训用假想消费者草稿，不用于发布；不继承 Pocket 的命名限制。

## 产品范围

- 目标为 DJI Osmo 360 系列，正文可用 `Osmo360`、`大疆360`，代际确认后再使用对应称呼
- 严格区分全景记录、平面重构、单镜头视频、原生帧率和软件插帧
- 不把 Action、Pocket、Nano 或竞品的画面结果强认作 360 的能力
- 两代产品、拍摄与导出、防水与水下成像必须分开核对

## 事实资料接口

按当前任务填充 `facts.template.json`，每条参数、模式、配件、拼接、隐形、增稳、夜景或水下断言保留型号、拍法／导出条件、来源和核验日期。总像素或全景分辨率不能单独推出裁切画质；成片不能反推机位、长杆或设置。

## 交给共享写手

先判断整帖是在展示全景玩法、记录运动过程、比较成片、分享导出还是求助，再选消费者真正想了解的视角、取景自由度、后期负担或使用取舍。能由一处结果引起兴趣，但不能只抓某一帧硬贴卖点；有话可聊再展开回复。
