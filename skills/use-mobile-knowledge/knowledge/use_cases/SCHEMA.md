# 详细使用场景记录格式

维护源为 `cards.jsonl`。它在七张概览场景和按型号卖点之下细化拍摄任务，不修改产品事实。每行一张完整卡，阅读页、目录与卖点反查表由 `scripts/use_cases.py render` 生成。

| 字段 | 用途 |
|---|---|
| `id`、`title`、`category`、`retrieval_tags` | 稳定编号 `MOBILE-USE-xxx`、具体任务标题、分类与关键词 |
| `models` | 每卡一个准确型号；相近型号需要另外说明其实际路径 |
| `audience_ids`、`selling_point_ids`、`scenario_ids` | 关联角色假设、型号卖点和已有概览；概览没有对应主题时可留空 |
| `kind`、`status`、`edited_at` | 固定为 `editorial_synthesis`、`hypothesis_only` 和实际编辑日期；不替代事实核验日期 |
| `moment`、`task`、`friction` | 具体发生时刻、要拍下的内容、拍摄中的难点 |
| `use_plan` | 已核能力可以怎样参与这次任务；不是对完整设备组合已经实测的声明 |
| `value_hypothesis` | 可能在意的用途或结果，不能写成普遍收益或量化改善 |
| `psychology.want/hesitation/tradeoff` | 可能想要什么、犹豫什么、愿意接受哪些操作；可有其他解释 |
| `writing_material.entry_angles` | 可供当次训练选择的关注点，属于分析，不是评论句式 |
| `writing_material.concrete_details` | 可选择的生活细节；只在当批人物设定中虚构，或由实际资料证实 |
| `writing_material.suitable_post_contexts` | 哪类话题可能引起此联想，均是假想筛选条件，不证明原帖含有该情节 |
| `writing_material.do_not_invent_as_post` | 不能由本场景反推到真实原帖的设备、动作、关系或结果 |
| `writing_material` 的状态 | `content_mode=training_fiction`、`calibration_status=pending_calibration`、`source_kind=synthetic_planning`、`user_endorsed=false` |
| `when_not_needed` | 当前任务何时不需要这项能力，或何时固定构图、已有器材更合适 |
| `conditions`、`avoid_claims` | 关键条件提示与不可推论；精确参数仍由事实记录唯一维护 |
| `fact_ids`、`compatibility_ids` | 只引用已核且匹配本卡型号的依据；命中后必须读取完整条件、来源定位和日期 |

同一张卡可以有多个表达方向，但这不是主评论数量配额，也不要求全部进入正文。人物经历在当批 `personas`，产品结论在 `product` 来源与 `product_fact`，真实原帖独立取证；此处不维护成品评论。

`scripts/maintain.py audit` 已接入结构、类型、编号、型号、状态、引用和本地链接检查。它不能判断场景是否有趣、心理是否被实际验证，也不能代替产品与选材语义复核。

检索命令会展开卡片直接引用以及相关卖点的事实和兼容记录，附上来源登记与该型号所有待核／冲突。将来已核事实变成待核或冲突时，应先撤下相应肯定能力或补证，不能通过删除限制使旧场景继续成立。

查询只审计命中卡及其依赖：受影响卡进入 `blocked`，显示问题和型号缺口，不返回其肯定用途；无关卡仍可正常读取。存在阻断项时命令退出码为1。全库 `audit/render` 继续严格检查全部记录。
