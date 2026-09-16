# 本轮公开语料来源与读取记录

主要讨论对象为 Pocket4 / Pocket4P。旧轮用户已要求现有材料足够、停止扩量；旧轮采集已结束，原150篇/30篇规模仅保留为历史计划。候选、已读作品、入库评论与未整理附件分别保存。

## 各文件的责任

| 文件或目录 | 记录什么 |
|---|---|
| `discovery/` | 候选发现出处与标题线索；搜索结果不算读过原帖 |
| `input-ledger.jsonl` | 原序号、平台、作品身份、冻结分组、提交次数、实际处理次数及逐项证据 |
| `run-state.json` | 本轮完整输入集合、批次、队列、原始导出位置与未完成项 |
| `raw/` | 社媒助手实际导出的原始 Excel；保留完整字段与 SHA256，不覆盖或手改 |
| `normalized/` | 整文件解析结果、原行/原列定位及逐输入核对报告；`parsed`不等于`success` |
| `works.jsonl` | 汇总实际作品状态、作者 ID、讨论主型号、来源、读取范围与限制 |
| `comments.jsonl` | 已核对入库的实际评论、直接父句关系及每次导出的来源定位 |
| `analysis/` | 仅训练作品的需求和表达分析；记录话语主体及具体来源 |
| `prior-exposure-audit.json` | 与已扫描历史文件的作品 ID 重叠检查；不证明从未在其他地方见过 |

XHS提交链接中的校验查询值只用于读取；展示与检索使用不带查询值的规范链接。原始导出本地保留，不能把其中的请求令牌复制到交付正文。

## 状态与计数

提交队列不代表每一项都已尝试；`submission_counts` 与 `attempts` 分开。只有核对实际导出或明确失败结果后才更新处理次数。界面显示完成不直接证明每篇内容可用。

作品信息、评论内容、媒体读取分别记录范围。没有读图或连续视频时不描述画面、动作、口播、机身标识或设备UI。作品主型号是讨论对象；标题/作者声明只提供 M1 证据，不证明实际拍摄设备。对比帖可保留多个提及型号，主型号需从具体文字判断。

每平台按作者 ID 去重，每个账号最多两篇计入目标；昵称不能代替账号身份。图片空评论和缺父句回复保留限制，不补文字或关系。完整父句讨论计数只来自真实评论，不把作品正文当作评论。

## 离线解析实际导出

完成统一技能采集及导出后运行；本脚本不执行网络读取，不调整节流或重试：

```bash
/Users/luocaihua/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  knowledge/pocket/scripts/ingest_social_exports.py \
  --platform xiaohongshu --kind posts \
  --source knowledge/pocket/corpus/raw/xiaohongshu-posts-01.xlsx \
  --ledger knowledge/pocket/corpus/input-ledger.jsonl \
  --output knowledge/pocket/corpus/normalized/xiaohongshu-posts-01.jsonl
```

解析器使用 openpyxl 完整读取每张表和所有非空行，保留精度风险、空文、未匹配身份及分组；摘要不输出留出正文。参数 `--mapping` 只能映射实际观察到的表头。不能从解析器成功推导采集或研究验收成功。

## 评论批次对账

评论导出也先用上面的解析器，选择 `--kind comments`。随后按已登记的批次边界预览入库结果：

```bash
python3 knowledge/pocket/scripts/reconcile_comment_batch.py \
  --batch-id xiaohongshu-comments-01 \
  --normalized knowledge/pocket/corpus/normalized/xiaohongshu-comments-01.jsonl
```

默认仅输出聚合与逐帖元数据，不修改资料。只有实际界面已终止、原始文件已导出，且该批状态已依据这些证据记为 `comments_exported_pending_reconciliation`，才能加 `--apply`。这项操作核对实际文件、更新评论与逐帖记录；它不会触发采集、重试其他作品或清除另一进行中的批次。

仅核对该批 `work_ids`；同平台尚未提交的链接不因本导出没有它们而算失败。评论身份、文字、父句或根讨论冲突保留为问题，同一实际记录的重复来源不增加讨论数。原帖来源保留，评论来源另记。作品采集完成与是否满足型号、作者及讨论覆盖条件分别计算。

`normalized/*.quality-review.json` 记录实际讨论上下文的人工审读；`*.review.json` 记录作品型号与使用阶段的证据范围。留出作品可以做必要的采样资格核对，不用于表达规律归纳。最终留出输入通过 [离线冻结工具](../evaluation/PREPARE_INPUTS.md)生成。

采集行为以[统一社媒读取技能](../../../read-social-links-with-social-helper/SKILL.md)为唯一规则源，本目录不重新定义采集限制、异常重试或停止条件。

## 用户收口后的状态

2026-09-06停止采集。39篇作品取得本轮正文与评论记录，其中32篇满足当前完整样本条件；不合格项保留具体原因。72篇作品有标题/正文来源，492条评论已入库。C3暂停时导出的58条属于7篇作品，仅保存原始及normalized文件，不进入学习、有效样本、主评/父句计数。

154个尚未完成的候选在台账记`closed_by_user`并保留原状态；这既不是采集失败，也不是待自动续跑。批次状态`not_collected_user_scope_reduced`或`partial_saved_unreviewed_user_stop`说明实际范围。此前的`pending`只在历史字段保留。没有把候选、停止附件或原始文件行数当成有效学习数量。

## 2026-09-10独立研究增量

新授权批次`op-pocket-7d-01`使用统一社媒助手取得9篇B站作品文字和34条评论，23条主评、11条可核父句回复，另外3篇没有导出评论。按真实platform/work_id/comment_id去重，新增34、已有0、原话变化0；语义审读另附，不改原始导出。来源链见[批次清单](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/manifest.json)、[原始读取账本](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/evidence/input-ledger.jsonl)、[增量与边界](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/knowledge-delta.json)。

此批独立为train，未改变旧split或续读C3。`research_text_reviewed`是当前文字研究已审读，不按旧150篇完整样本规则冒称合格作品；目标30篇与媒体未读缺口见批次报告。
