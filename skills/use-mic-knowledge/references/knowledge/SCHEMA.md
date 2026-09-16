# Mic 知识记录约定

本库用 UTF-8 JSONL 保存逐条记录，用 Markdown 提供阅读入口。结构化记录是事实维护源；阅读文档引用记录编号，不另存一套参数。

## 文件与型号

- `products/models.jsonl`：型号目录。
- `products/*.facts.jsonl`：产品事实（按资料负责范围分文件）。
- `sources/*.jsonl`：官方来源登记。
- `compatibility/*.jsonl`：有方向的连接及配件兼容记录。
- `scenarios/cards.jsonl`：有事实依据的编辑场景问答。
- `evaluation/cases.jsonl`：检索验收问题。

型号 ID：`mic`（初代）、`mic_2`、`mic_3`、`mic_mini`、`mic_mini_2`、`mic_mini_2s`。不能将裸“Mic”“Mini”“Mini 2S”自动确认为具体麦克风型号；型号筛选使用完整名称或规范 ID。

## 官方来源

必填：`id`、`title`、`url`、`source_type`（specs/faq/manual/compatibility/firmware/store/support/index）、`region`、`language`、`checked_at`（实际读取日，YYYY-MM-DD）、`read_scope`（实际读取部分）、`summary`（自主归纳）。

可选：`document_version`、`published_at`（来源未标则 null）、`local_path`（库内相对路径的已保存证据）。来源 URL 只允许大疆官方域名或官方文档 CDN；不能将下载列表存在文档等同已读该文档。引用定位应精确到页码、表格行或问题标题；不复制整页原文到知识卡。

## 产品事实

必填：`id`、`models`（型号 ID 列表）、`component`（具体部件／套装）、`topic`、`statement`、`conditions`（数组）、`limitations`（数组）、`source_refs`（`[{"source_id":"…","locator":"页码／小节／表行"}]`）、`checked_at`、`status`。

主题：`identity`、`wearing`、`audio`、`recording`、`channels`、`transmission`、`power`、`connections`、`controls`、`export`、`firmware`、`kits`。

状态：`verified`（按日期核实）、`pending`（资料未确认）、`conflict`（来源冲突）。待核或冲突必须给出 `gap_reason`，并保留可用来源。`verified` 必须有已读官方来源与定位。没有证据不能写成“明确不支持”。`keywords` 可补检索用语，不构成事实。

## 兼容记录

共有字段：`id`、`models`、`component`、`statement`、`conditions`、`limitations`、`source_refs`、`checked_at`、`status`。

专有字段：`transmitter_model`、`receiver_model`（没有接收器时填 null）、`host`、`method`、`support`（`supported`/`not_supported`/`conditional`/`unconfirmed`）、`features`（数组）。型号端点可使用准确配件或宿主名称；`models` 仅用上述六个库内型号 ID。矩阵行有方向，不能自动对称或传递；`verified` 不能配 `unconfirmed`。

## 型号目录

`id`、`official_name`、`aliases`（无歧义名称）、`priority`（primary/basic）、`components`（部件名称数组）、`fact_ids`、`source_refs`。

## 场景卡

`id`、`models`、`scenario`、`question`、`task`、`steps`（数组）、`answer`、`limitations`（数组）、`fact_ids`、`compatibility_ids`、`kind` 固定为 `editorial_synthesis`、`keywords`。每条操作／能力解释须能回到所引事实，不能把编辑场景当成真实消费者体验。

## 检索与审计

`search` 返回相关事实、兼容记录和场景卡，以及展开后的来源。默认排除 pending/conflict，但单独报告相关待核事项，避免把它们当作答案。查询无相关资料时返回空结果与明确提示；不以其他型号补答案。`audit` 区分结构错误与资料缺口；结构校验不证明事实正确，也不证明网页今日仍可访问。

## 独立角色假设层

