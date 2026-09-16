# 卖点记录格式

`cards.jsonl` 每行一个明确型号的卖点。它是编辑组织层，产品事实、兼容和来源仍维护在原JSONL。

必需字段：`id`（MOBILE-SELL-三位编号）、`models`（仅一个明确型号）、`title`、`kind=editorial_synthesis`、`value_status=hypothesis_not_measured`、`edited_at`、`capability_summary`、`task`、`possible_value`、`audience_ids`、`scope_note`、`fact_ids`、`compatibility_ids`、`avoid_claims`。

能力概括必须由同型号的已核记录支持；不同型号的对比只写清边界，不以别款的能力当本款依据。用途和价值是编辑推演，人物匹配不是调研结果。不能将这层标为verified、实测收益或用户认可。

不在卡内复制一套参数、完整条件、来源快照与核验日期。生成页链接至原事实的完整条件及来源，显示的核验日期自动从事实记录取得；`edited_at`仅代表编辑日期。未决项目自动按对应型号在阅读页提示，不得用通用卖点覆盖具体兼容冲突。

`scripts/maintain.py render` 调用 `selling_points.py render` 生成概览和7个型号页面；`audit` 检查ID、型号、事实状态与归属、角色引用和资料性质。`rg`先命中整卡，随后读取其fact_ids、compatibility_ids的完整原记录；需要具体参数时可使用原query.py，不能只拿标题作答。

本层不提供成品评论或固定句式，实际写作仍由共享写手决定表达及training_fiction状态。
