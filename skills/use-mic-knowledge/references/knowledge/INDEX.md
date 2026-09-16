# DJI Mic 官方产品知识库

本库是供任意项目调用的 Mic 产品核验与评论培训资料快照。重点型号是 **DJI Mic 3、DJI Mic Mini 2S**；初代 DJI Mic、Mic 2、Mic Mini、Mic Mini 2 提供基础对照。官方事实、连接条件与编辑场景各自保留来源；首版未含消费者语料；后续真实材料单独收录于[材料盘点](materials/STATUS.md)，不回填为官方事实。

## 从一个具体问题开始

以下命令在技能目录运行，也可将脚本改为绝对路径从任意目录调用：

```bash
python3 references/knowledge/scripts/mic_knowledge.py search '手机口播怎么接收音' --model mic_mini_2s
python3 references/knowledge/scripts/mic_knowledge.py search '四个人接相机能分开声道吗' --model mic_3
python3 references/knowledge/scripts/mic_knowledge.py search '不可重录时怎样备份和导出' --model mic_3 --format json
python3 references/knowledge/scripts/mic_knowledge.py audit
```

脚本从自身位置定位知识库，不依赖当前工作目录；也可用绝对脚本路径运行。`--limit` 控制每类最多返回条数，默认 3。`--model` 可用上述规范 ID 或明确名称，如 `DJI Mic Mini 2S`（名称含空格需加引号）。`Mini`、`Mini 2S` 等与无人机混淆的称呼不会作为型号筛选；初代明确使用 `mic` 或 `DJI Mic 初代`。未指定或识别出明确型号时检索全系列，每条结果分别注明归属，不将多款能力合并成“一款”。

未传 `--model` 时，问题中明确的完整型号会自动限定检索；同时明确两款时只检索这两款。显式 `--model` 优先。问题未给出明确型号时才检索全系列；型号或品牌词本身不作为内容相关性的依据。

结果包含事实、连接兼容、场景及其证据。已核验表示在所列日期读过对应来源；不能当成今天已核验。相关待核／冲突单独展示，不进入肯定答案；确实查不到时保留缺口。

## 阅读入口

| 想了解什么 | 入口 |
|---|---|
| Mic 3 能力、操作及限制 | [Mic 3](products/mic_3.md) |
| Mic Mini 2S 能力、操作及限制 | [Mic Mini 2S](products/mic_mini_2s.md) |
| 其余四款的基础区别 | [基础型号](products/basic.md) |
| 六类典型用途 | [场景问答](scenarios/guide.md) |
| 功能怎样转为有条件的用途价值 | [卖点指南](selling_points/guide.md)（关联事实与角色） |
| 相同能力的不同用途、偏好和使用阶段 | [需求与价值发散](selling_points/value-expansion.md)、[卖点反查场景](writing_scenarios/selling-point-map.md) |
| 细化场景、角色关注与后续培训选材 | [详细场景指南](writing_scenarios/guide.md)（编辑推演） |
| 实际声音、录制过程、原话与真实讨论材料 | [体验材料指南](training/experience-materials.md)、[当前盘点](materials/STATUS.md)、[真实讨论与选材](materials/discussion-context.md)、[录制过程](materials/recording-process.md)（原话、编辑解释与未听音范围分别保留） |
| 有条件的采访与外拍作者记录 | [field-tests](materials/field-tests.md)（Mic、Mic 2、Mic Mini、Mic 3、Mic Mini 2S，作者条件与待补作品） |
| 原作者的具体录制选择与公开音频样本 | [公开作者材料](materials/published-experience.md)（7篇文字、1份未听样本、[步行作品](materials/walking-vlog.md)与[两份采访](materials/interview-pair.md)链接） |
| 潜在人群、角色动机与心理表达 | [角色心理指南](audience/guide.md)（编辑假设，待校准） |
| 已覆盖内容与真实数量 | [覆盖清单](COVERAGE.md) |
| 资料冲突与未确认内容 | [缺口清单](GAPS.md) |
| 官方资料与证据定位 | [来源目录](sources/README.md) |
| 本库怎样更新 | [维护说明](MAINTENANCE.md) |
| 检索和事实抽查结果 | [验收记录](evaluation/acceptance.md) |

## 在写作中使用

从[共享消费者写作](../../../write-consumer-comments/SKILL.md)进入共享写作能力库。先确定当前帖子或训练命题中的问题，再检索相关的少量事实，不要求评论为了使用知识库而讲参数。

- 写入产品断言时保留知识编号、精确部件、连接方式与适用条件，复核当前官方来源；按共享训练契约绑定 `product` 来源和 `product_fact` 断言。知识编号不替代核验，也不是旧真实性审查的 claim 注册号。
- 发射器内录、接收器输出、手机／相机保存的声音和平台成片分别核对。产品支持某能力，不能证明某个原帖用了该能力或因此获得某种听感。
- 区分标准接收器、手机版接收器、蓝牙直连与 OsmoAudio；不能把某一种连接的功能推给其他连接。
- 真实来源和官方参数保留原有性质。场景问答是编辑归纳；培训人物和假想体验单独保存在当次写作任务中，不写入本库。

## 文件与接口

`products/models.jsonl` 保存六款型号目录，`products/*.facts.jsonl` 保存事实，`compatibility/*.jsonl` 保存有方向的兼容关系，`sources/*.jsonl` 登记官方来源，`scenarios/cards.jsonl` 保存编辑场景。记录字段和状态见 [SCHEMA.md](SCHEMA.md)。

检索为只读、无网络命令；JSON 输出有 `query`、`model`、`selected_models`、`results`（facts/compatibility/scenarios）、`unresolved` 和 `message`，各结果展开来源与定位。审计输出结构错误、覆盖情况和待核清单；正常退出码为 0，结构错误为 1，参数错误为 2。

`audience/cards.jsonl` 单独保存潜在角色、动机、行为线索、表达方向和反例，全部为待验证编辑假设，不含真实调研结论。个人技能 `$use-mic-knowledge` 提供跨项目的产品检索与 `audience` 检索；本包更新与迁移见[封装说明](../package.md)，不后台同步。

`selling_points/` 保存按型号组织的卖点与来源复核记录，回答“这项能力在什么情境下有用”；用途价值和角色适配是编辑归纳。运行 `python3 references/knowledge/scripts/mic_selling_points.py '四人采访备份' --model mic_mini_2s` 或个人技能的 `selling-points` 命令，结果同时显示依据、条件、限制、原事实核验日与卖点复核日。无法核实的依据会使相关卖点进入待核结果，不借其他型号补齐。

`writing_scenarios/` 从具体拍摄与协作时刻展开任务、心理假设、原帖待观察线索、分型号路线及多个选材方向；与 `scenarios/` 的十二类技术操作问答分别维护。个人技能用 `scenes` 检索，维护源可运行 `python3 references/knowledge/scripts/mic_writing_scenarios.py '异地播客录音' --model mic_3`。场景不是已采集的真实素材，也不是可直接套用的评论稿。

已有明确卖点可用 `scenes --selling-point MIC3-SP003` 反查相关场景；可与中文问题、型号和类别筛选组合，取交集。需求解读提供选择角度，真实声音、使用者原话和完整讨论仍按材料区的实际采集范围判断。
