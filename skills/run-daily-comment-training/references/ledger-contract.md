# 每日台账与 KPI 契约

台账只保存调用、计量与产物定位；正文、共享训练状态、采集证据、内容判断和修改说明分别保留。脚本只校验结构、引用文件存在和计量关系，不能证明证据真实、语义合格、反馈确属用户或首稿文件从未被改写。

质量目标与当前写手的教学完整交付条件见[最新 KPI 口径](kpi-standard.md)。本契约的 `draft_completion` 仅计稿件实交；它和复核覆盖标记均不代表当前写手要求达标。教学完整结论引用实际表达版本、结构报告和语义审查，另记于批次 KPI 日报；当前 CW5.4.2 继续采用 cw5 结构 profile，横测链接另核实际对照关系、比较轴、目标产品种草方向和消费者立场，仍须另核其表达、选材和整楼讨论判断。旧版结果保留原范围，不回写首稿。

## 目录、身份与续接

正式根目录为项目 `outputs/daily-comment-training/`，账本固定为 `YYYY-MM-DD/B001/ledger.json`。`B` 是一次请求的完整接单批次，不是 10 链接输出组或采集批次。日期取批次真实开始时间的上海日期；批次号同日递增。复制[空批次模板](../assets/batch-ledger.template.json)后填真实日期和开始时间，不把占位模板、模拟数据或测试批次放入正式根目录。

- `material_id` 是稳定原帖／材料身份，例如 `douyin:真实作品ID`；短链、长链、带参数链接解析到同一作品后使用同一身份。无法确认同源时保留暂定身份，证据确认后统一修正引用，不能仅因标题相似合并。用户直接材料使用稳定材料编号。
- 单位是当天的 `product_code + material_id`；同一天在所有批次中只定义一次 `tasks`。同作品分属 `op`、`dm` 是两个任务，读取分母仍是一份作品。
- `task_ref` 固定为 `YYYY-MM-DD/B001/T001`。`inputs` 保留每次收到的原序号、产品与材料身份并映射到该引用；同日重发、跨批次重发不重复定义任务。无用户序号时按收到顺序分配字符串序号。重复原序号可同时存在，数组顺序保留到达次序。
- 新链接／材料请求新批次，完整输入保存在该批次 `inputs`；混合“重发＋新增”时重发输入指向原任务，新材料才进新批次 `tasks`。全部重发可以只有输入映射、没有新任务，仍分组返回引用但不增加执行日。同日同产品同材料另写方案也作为原任务新版本；纯修订／反馈更新原批次 `revisions` 和反馈记录，不新建批次／任务／日期。新日独立新写作请求可定义当天新任务；只改旧稿不生成新执行日。
- 一个任务对应自己的稿件和共享训练 state；同作品跨产品写作可共享采集证据，但拆开任务文件，避免同一个 state 出现重复真实作品 ID。不要伪造作品 ID 来绕过共享写手检查。
- `draft_ref`、`training_state_ref`、`evidence_ref`、审查引用为相对所在账本目录的文件路径或绝对文件路径。训练 state 完全复用共享写手当前模板及 SHA256 绑定，不在此定义另一套状态或固定旧版写作流程。

## 10 链接输出组与版本记录

`schema_version: 1` 和任务／来源计量不变。只读工具从每个接单批次的 `inputs` 按数组位置派生输出组：每 10 个位置一组，尾组保留余数。0 个输入无组；1、10、11、23 个输入分别为 `1`、`10`、`10＋1`、`10＋10＋3`。失败和重复输入也保留位置，不按产品或平台重排、不删去再补位。采集仍按统一读取技能对完整集合执行，其平台批次与输出组大小无关。

分组结果在报告顶层 `output_groups`，每项包含：

- `group_ref`：例如 `2026-09-07/B001/G001`；每个新 B 从 G001 开始，后来请求不回填已交付尾组。
- `input_start/input_end/input_count`：本批次数组的 1 起位置范围与条目数，位置不同于用户可能重复的原编号。
- `items`：每项含 `position/original_index/product_code/material_id/task_ref/task_status`；实交任务另带当前版本 `draft_ref` 绝对路径。同一天已出现的任务可带 `first_occurrence: {group_ref, position}`，用于重复引用说明。

组文件 `B001/G001.md` 等汇编各任务当前终稿及受限／重复说明，保留产品线与原序号。分组不复制或重定义任务，不合并共享 state，不新增产量。首次输入即使跨产品同链接，按各自输入位置输出产品专属任务；相同任务重复出现则指向已有结果，不虚报新写稿。