`audience/cards.jsonl`：`id`（MIC-A001 等）、`role`、`aliases`、`tags`、`trigger`、`motives`、`tensions`、`behavior_signals`、`expression_directions`、`counterexamples`、`scenario_ids`。除 ID、角色名与情境外以上字段为字符串数组。

固定性质：`status=editorial_hypothesis`、`evidence_status=not_user_research`、`origin=assistant_synthesis_from_thread_discussion`、`review_status=pending_user_calibration`。没有官方核验日期或已核验标记。`scenario_ids` 只定位待另行核对的产品使用场景，不是心理证据。假设由个人技能的 `audience` 命令独立检索，不混入产品 `search` 的已核验结果。

## 卖点层

`selling_points/basic.jsonl`、`mic_3.jsonl`、`mic_mini_2s.jsonl`：`id`、`models`、`component`、`title`、`fact_ids`、`audience_ids`、`trigger`、`user_value`、`conditions`、`limitations`、`expression_angles`、`review_ids`、`keywords`，`kind` 固定 `editorial_synthesis`。型号、引用和条件／限制／表达方向／关键词为非空字符串数组，其余为非空字符串。

`fact_ids` 可引用同型号的已核验产品事实或兼容记录，不能把待核功能转成卖点保证；`audience_ids` 仅说明编辑匹配，不证明某人群偏好。每条依据须由相应 `review_ids` 复核覆盖。`user_value` 是用途价值推导，不能当作官方事实或真实体验。

`selling_points/reviews_*.jsonl`：`id`、`source_id`、实际读取的官方 `url`、`locator`、实际 `checked_at`、`fact_ids`（数组）、`result`（consistent/unresolved）、`note`。复核 ID 与产品来源 ID 分开；来源必须已登记于所引事实。复核日只适用于明确读取的部分，不改写全库历史日期。引用未核验、跨型号或缺少一致复核的卖点单列 `unresolved`。

## 详细场景与培训选材层

`writing_scenarios/creator_learning.jsonl`、`people_memories.jsonl`、`business_team.jsonl`：每卡含 `id`（MIC-WS001 等）、`title`、`family`、`scene_moment`、`user_task`、`audience_ids`、`motives`、`tensions`、`post_cues`、`routes`、`angles`、`non_fit`、`variation_axes`、`keywords`。角色、动机、取舍、原帖线索、变化轴、关键词是非空字符串数组，其余普通字段为非空字符串。

`routes` 是非空对象数组，每条含 `model`、`selling_point_ids`、`setup`、`conditions`、`limitations`；型号与设置思路为字符串，其余为非空字符串数组。一个型号在同卡只保留一条候选路线，同一场景可以含多个型号路线，检索时分别筛选。每个卖点必须属于路线的精确型号，引用可追到原事实与复核；某路线依据失效只使该路线进入待核，不能从另一型号借能力补齐。

`angles` 是 `{focus, detail}` 非空对象数组，用于提供不同关注点，不是固定评论槽位。`kind=editorial_synthesis`、`psychology_status=editorial_hypothesis`、`review_status=pending_user_calibration` 固定标记内容性质。`post_cues` 只是可观察线索，不能冒充已读帖子；`scene_moment` 是泛化情境，具体假想人物和经历仍存写作任务。候选路线有事实支撑不等于具体设备组合已经实测或全部兼容。

`scenes --selling-point ID` 按路线中已存在的 `selling_point_ids` 反查；与型号、类别及文字问题取交集，不增加跨型号关联。JSON 新增 `selling_point` 字段（未指定为 null）。未知卖点编号报参数错误；型号和卖点不相交时返回空结果；依据待核的匹配路线保留在 `unresolved`。

`writing_scenarios/selling-point-map.md` 由场景路线自动生成；`selling_points/value-expansion.md` 是人类阅读的用途解读，链接回卖点与场景，不另存参数。两者不能作为已采集原帖、真实心理或使用效果的依据。
