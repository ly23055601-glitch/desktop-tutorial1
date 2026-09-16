# training_cw5 首期校准试点

首期先从历史培训产出抽取 10–20 帖，不把既有 `independent-review.json` 直接当作新质检结论。它们只作为正反例和证据范围的候选来源。

建议覆盖：

- 至少三条产品线和两类帖子类型
- 已通过稿、返工稿和存在语义问题的稿件
- 普通产品语境与横测稿
- 主评、回复和跨帖同质化问题

对每个候选稿，在其对应 `v1` 目录创建 `quality-review.json`，绑定原稿 SHA256，按 `training_cw5` 维度重新评分。两名独立审稿角色对部分样本双盲评分，先对齐问题码、严重度、证据引用和改写边界，再冻结首版权重。

单条质检：

```bash
python3 quality_review/quality_review.py \
  outputs/daily-comment-training/2026-09-08/B001/T053/v1/quality-review.json \
  --draft outputs/daily-comment-training/2026-09-08/B001/T053/v1/comments.md \
  --output-json outputs/daily-comment-training/2026-09-08/B001/T053/v1/quality-review.scored.json \
  --output-md outputs/daily-comment-training/2026-09-08/B001/T053/v1/quality-review.md
```

批次或写手汇总：

```bash
python3 scripts/quality_summary.py outputs/quality-review-pilot --pretty \
  --output outputs/quality-review-pilot/quality-summary.json
```

试点结束前只比较分数、问题码和审稿一致性，不把试点结果写回共享写手反馈或绩效记录。确认口径后，再由每日入口在全量基础质检和风险/抽样深审阶段引用这些文件。
