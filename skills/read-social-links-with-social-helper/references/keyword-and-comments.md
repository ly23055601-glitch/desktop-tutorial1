# Bounded keyword discovery and comment evidence

Read this for an explicit keyword/topic discovery request or any comment collection. Ordinary supplied-link reading does not trigger a new search. This reference extends the central skill, not its batch sizes, intervals, direct human-handoff or browser-ownership rules.

## Scope and planned stages

Agree on the keyword set, platforms, time range, intended number of selected works, comment quantity per work, and whether replies are needed. Infer choices from an already clear request; if no actual keywords or meaningful collection scope were supplied, propose a small pilot and ask for the missing inputs before collecting. Do not reinstate canceled daily quotas, automatic learning, schedules, paid discovery tools or Apify.

Plan only required stages: **discover candidates → select locally → batch missing content/comments → reconcile and analyze**. Existing adequate artifacts can eliminate a stage. If a request already supplies the complete links, begin with those links; do not search replacement works for failed inputs.

For learning purposes, relevance and informative discussion matter alongside popularity. Preserve positive, negative and mixed viewpoints; do not cherry-pick only praise or treat popularity as factual accuracy. Do not infer an individual's sensitive traits. Keep raw evidence, analyst interpretation and training fiction separate; collected comments are not automatically approved writing examples or product facts.

## Keyword task

1. Use the same connected Chrome/native panel preflight and verify no other browser collection/download is active. Select the platform's **作品关键词** route, not creator keywords or paid keyword expansion. Keep the complete keyword set and original keyword order in one request ledger.
2. On the existing membership, submit the whole platform keyword set together unless the actual form imposes a limit. v3.5.1's ordinary-account component limits a submission to two keywords; do not impose that on an authorized member. Keyword expansion has a separate allowance and is not required. Keyword counts are not work-link batch sizes. Respect any actual account/platform limit without bypassing it.
3. Enter the planned per-keyword candidate quantity and select the native sorting/time filters. Known v3.5.1 work sorting options are:

   | Platform | Work search sorting |
   |---|---|
   | 小红书 | 综合、最新、最多点赞、最多评论、最多收藏 |
   | 抖音 | 综合、最多点赞、最新 |
   | B站 | 综合、最多播放、最新发布、最多弹幕、最多收藏 |

   Verify the actual form; unsupported filters must be disclosed. Preserve the requested date range if the UI offers only a broader period, and check exported dates before claiming a match. Search results are a bounded, account/time-dependent sample, not the platform's complete ranking.
4. Use the UI reference's **candidate** field preset. Do not make every search result fetch full detail, account information or playback resources by retaining a general-purpose default. Keep title and identity for relevance checks. If comment activity/date cannot be established from list fields, obtain the needed field for a bounded subset before final selection, or explain the limited basis.
5. Verify interval for this platform/type/mode before starting; one keyword task may make many paginated requests. Monitor and export once per terminal task. A keyword task's total may describe target/result rows rather than the number of keywords—check task type, accepted keywords and actual returned work IDs, not a link-task count formula. Stop on platform end-of-results, scope limits or the central risk/stop rules; do not loop new keyword variations to overcome a limit.
6. Read the whole export locally. Deduplicate by work ID, preserving all matching keywords and first-seen ranks; select the relevant works using same-platform metrics and the agreed date range. Do not directly compare raw likes across platforms or label an ad as authentic consumer experience. Retain rejected-candidate reasons compactly.

Give selected works stable `inputOrder` values in first-seen discovery order and keep optional `discovery` metadata (keywords, query/filter/rank, selection reason and retrieval time). Supplied links retain their original orders. Submit the complete selected work set through the central batch policy; do not make one acquisition call per keyword or selected work. Already verified content is reused, with its actual timestamp.

## Comment task and cost controls