每日首批和新执行对话按入口核对两项规则来源任务及其当前技能；接单目录另存 `runtime-sources.md`，记录实际核对时间、任务 ID、可读的最新完成轮次或限制、技能与所用参考路径、实际版本与 SHA256。组边界发生规则更新时追加该组采用版本；这份说明不属于训练 state，不参与 KPI，也不是新增执行日。不能保存一个固定 CW 版本号后当作往后每日的“最新版本”。

## `ledger.json` 字段

顶层必填 `schema_version: 1`、`date`、`batch_id`、`started_at`、`inputs`、`sources`、`tasks`；`external_blocks` 默认为空数组。时间使用真实带时区 ISO 字符串，例如 `2026-09-07T10:00:00+08:00`。不得用示例时间冒充实际记录。

输入映射格式：

```json
{"original_index":"1","product_code":"op","material_id":"douyin:123","task_ref":"2026-09-07/B001/T001"}
```

来源格式（这里只演示字段，不是实际证据）：

```json
{
  "material_id": "douyin:123",
  "url": "原始链接，仅存原始台账，统计不输出",
  "read_required": true,
  "status": "pending",
  "evidence_ref": null,
  "verified_at": null,
  "reason": null,
  "attempts_ref": null,
  "raw_evidence_ref": null,
  "reconciled_at": null
}
```

`raw_evidence_ref` 指向批次 `evidence/` 中固定落盘的 evidence pack 或媒体文件，`attempts_ref` 指向统一采集技能的实际首采／人工交接记录，`reconciled_at` 是输入位置、别名和作品 ID 完成对账的时间。Chrome Downloads、临时浏览器路径或只有“任务完成”文字不能作为可复现证据引用。

- `read_required: true` 的 `status` 为 `pending`、`blocked`、`qualified` 或 `reused`。后两项须有实际合格证据文件 `evidence_ref` 及实际核验时间 `verified_at`；复用时沿用原核验时间，不能填今天假装重读。是否能复用、证据是否合格由统一读取流程和当次材料判断。
- 失败用 `blocked` 并填具体 `reason`，没有合格证据不能记成功。重复作品在同日不同批次出现，按稳定身份去重，保留原问题状态和人工交接记录，不因重发自动重采。人工后续提供充分材料时按下方 `provided` 规则另登记，保留原读取失败。
- 这里的状态仅是 KPI 映射。统一读取技能的原始证据包、账本、原始 `failed/blocked/pending` 与尝试次数须另存，不被本账本合并后的 `blocked` 覆盖；在 `reason/evidence_ref` 或批次说明定位原记录。问题项依统一读取技能交人工，KPI 状态不构成自动重试、补读或重采授权。
- 用户已给足材料且明确无需实时读取，用 `read_required: false, status: "provided"`，`evidence_ref` 指向用户材料。它参与写作任务分母，不参与链接读取分母。
- 不同产品可以引用同一份来源。任务必须能在同日账本中找到来源记录；新日复用也登记 `reused`。多日基线读取率合并每日分子分母，同作品在独立新日的读取／复用请求可再次计一次；这不是宣称进行了重复联网采集。
- 原始链接必要的敏感参数仅留原始来源记录和受控证据文件，不复制到统计正文、汇总 JSON 或反馈定位。

任务初始格式：

```json
{
  "id": "T001",
  "product_code": "op",
  "material_id": "douyin:123",
  "status": "pending",
  "conclusion": null,
  "first_delivery": null,
  "revisions": [],
  "user_feedback": [],
  "hard_errors": []
}
```

- `status` 为 `pending`、`blocked`、`concluded` 或 `delivered`；`blocked/concluded` 必须有具体 `conclusion`。`concluded` 指已明确解释结果但未交稿，例如不适用；不能用空泛“已处理”冒充闭环。
- 实际交付后才填 `first_delivery` 并设 `delivered`。已交付任务即使有修订要求仍保留交付事实，不能撤回首稿改记未交付。
- 实交任务必须能在其所属日期找到同 `material_id` 的可用原帖／材料依据：至少一项 `qualified/reused/provided` 来源及其实际证据文件。只有 `blocked/pending` 时，脚本拒绝将任务登记为实交，不增加完成分子。若读链失败但用户另给了充分材料，保留失败的 `read_required: true` 记录，再以相同材料身份登记 `read_required: false, status: provided` 的替代材料；可正常交付，读取率仍按失败计。来源存在不代表内容足够，是否能支持正文仍须按共享写手语义核验。
- `first_delivery` 首交快照一经记录不覆写；首稿文件、训练 state、检查记录同样保留。新版追加到 `revisions`，使用不同版本路径。脚本拒绝同任务跨版本复用解析后的稿件或 state 路径，包括符号链接别名；这不能证明文件内容在历史上未被篡改。修复旧记录确有录入错误时另存更正说明和原值，不以改稿结果重算首稿。

