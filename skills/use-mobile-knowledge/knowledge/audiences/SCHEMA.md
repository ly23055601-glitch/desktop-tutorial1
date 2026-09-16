# Mobile 角色与使用心理记录约定

`profiles.jsonl` 是本层唯一维护源；`guide.md` 由 `scripts/render_audiences.py` 的 `render()` 生成。本层与 `products/`、`compatibility/`、`scenarios/`、`sources/` 同处知识根目录，不依赖项目绝对路径。

## 范围与状态

每行一个可以相互重叠的任务角色，不是人口分类、性格分类或实测消费者分群。角色排序不表示占比、需求强度或商业价值。同一个人可以因任务、场地、同行者和时间进入不同角色。

所有角色固定 `kind=editorial_hypothesis`、`status=hypothesis_only`；`basis.type=editorial_reasoning`、`basis.empirical_evidence_refs=[]`。本版本只来自任务分析，没有真实访谈、社媒原话、样本统计或心理测评。不能用产品官方材料证明心理动机，也不能把分析写成“消费者普遍认为”。

所有口语片段固定 `content_mode=training_fiction`、`calibration_status=pending_calibration`、`user_endorsed=false`、`source_kind=synthetic_illustration`、`product_claims=[]`。片段只示范注意力与语言外显，不是成品评论、真实用户反馈或用户认可模板。脚本通过、助手自评通过都不改变这些状态。后续如有明确用户认可，另建有范围和依据的校准记录，不追溯性地把本页假想片段改成真实反馈。

## 必填字段

| 字段 | 类型与约定 |
| --- | --- |
| `id` | 稳定且唯一的 `MOBILE-AUD-001` 格式编号；删除后不复用 |
| `role` | 任务角色名称，不暗示年龄、性别、收入、诊断或固定人格 |
| `kind`、`status` | 固定为上述编辑假设状态 |
| `created_at` | 编辑记录建立日期；不代替产品实际核验日期 |
| `basis` | `type`、`note`、`empirical_evidence_refs`；明确编辑来源与无实证边界 |
| `task` | 当前想完成的具体拍摄任务，不夹带未经核验的实现方式 |
| `possible_motives` | 非空字符串数组；可能为什么在意，可以是兴趣、参与、学习等正向动机 |
| `psychological_tension` | 当前两种目标、节奏或负担如何取舍；不必以痛点或焦虑叙事 |
| `acceptable_operation_load` | `willing_to_do` 字符串数组、`threshold` 字符串；写可接受步骤及范围 |
| `abandon_or_switch_triggers` | 非空字符串数组；何时停止、暂缓、换机位、请人帮助或不用云台 |
| `alternative_explanations` | 至少一种不同解释；防止从身份或一个词推断唯一心理 |
| `selection_cues` | 可据当前任务材料判断适用性的线索；不是角色识别模型或心理测量题 |
| `natural_expression` | `attention_focus`、`expression_mechanism`、`avoid_patterns`、`illustrative_fragments` |
| `fact_ids` | 已存在且 `verified` 的产品事实编号数组；可为空但不可借用待核条目 |
| `compatibility_ids` | 已存在且 `verified` 的兼容编号数组；`support` 不得为 `unconfirmed` |
| `scenario_ids` | 已存在的场景编号数组；场景为 `editorial_synthesis`，不当官方事实依据 |
| `claim_guardrails` | 角色相关的不可外推提醒；不把未知改写成确定“不支持” |
| `model_scope_note` | 明确角色不限定型号，型号边界只来自被引用记录 |

`illustrative_fragments` 每条必含 `text`、`content_mode`、`calibration_status`、`user_endorsed`、`source_kind`、`persona_context`、`product_claims`、`note`。人物设定说明假想语境，不能冒充用户本人经历或真实原帖；本层片段不承载产品能力结论。要写具体产品使用效果，先走共享写手流程，另保存人物设定与对应事实条件。

## 四层区分

1. 场景需求：想保留哪个画面、过程或互动。
2. 心理动机：这件事对这个假想角色可能为什么重要。
3. 顾虑与操作负担：实际要做什么，何种情境下值得或不值得。
4. 自然说法：通过一个动作、位置、比较或注意力来表达；不让人物复述分析术语。

“麻烦”需要再拆为携带、步骤、反复确认、打断同行、错过片刻等线索。家庭拍摄不自动归因孤独；初学创作不自动归因流量焦虑；公开摆机位的迟疑不自动诊断社恐；同行节奏不同不自动套入伴侣冲突。没有这些心理叙事，同样可以有清晰需求。

固定机位、不拍、暂缓购买或继续用旧设备均是允许的结果。相关产品事实是辅助理解任务的材料，不是证明此人“应该购买”或“必然受益”的依据。

## 引用与代际边界

角色记录只维护事实编号和角色相关提醒，不另抄一套产品规格。渲染器从产品和兼容 JSONL 实时读取完整 `models`、`component`、`statement`、`conditions`、`limitations`、`source_refs`、`checked_at` 和状态；兼容记录同时展示设备、方法、功能及支持口径。阅读版末尾按编号去重生成这些内容，保留原始官方链接与章节定位。

引用前必须重新读取完整事实和当前官方依据。记录从 `verified` 变为 `pending/conflict` 后，渲染应失败并提示修复引用，而不是沿用旧阅读版肯定能力。附录重复展示不成为第二事实源；只修改 products/compatibility 的维护源后再生成。

每条引用代表自己的路径，不因同一角色引用了多个编号就证明可以合用。特别注意：

- Osmo Mobile 8 支持模块 2 的更新条件，不等于获得 8P 的触屏、框选或 FrameTap 整套联控能力。
- 手机投屏显示手机画面，模块预览显示模块镜头画面；10 米遥控与 25 米特定测试条件的 Wi-Fi 图传分开。
- 原生人物跟拍、DJI Mimo 智能跟随及追踪模块是不同路径；保留具体机型、系统、App、固件、连接与拆装要求。
- 儿童是人物场景，不是已核“儿童身份锁定”；能跟随不保证始终全身入镜或不换目标。
- 模块 2 的非人物画面占比、人物及手势距离和其他物体框选条件不可省略；不跨代扩大可跟随对象。
- 跟随、快门、取景、变焦和音频输入分别核对；能夹住、能连接不表示各 App 全部兼容。
- 模块 2 无线收音仍待核，不能用一代模块的接线收音路径补成已确认组合，也不能据此写成确定不支持。
- 三轴稳定不等于无限防抖或所有步行位移都被消除；固定支撑和防水条件不从角色设想推导。

## 按需读取与维护

先读 guide 的使用方式和角色索引，按当前任务选择相关 1—3 类；可用 `rg` 搜角色关键词或完整编号。只有当要使用某条产品能力时，才读关联事实和完整条件。无需每次读完全部 15 条与事实附录。

修改 profiles 后执行知识库维护命令 `maintain.py render`，其应从同一 scripts 目录导入并调用 `render_audiences.render()`。也可单独执行 `python3 scripts/render_audiences.py`。隔离校验支持 `--root <知识根目录> --audiences-dir <暂存角色目录>`，输出只在指定角色目录。

校验至少覆盖：编号唯一、必填字段、编辑与训练标签、空实证引用、事实与兼容引用存在且 verified、场景引用存在、示例不含产品能力结论、替代解释与操作负担非空。还需人工检查任务与引用的相关性、心理归因和代际边界；结构校验不能证明自然口语已获用户认可。