- Select **采集评论数据** and paste each planned platform batch once. Use API for the first pass and existing membership controls when available. A problem item goes to humans, not RPA, another API attempt, a new service or an original-page recheck.
- Set and record the **per-work total comment quota** and `采集子评论` state. In the inspected v3.5.1 implementation, roots and replies both count toward that quota. A value such as 100 does not mean 100 roots plus unlimited replies, and fewer returned rows do not by themselves prove failure.
- For main-comment expression learning, explicitly turn subcomments off. For reply interaction/long discussion, turn them on initially and retain parent/referenced-comment fields. A truncated quota can cut off a thread; do not call it complete. Set required depth before the first pass, not by automatically expanding the quota afterwards. If a required thread is incomplete, preserve collected rows and request the missing material from a human without another collection.
- Use comment ID + platform/work ID for deduplication. Keep original text, likes, timestamp, root/reply and reference IDs, and necessary parent/reference text. Pseudonymize display identities in learning outputs; omit profiles, account IDs and IP/location fields unless genuinely required. A nickname is not a reliable join key.
- If the existing work artifact contains sufficient context, omit associated title/body/stats and join locally by work ID. Otherwise include only necessary associated fields or plan a first-pass batch of required context for non-problem works. Keep stage-specific history. Once a work has a collection/evidence problem, exclude it and all aliases from remaining assistant stages; missing context cannot become a fallback collection.
- Do not download videos merely because a comment task exists. If interpretation depends on footage or speech, inspect the needed original evidence before making that claim; title-only context must be labeled. Media requests share the central browser-run ownership rule.

## Export, ranking and acceptance

Export the terminal batch once and parse all rows together. Reconcile every selected work, including zero-row cases, against task status and the requested evidence scope. Keep the existing evidence-pack keys; add comment detail or a local comment-artifact locator when needed rather than duplicating thousands of rows in every per-work handoff.

The inspected v3.5.1 comment forms do **not** offer an explicit user-selectable “热评排序”. Work search sorting is not comment sorting. Preserve platform-return order and any visible pinned/author markers separately; sort the collected sample locally by comment likes/reply activity when asked. Label the result **本次已采样本中的高赞评论**, never “全平台最热” or guaranteed complete top-N. A pinned comment is not necessarily the highest-liked one.

Record requested versus returned root/reply counts, collection time, work and comment IDs, and one of these scope explanations when applicable: quota reached, observed source exhausted, user/risk interruption, explicit collection error, or unknown reason. These are explanatory metadata, not replacement per-link failure categories. A source-exhausted nonempty sample can be useful without reaching the quota. An unexplained shortfall stays limited; do not automatically retry until the requested row count is reached. Zero rows must not be presented as proof that the original work has no comments.

Failed keyword queries, failed works, zero/empty required comments and unexplained required-sample gaps go to the same human-handoff list. Keep platform+keyword+filter identity, accepted scope, observed result counts and existing artifacts; do not retry the query, alter keywords/filters, search replacements or open the source page to explain it. Continue other planned valid queries only if the existing queue can safely advance. No quota, membership feature, new stage, alias or later turn grants a fresh attempt to a problem item. Source exhaustion/quota reached are recorded scope limits, not grounds for retries; successful limited samples may still be analyzed within their actual scope.

Return the shortlist, verified comment artifact/source locators and the requested analysis. Restoring output order, preserving failures and separating actual comments from invented examples remain mandatory. Do not save learned writing rules to another skill or knowledge library without the user's authorization for that update.

## Basis and verification boundary

Behavioral details were checked against the user-provided v3.5.1 CRX offline on 2026-09-10; do not execute or patch its code, scrape browser storage, or invoke its internal interfaces. Current labels/entitlements and actual export contents remain the runtime authority. Supporting vendor documentation: [XHS keyword collection](https://socialext.com/help/xiaohongshu/batch-collect/note), [B站 keyword collection](https://socialext.com/help/bilibili/batch-collect/video), [comment collection](https://socialext.com/help/bilibili/batch-collect/comment), [membership features](https://socialext.com/pricing).