交付快照字段：

```json
{
  "delivered_at": "真实交付时间，带时区",
  "draft_ref": "T001/v1/comments.md",
  "training_state_ref": "T001/v1/training-state.json",
  "main_comments": 3,
  "replies": 2,
  "review": {
    "facts": true,
    "naturalness": true,
    "product_interest": true,
    "difference": true,
    "post_understanding": true,
    "evidence_sufficiency": true,
    "discussion_value": true,
    "comparison_evidence": null,
    "self_check_ref": "T001/v1/review.md"
  },
  "independent_review_ref": null,
  "knowledge_handoff_ref": "T001/v1/knowledge-handoff.json",
  "delivery_manifest_ref": "../delivery-manifest.json"
}
```

`review` 是当前版本有实际语义判断记录的逐项矩阵；缺项或 `false` 不计完整复核。`comparison_evidence` 仅在 CW5.4 横测触发时为布尔值，普通帖子填 `null`。共享脚本检查通过不能直接填任何语义项为 `true`。`self_check_ref` 指向具体检查、问题及修正说明；独立审稿另存 `independent_review_ref`，没有独立审稿就留空。产品兴趣指具体兴趣切口检查，不强求每条写型号或按回复数量加分。

批次目录还必须有 `delivery-manifest.json`：逐 `input_position` 对应 `task_ref`、`evidence_ref`、`knowledge_handoff_ref`、`draft_ref`、`training_state_ref`、`review_ref`、采用版本／SHA256、`status` 和限制，并列出 `missing_refs`。交付前 manifest 的输入位置必须与 `output_groups` 完整相等；差异项只能标 `blocked` 或 `pending`，不能从组文件中删除。

每个 `revisions` 元素沿用交付快照字段，另加 `feedback_ids: []`，有用户反馈驱动的修订引用相应反馈 ID。一次整组修订交付为一轮；助手内部自改不虚计用户返工。同一轮多个反馈仍计一轮。当前主评／回复库存取最新版；累计新增产量始终取首交，不把新版新增回复记成新任务产量。

## training_cw5 质检引用

文案质检是独立于共享 `training-state` 的附加层。它不改变 `draft_completion`、原有 `review` 矩阵或结构检查器的含义。交付任务可在当前版本快照中追加以下字段：

```json
{
  "quality_review_ref": "T001/v1/quality-review.json",
  "quality_score": 92,
  "quality_decision": "retain",
  "quality_issue_codes": [],
  "quality_coverage": "deep",
  "revision_count": 0
}
```

`quality_coverage` 取 `basic`、`deep` 或 `risk_deep`。全量基础记录不等于独立深度审稿；批次汇总必须同时报告深度覆盖率与未深审数量。`quality_review_ref` 必须绑定当前 `draft_ref` 和 `draft_sha256`，改稿后新增质检文件，不覆盖首稿结论。

质检结果使用 `training_cw5` profile，采用硬错误封顶加百分制分级。它只用于交付门禁、训练反馈和任务分工，不直接写入绩效结论。问题必须保留 `issue_id`、问题码、严重度、评论定位、证据引用、修改动作和复检状态；合规的培训假想经历不属于产品事实硬错误。

批次可在顶层 `quality` 中追加 `profile`、`summary_ref`、`deep_review_coverage` 和 `unreviewed_count`。缺少质检文件只能标记未质检或受限，不能由结构检查通过推定语义质量通过。

## 用户反馈、错误与时间

用户反馈只在实际消息明确到具体任务时追加；批量明确认可可展开到被点名任务，模糊指代不能自行扩展。字段：

```json
{"id":"F001","at":"真实反馈时间，带时区","target":"first_draft","outcome":"changes_requested","source_ref":"用户消息定位或保存原话的文件路径","note":"用户具体反馈及适用范围"}
```

