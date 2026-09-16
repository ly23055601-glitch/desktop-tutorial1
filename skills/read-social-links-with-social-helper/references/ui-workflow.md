# 社媒助手 UI 工作流

Use this reference when driving 社媒助手 through Computer Use. Labels may vary slightly by extension version; match their meaning in the current accessibility tree instead of relying on position.

## Platform routing

| URL platform | Side-panel header | Default item route | Item-link control | Creator-link control | Comment route |
|---|---|---|---|---|---|
| 抖音 | `社媒助手 - 抖音` | `采集视频数据` | `视频链接` | `达人链接` | `采集评论数据` |
| 小红书 / Rednote | `社媒助手 - 小红书` | `采集笔记数据` | `笔记链接` | `博主链接` | `采集评论数据` |
| B站 / Bilibili | `社媒助手 - B站` or equivalent | `采集视频数据` | `视频链接` | `UP主链接` or the visible creator-link equivalent | `采集评论数据` |
This skill is intentionally scoped to the three rows above. For 快手、TikTok、星图、蒲公英、微博 and other platforms, do not open 社媒助手; follow the global all-channel rule, organizing the complete set and reading original visible content once in the user's connected external Chrome. Problem pages go directly to humans, without refresh/revisit or a substitute search.

## URL and redirect validation

Before navigating, parse the URL rather than matching text fragments. Accept only HTTPS URLs with no embedded username/password, no non-default port, and a hostname equal to or beneath one of these registrable domains:

- 抖音: `douyin.com` or `v.douyin.com`;
- 小红书: `xiaohongshu.com` or `xhslink.com`;
- B站: `bilibili.com` or `b23.tv`.

Reject IP literals, localhost, non-HTTPS schemes, and lookalike suffixes such as `douyin.com.example.org`. An approved official short-link host may redirect only to another allowed hostname for the same platform. Re-check the final URL after redirects and stop before opening 社媒助手 if the platform changes or the final host is outside the allowlist.

## Preflight

1. Use the external Chrome profile that already contains the extension and platform login.
2. Reuse a suitable target-platform tab or open one representative page and let navigation finish. Confirm the native window's selected tab and URL match it; a background browser-tab handle alone is not enough. Do not navigate every link or open a new tab for every batch.
3. Open the sidebar with `Alt+C` or its visible toolbar/sidebar control only when closed; repeatedly toggling an already-open panel hides it.
4. If another task is unfinished, inspect its state. Monitor it if it belongs to this request and is healthy; problem/uncertain tasks follow the human-handoff reference. Otherwise wait for its owner's handoff before disrupting it. Existing unrelated tabs may remain open; only the current batch's representative tab and side panel should be controlled, with one active collection task across callers.
5. Confirm the panel header matches the target platform. A mismatched page/panel can produce a “切换” prompt or the wrong set of actions. One representative page is sufficient; do not visit every valid input before batch submission.

Use the native Chrome app accessibility surface for the side panel and save dialog. The preflight passes only when that surface exposes the actual form/task, not merely a readable platform webpage. If the native panel really is unavailable or the debugger is detached, follow [control incident handoff](browser-control-recovery.md); a missing screenshot alone is not a failure when accessibility state is sufficient. Do not refresh/create tabs to repair a failed surface. After explicit human handback, prefer existing artifacts and follow that reference before touching a stored task; reported completion is not permission to collect again.

Use one fresh native state after each navigation/form change. Read only the relevant panel section for routine progress; if an AX diff omits an unchanged panel, request a full state when needed rather than declaring the panel missing. Use screenshots for unlabeled controls or ambiguous states, not alongside every otherwise sufficient text observation. Batch deterministic form edits in one tool call, then verify the resulting state before starting.

## Input preparation

