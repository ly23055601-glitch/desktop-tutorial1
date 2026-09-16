# Browser control incidents and human handoff

Read this for unavailable browser/side-panel control or an explicit human handback. The filename is retained for compatibility; it no longer authorizes an automatic recovery pass. Collection and evidence rules remain in the central skill.

## Classify without repairing

A detached debugger, inaccessible native menu or unreadable side panel is a control incident, not proof of a platform API error, bad link or missing membership. A missing screenshot alone is not a failure when current accessibility state sufficiently exposes the intended controls. A diff omitting unchanged content is not proof that the panel disappeared: one full state may supply the missing context.

Normal preflight may select the intended existing tab and open a closed side panel before submission. Once control genuinely fails, preserve the last observed state and hand it to a human. Do not loop menu cancellation, shortcuts, resets/rebinds, fresh tabs or page refreshes to repair access. Do not use another transport, extension-internal URL, hidden data, DevTools or browser restart to circumvent a blocked surface.

One read-only observation of the existing current surface is allowed if it can record the handoff; it does not authorize navigating, reopening a failed work, inspecting task after task or retrying a failed tool call. If that observation fails, retain previous facts and mark uncertainty. Do not pause/navigate/refresh a possibly active queue solely to repair observation; use a pause control only if its current safe target is actually known.

## Preserve submission and ownership

Record a run-level controllerIncident: platform, task name/type/creation time if known, accepted scope, completed/failed/pending counts, last real progress, current collection/download activity, artifact paths and observed error. Keep submission state separate:

- **not submitted:** the known form was never started; inputs are unattempted but blocked on the run-level incident, not immediately available for another task;
- **submitted:** the existing queue may still be working; do not replace it;
- **unknown:** preserve uncertainty; neither zero attempts nor failure nor completion may be inferred.

Do not assign every work a false platform failure category because the controller is unavailable. Leave definitely pending works pending under the run blocker; retain adequate successes. A metadata-complete task can still own the browser through a media download, especially a B站 relay. No other caller may switch platform or close/refresh that page until terminal state or a safe human handoff is established.

Send the human a compact request to take over the existing task, including what is known, uncertain and still required. No password, token or login secret is needed.

## Receive an explicit human handback

“已登录会员” only clarifies entitlement. “已处理” or “已采完” does not grant automatic retries. If a user reports completion, retain old observations as history, record userReport: completed, and mark current unobserved submission state unknown until supported by a matching existing task or supplied export. Do not infer their attempt count.

After an explicit handback or supplied artifact:

1. Prefer an existing local export/media file. Verify IDs and required content offline once; use actual provenance/time and do not label it an assistant-witnessed collection.
2. If a stored result is needed and the user restored the visible surface, read current state once. Match task by platform, type, name/time and accepted inputs—not a generic title alone. Use visible read-only **查看详情** or **采集历史** only to reach that matching existing result. Never use **重新采集**, create a task, repair the connection or replay failed controls. If identity/control remains uncertain, retain handoff.
3. Export a matching terminal task once only if no adequate final export exists and that export step has not already failed. A prior partial checkpoint does not prevent the first final export of that same queue after human completion: it is a new result snapshot, not a repeat of the partial one. Record snapshot kind/counts, never repeat the same result or retry an export failure. Verify selected folder, non-colliding filename and actual nonzero file after saving; preserve failure without another attempt.
4. A visibly running healthy queue may be observed without a new start. A paused/remainder queue may return to assistant first-pass processing only when the human explicitly asks for it and preserved progress proves the remainder is unattempted, the blocker is gone, and no problem/unknown item will be retried. Membership **续采** alone does not prove these conditions; **重新采集** never does. If current state/artifacts cannot establish the boundary, leave the queue with the human.

Problem works stay excluded across turns and aliases, even when healthy unattempted works return. Human replacement material can close evidence gaps offline. Continue independent offline analysis while the human holds browser ownership; never create a competing browser task.

## Evidence boundary

Report control incidents separately from membership/platform errors. If a human restored the surface, report that observed state; do not claim a policy/field edit fixed an unreproduced transport bug. A historical task card establishes its own settings, not that the assistant witnessed the original run. Keep the incident and handoff in the same ledger rather than resetting them each turn.