`target` 为 `first_draft/revision`；后者加 `revision_number`（`revisions` 的 1 起序号）。`outcome` 为 `accepted/changes_requested/reviewed`；`reviewed` 仅表示用户已明确审阅但未给认可／修改结论。未反馈用空数组，状态为待验收。不要把助手自检、独立审稿或猜测写入这里。

首稿审阅分母为有 `first_draft` 反馈事件的任务；首稿直接认可看首个明确决定（跳过仅 `reviewed` 的中性事件）是否 `accepted`，且此前没有改稿交付。首个决定是 `changes_requested` 后，后续认可只针对修改版本，不能改成首稿通过。事件追加保留原决定；脚本不具备审计文件历史的能力。

硬错误仅记录产品型号／能力错误、编造原帖内容、来源归属错误：

```json
{"id":"E001","detected_at":"真实时间，带时区","kind":"product_fact","stage":"internal","detail":"具体错误及位置","resolved_at":null}
```

`kind` 为 `product_fact/post_fabrication/source_attribution`；`stage` 为 `internal/delivered`，区分内部发现和已交付问题。修复只补真实 `resolved_at`，不删除日志；合规的假想人物经历不算硬错误。自然度等一般问题放语义审查记录，避免混入硬错误数。

`external_blocks` 记录真实区间 `{ "started_at": "…", "ended_at": null, "reason": "…" }`。结束后填真实结束时间；不能从总耗时推测外部阻塞。批次首交取其所有任务最早首交时间，总墙钟为首交减批次开始；无首交为 `null`。已结束阻塞区间合并重叠后单列，没有已结束记录为 `null`，未结束只计项数。不从墙钟扣除，不将差值称为助手执行时间。

## 只读汇总与日收尾

在项目根目录运行：

```sh
python3 .agents/skills/run-daily-comment-training/scripts/daily_kpi.py outputs/daily-comment-training
python3 .agents/skills/run-daily-comment-training/scripts/daily_kpi.py outputs/daily-comment-training --date 2026-09-07 --json
```

- CLI 不写任何文件；缺失根目录、空目录、无任务空批次均不算执行日。数据错误以非零退出并指出问题，不跳过损坏台账给出漂亮指标。测试必须在临时目录或技能 `tests` 中，不能污染真实基线。
- 默认最新实际执行日；`--date` 选择该日任务群，读取账本**当前**状态，包含后续已登记反馈，不是还原该日历史快照。最近 7 日／基线的日期集合限制为选择日期及之前的实际执行日。
- JSON 的 `daily` 为当日指标；`first_seven_baseline` 为首 7 个实际执行日加权合计及是否满 7 日，满 7 日提示人工据实际结果提目标，不自动设置验收率或分钟阈值；`recent_execution_days` 提供近 7 日目录、首稿与改稿路径、明确用户反馈，供新对话读取材料；`output_groups` 为所选日期各接单批次的 10 链接输出清单。
- 当天仅有重发输入而没有新任务时，不新增执行日；使用 `--date` 显式选当日仍可取得引用输出组，不能仅因默认日期指向最近真实执行日就漏掉当日的重发请求。工具只提供分组规划，需按清单生成实际组文件并核对终稿内容后才算输出完成。
- 比率统一 `{numerator, denominator, value}`，`value` 为 0–1；分母为零是 `null`，文本显示“暂无数据”。`input_closure` 是有实交／明确结论／明确阻塞的任务占比；`draft_completion` 只算实交，材料不足仍在任务分母。`reading_success` 按需读取作品去重。
- `semantic_review_coverage` 和 `independent_review_coverage` 取每个任务当前交付版本；新版没复核不能借首稿通过。`first_draft_acceptance`、`first_draft_review_coverage` 分别是首稿认可率与用户首稿审阅覆盖率；`production` 是冻结首交产量，`current_production` 是当前库存，后者不能累加算新增。
- `current_user_acceptance` 单列当前版本已认可、要求修改、已审阅待结论、待验收任务数；只看当前版本对应的用户反馈，新版不能沿用旧版认可。它不替代或倒改首稿验收 KPI。
- 每日正文展示输入／完成数、主评／回复数、阻塞、自检问题、用户验收、总墙钟与已记录外部阻塞、返工轮次；脚本不读审稿正文，需另读 `self_check_ref` 补充具体自检问题。基线不把助手自评当用户验收；近期仅有修订的旧批次从原任务路径续接，不新增执行日。
