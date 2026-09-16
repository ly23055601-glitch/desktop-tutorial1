# training_cw5 文案质检核心

`quality_review.py` 是独立的质检 artifact 检查器和评分器。它不读取、修改或扩展
`ledger.json`、`training-state.json`，因此可以被每日入口作为引用产物接入而不改变既有
`draft_completion` 和 `review` 口径。

## 使用

```bash
python3 quality_review.py quality-review.json \
  --draft v1/comments.md \
  --output-json quality-review.scored.json \
  --output-md quality-review.md
```

输入可使用 `assets/quality-review.template.json`。`draft_sha256` 必须是稿件的 SHA-256；
传入 `--draft` 时会再次核对。默认输出评分后的 JSON；指定输出文件后不会向 stdout 写
内容，校验失败返回退出码 2。

必填字段是任务/稿件引用、哈希、`profile=training_cw5`、覆盖档位、三项维度分数、问题
数组、教学完整和用户验收状态。每个问题必须提供稳定 `issue_id`、受控问题码、严重度、
观察和处理动作；`location`、`evidence_refs`、`rewrite`、`recheck_status` 用于定位和
保留改稿复检链。`reviewer` 与 `reviewed_at` 可选，适合在独立复审完成时写入。

原始分为 60/25/15 三项之和。存在 blocker 时总分封顶 59 且结论为 `block`；无 blocker
但存在 major 时封顶 79；总分低于 90 或 `teaching_complete=false` 为 `revise`，其余为
`retain`（因此 75–89 分进入修改/复训）。输出同时提供 `quality_score`、`quality_issue_codes`
和派生 `decision`，便于台账引用。输入中若已有 `decision`，必须与上述派生结论一致，避免覆盖历史结论。

问题码、JSON Schema 和五条产品线的检查插件清单位于 `assets/`；Schema 用于编辑器/离线校验，最终约束以 CLI 为准。插件清单只声明产品侧追加检查项，事实核验仍由对应产品知识入口和 evidence/knowledge handoff 提供，不由通用评分器臆测。
单元测试：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
