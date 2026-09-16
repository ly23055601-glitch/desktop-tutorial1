> 跨项目查询：将命令中的 `<技能目录>` 替换为当前个人技能 MODULE.md 所在绝对目录；不从工作目录猜原项目路径。

# Pocket 统一知识库

重点Pocket4、Pocket4P。这里把产品、使用过程、真实表达、审美、比较、反馈和研究串起来；事实与语料仍各自保留来源，写法始终调用当前共享写手。

**当前问题 → 相关知识与原话 → 确认型号和证据边界 → 写作参考 → 需要写稿时进入共享写手。**

## 一次查相关资料

可以直接说：“调用op统一知识库，围绕这帖关心的问题给我写作参考。” 也可以在项目根目录运行：

```bash
python3 "<技能目录>/knowledge/scripts/pocket_library.py" brief '独自旅行 人像 跟随' --model pocket_4p
python3 "<技能目录>/knowledge/scripts/pocket_library.py" brief '同场景 不换 取舍' --model pocket_4p --competitor Pocket3
python3 "<技能目录>/knowledge/scripts/pocket_library.py" brief '挂绳 容量' --model pocket_4p --platform bilibili
```

简报合并原有事实/表达检索与卖点/详细场景检索，按当前问题附上有关的观感、反馈和上下文入口。只取相关结果，不要求每类都写进评论。原帖设备未明可省略型号；用户明确的目标型号不等于原片设备证据。单个事实、表达或场景需要更深核查时，继续沿命中ID和来源追溯。

## 能理解哪些问题

| 需要理解什么 | 资料 | 使用边界 |
|---|---|---|
| 产品到底能做什么、怎样操作 | [事实与流程](products/topic-coverage.md)、[两款比较](products/pocket4-vs-pocket4p.md) | 型号、条件、官方来源和实际核验日期一起读 |
| 为什么会关心这个能力 | [卖点价值](selling_points/guide.md)、[详细场景](use_cases/guide.md)、[真实需求](scenarios/README.md) | 官方事实、编辑解释、场景假设分别标注 |
| 使用者为什么在这里开口 | [表达与父句](voice/README.md)、[真实讨论](aesthetics/discussions.md) | 主评/父句按来源理解，个案不变成人群规律 |
| 喜欢什么画面、平时怎样用 | [观感材料](aesthetics/works.md)、[审美与习惯](aesthetics/preferences.md) | 有限抽帧、作者自述与完整视听不是同等证据 |
| 怎样比较，也保留其他选择 | [竞品与代际取舍](comparisons/README.md) | 保留不升级和支持其他设备的原话，不预设实测胜负 |
| 哪些要求和反馈已经明确 | [上下文](context/README.md)、[本人素材与反馈](feedback/README.md)、[原句对照](aesthetics/feedback.md) | 只沿用来源支持的作用范围，不把自评当认可 |
| 新材料从哪里来、怎样进入库 | [研究批次](research/README.md)、[研究入库](research/handoff.md) | 候选、已读证据、研究观察、正式入库与快照分开 |
| 实际有什么、还缺什么 | [动态覆盖](COVERAGE.md)、[待核问题](GAPS.md) | 数量由实际数据生成，未达目标不改成完成 |

## 接入执行能力

写评、改稿、培训案例使用[共享写手](../../write-consumer-comments/MODULE.md)和[Pocket边界](../../write-dji-pocket-comments/MODULE.md)。Apify 话题发现已按用户 2026-09-10 要求停用；已有研究材料继续保留。读取三平台链接使用[统一社媒读取](../../read-social-links-with-social-helper/MODULE.md)。已读入口不循环调用，知识库不重复维护采集、文风、数量或交付规则。

研究中保留正反意见；培训写作按任务目标与共享当前规则选材。独立训练人物与公共原话、本人经历分开保存。纯知识整理不计培训新稿，本次没有新建定时任务；另行授权的每日研究按自己的计划运行。

需要完整文件导航时读[完整索引](INDEX.md)。维护源为`knowledge/pocket/`；个人技能是显式刷新并验证的快照，项目外查询不依赖原项目目录。证据档案和历史验收保留用于追溯，含留出材料的验收稿不作为写手学习范文。