- The link box accepts bare validated HTTPS URLs and share snippets containing them; put one target per line. Normalize an official HTTP form to HTTPS without navigating it, then apply the same validation.
- Preserve source order while removing duplicates. Choose an intact provided canonical/share form locally when available; otherwise let the extension resolve a supported short link in the normal first pass. Do not add a conversion workflow.
- Deduplicate locally known work IDs before submission. Submit supported short links without pre-opening each one, then merge aliases using returned work IDs, retaining earliest position and all source orders. Remove satisfied aliases from later queues. When an alias reveals an already-problematic work, preserve its existing handoff and remove every known alias from remaining assistant stages; do not navigate the failed link individually.
- Keep submission text separate from sanitized ledger URLs. Retain provided 小红书 share parameters for submission; never reconstruct from a redacted report or an ID-only archive. Do not assume all tokenless URLs fail. If the actual form rejects a missing parameter or link, isolate that work for humans and keep valid peers together. Do not try another alias, resolve the rejected short link, invent/borrow tokens, or probe variants. A pre-submission rejection is recorded as not submitted but remains a problem item, not a fresh queue candidate.
- Record each unique work in a small ledger with `platform`, `workId/canonicalUrl`, first `inputOrder`, all `sourceInputOrders`, sanitized `aliasRefs`, `pending|success|failed|blocked`, and an `autoSkipped` provenance flag. Never infer that all inputs succeeded from the batch-level status.
- Never combine platforms in one task.
- Partition the platform group using the central [batch policy](../MODULE.md#batch-policy). Do not add local caps or split for per-link writing/evidence review. Paste once and verify accepted count. An explicit lower input/task limit may require smaller batches. If a mismatch cannot be resolved from the existing visible validation and local input ledger, preserve the form and hand over the uncertain scope; do not repeatedly submit or investigate links to explain a missing tail.
- After filling the multiline field, move focus out to commit validation. Check that punctuation and provided share parameters survived input; count alone does not prove valid input. Before submission, correct only an obvious input-tool transcription error using the unchanged source text. A genuine source/form rejection follows direct human handoff; do not repair the source URL. Remove identified rejected rows and commit valid peers together without per-item test submissions.
- Use the platform-native item-link control from the table, not its creator-link control, unless the user explicitly asks for a creator feed. Verify the label in the current UI rather than assuming a recorded Douyin label exists on every platform.
- Enable `异常自动跳过` for multiple links when available under the user's existing membership. If unavailable, keep the batch and use one visible skip for an ordinary failed current item only when it safely advances to valid peers. Record each skipped work for humans, never a retry pass. Do not skip login, captcha or risk control. If no safe skip/continuation exists, preserve the queue and hand off rather than purchasing access or repeatedly acting on the problem item.
- Configure the platform's interval as described below; the extension controls per-request waiting. During a running queue, perform offline preparation or analyze already-exported evidence instead of manually starting each item.

## Request interval before batch start

1. Read the central batch policy and identify this platform, collection type and mode. Use the visible `当前请求间隔为` / `点击修改` control and the `修改请求间隔` dialog's `最小间隔` and `最大间隔` fields. Set the values, click `确定`, and verify the displayed range. Only change this collection setting, not account/sync settings.
2. In v3.5.1, saving this task-card dialog also saves a default keyed by **platform + task type**. New tasks read that default when initialized; another type falls back to its own value. In particular, a post/video task's setting does not establish a comment task's setting. A previous RPA card alone also does not establish the next API task. Use an existing terminal same-platform, same-type, matching-mode task and its visible dialog before opening the next form; prefer a directly visible pre-start control if the current version provides one. Record the type/mode that was actually checked. Do not invent a global settings control, change stored configuration through code, or create a dummy collection to expose it. If no safe pre-start path is available, stop before submission and explain the specific missing setup.
3. 小红书 uses the central range for every relevant type, including keyword discovery and comments; the number of API waits can exceed the number of works. 抖音/B站 use their own defaults, not the XHS range. Reusing the current run's verified type/mode setup avoids repeated history visits, but each new task still needs the immediate post-start check below.
4. Immediately after starting once, check the interval. The task may briefly show `任务初始化` and `0 / 0`; let initialization settle before reconciling scope. In a post-link task the total should match accepted works; comment/keyword totals can instead be target/result rows, so verify accepted inputs and the counter's meaning. This unit difference or transitional display is not a dropped batch. Persistent initialization with no actual progress follows the [progress checks](recovery-and-evidence.md#bounded-progress-checks). If the actual scope/interval is wrong, pause through an already-visible safe control, preserve completed rows and hand over the queue/settings issue. Do not continue at the wrong range or restart to repair it.

## Stage-specific field selection

Open `自定义导出字段` and select by field name, not a fixed selected-count badge. In v3.5.1 fields are tied to API dependencies, so a larger export preset can cause more requests even without downloading files. Saved local field templates are useful; create purpose-specific ones only when needed, preserve unrelated defaults, and reuse unchanged selections within the run. Templates do not configure the separate interval, media or subcomment switches.

| Stage | Needed fields and explicit switches | Avoid unless this request needs them |
|---|---|---|
| Candidate discovery | Work ID/link, list title, creator nickname, source keyword and list-supported ranking metrics; preserve search filters/time | Full body/description, detail-only publish time, CID, duration, account profile details, tags, media resources |
| Post reading | Work ID/link, substantive title/body, publish time/type and the context actually needed | Account statistics/bio, irrelevant topics/tags, shop/product/affiliate fields, unnecessary media-resource links |
| Comments with sufficient post evidence already available | Comment ID/text, work ID/link, likes, time, reply count; parent/referenced IDs and content when collecting replies; explicitly set `采集子评论` | Associated post title/body/stats already available for local joining, commenter profile/UID/IP, media downloads |
| Comments without sufficient post context | Above comment fields plus needed associated post fields if offered; otherwise one planned batch of missing post context | Full candidate-set detail collection when only a selected subset will be studied |
| Audiovisual evidence | Only the required selected works and media categories | Fetching/downloading every candidate or all categories for a comment-only request |

Candidate metadata is for selection only. Include required content, time and media in the planned first-pass stages for selected non-problem works, or disclose the scope limit. Once a requested stage fails or lacks required fields, hand it to humans; do not add “补读” to make it pass. If a ranking field needs another data layer, plan that bounded layer before collecting or label the available ranking—do not invent an equivalent score.

Platform-specific request costs (v3.5.1 static implementation, recheck the live UI on change):

- **B站:** for discovery, CID/duration and other detail-only fields trigger per-work detail calls. For metadata/comment-only work, explicitly turn **`需要视频文件` off and unselect `视频文件链接`/play-resource fields**: either the switch or such a field can trigger playback-resource requests. Ordinary cover/list fields are not the same as requesting full video. Existing post evidence can be joined to comments by work ID instead of selecting associated post fields again.
- **小红书:** title/link/likes can come from search results; body and publish/update-time fields require note detail, and blogger statistics/bio require separate blogger data. Preserve necessary share parameters, and fetch these extra layers only where the request needs them. Do not omit publish time when it is needed to verify the selected date range.
- **Comments:** v3.5.1's `采集子评论` defaults on; explicitly turn it off for main-comment-only work. Turn it on from the first planned comment pass when discussion chains are required, rather than deliberately collecting roots now and repeating the whole work later. See [keyword and comment collection](keyword-and-comments.md) for quota and completeness checks.

Click `保存`, verify the dialog closes/saved selection is present, then complete the other preflight checks and start once. Do not reconfigure unchanged fields between same-stage batches merely to repeat this checklist.

## Completion and export

Watch the task card rather than repeatedly clicking controls. A successful task normally exposes a terminal `已完成` state and enables a result or export action. Verify:

1. the requested work ID or canonical URL is present;
2. the required content is actually present: verify each requested field or media aspect, not merely one non-empty title. At least one substantive content field must be non-empty; if the source legitimately has no separate title or another requested field is unavailable, record that absence and limitation rather than inventing it or claiming full evidence;
3. each input-ledger row maps to a returned record, an explicit skip, or an explained failure;
4. no item is silently missing because it was auto-skipped. Assign every missing record a per-link state and reason. Do not assume one media file per input because image posts and unavailable media can legitimately change media counts.

Use `导出Excel数据` once per completed batch and parse all rows together. Restore each record's source order and reuse its evidence downstream; do not export or reopen the same task for each link. The next batch may collect while offline processing of the previous export continues. For actual media evidence:

1. click `下载媒体文件`;
2. acknowledge the one-time `下载提醒` with `知道了` if shown;
3. prefer a platform-neutral, collision-resistant path such as `社媒助手/{平台}/{作品ID}/{媒体类型}-{序号}` using the platform-native ID placeholder currently offered by the dialog. If author/title/description placeholders are useful, sanitize path separators, dot segments, control characters, reserved names, and excessive length; fall back to work ID rather than inserting raw page text. (`达人昵称`/`视频ID`/`视频描述` are Douyin examples, not cross-platform constants.)
4. select only what is needed: video for moving image and speech, images for image posts, audio only when a separate audio file helps, and cover only when the thumbnail matters;
5. click `开始下载`;
6. derive expected queue size from selected categories, then monitor until `等待中 = 0` and `下载中 = 0`, or the central stall/blocker handoff applies. At a terminal queue require `已完成 + 下载失败 = expected queue size`; map completed files to work IDs and send failures, missing or mismatched required files to humans without another download.

If the user asks only for a textual summary and the exported fields are sufficient, skip media download.

For B站 downloads, keep the associated page and relay alive until the browser-mediated download queue is terminal or handed to a human; do not switch platform, close/refresh the page, or start another collection while it is downloading or active state is unknown. Record bytes/file progress separately from metadata completion. A relay/file failure goes to humans: no reconnect repair, retry-download control or post-field refetch. Analyze completed files offline while a healthy remainder runs; do not claim missing audio or an incomplete file was reviewed.
