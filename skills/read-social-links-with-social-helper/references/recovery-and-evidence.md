# 问题项交人工与证据交付

Read this for any collection/evidence problem and when accepting or returning artifacts. The filename and evidence-pack keys remain compatible, but all older retry/fallback permissions are retired. **问题项直接跳过交人工，不自行复查采集。**

## Problem isolation and handoff

Use already-observed validation/errors and existing artifacts, not another original-page visit to diagnose the cause. Distinguish rejected input, explicit request failure, inadequate required evidence, control incident, source/quota limit and media/export failure. Missing parameters, source exhaustion and a detached controller do not establish missing membership. Use existing authorized features without purchases or account management.

| Observed condition | Action |
|---|---|
| Local validation failure or form rejection, including missing share parameters | Preserve orders/sanitized input references, exclude the work and known aliases, request human materials. No repair, alias test, rejected short-link resolution or parameter probing. |
| Short-link resolution error, timeout, empty/incompatible extraction, private/deleted/unavailable work | Auto-skip, or use one visible safe item-skip control, and continue valid peers. Hand over the item; no API/RPA retry or original-page recheck. |
| Required fields/IDs missing or mismatched in the once-read export | Preserve export/usable layers, identify the precise gap offline and request human material. Do not re-export/recollect to make the check pass. |
| Smaller comment sample with observed source exhaustion or quota reached | Record real scope/counts; a useful sample is not failed merely for missing a target. No quota expansion/retry. If a specifically required thread/evidence is absent, hand that gap to humans. |
| Required comments empty or unexplained shortfall | Preserve counts/uncertainty and hand over the work. Never claim the source has no comments or fill the gap with another query. |
| Export/download failure, missing/corrupt/wrong required file, stalled relay | Preserve usable rows/files and transfer remaining requirements to humans. No export/download retry, relay repair or metadata recollection. |
| Required feature unavailable or gated | Record the actual missing control, not an assumed free-tier account. If no available initial route meets required scope, hand it over; do not purchase, bypass or substitute a failing mode. |
| Login, captcha or risk warning | Hand over the active run, retaining completed/failed/pending state. Do not skip the warning and continue other browser tasks. |
| Unavailable control or unknown submission | Follow [control incident handoff](browser-control-recovery.md); retain unknown state as needed, with no controller self-repair followed by collection. |

Normal preflight alignment and correcting an obvious input-tool transcription error from unchanged source text are not failed-link recovery. Once a source/work problem is observed, do not recast it as preflight or a different stage to fetch again. Planned first-pass required layers for still-healthy works remain allowed.

Finish other safe first-pass batches when the current queue is terminal or can visibly skip an ordinary item error. If safe skipping/continuation is unavailable, hand over the affected queue including unattempted peers. Do not start a browser task while an old collection/download may still be active. Offline work on completed artifacts may continue.

## Bounded progress checks

Use checkpoints, not one blocking wait over 60 seconds. A healthy queue does not fail because its total duration exceeds an old ten- or thirty-minute threshold.

- Collection: observe every 30–60 seconds. Completed/failed counters, current-item advance, new result rows, comment/page advance and visible request completion count as real progress. A timer/spinner alone does not. After at least 120 seconds without real progress or a visibly explained scheduled wait, record stalled scope and hand it to humans; no refresh, original-link investigation or diagnostic collection.
- Download: observe queue/file/byte progress at intervals no longer than 60 seconds. After five minutes without progress, preserve completed files and hand over the remaining transfer. No retry or reconnection repair.
- Explicit errors, login/captcha/risk or control incidents take their corresponding action immediately. A failed observation is not proof of a stalled collection; record the control incident instead of inventing a timeout for each work.

Auto-skipped items retain autoSkipped: true as provenance; manual skips are recorded separately. Neither removes an input nor implies success. If the plugin's internal request behavior is not exposed, keep it unknown rather than claiming one underlying HTTP request. The enforceable policy is no assistant resubmission/fallback; use a visible no-retry setting if available, never hidden configuration.

For a run-level blocker, use an already-visible safe pause control where possible, without bypassing dialogs. If the stopped task visibly permits exporting completed rows and that step has not failed, save one labeled partial checkpoint. Otherwise preserve known state and existing artifacts. A partial export is not a completed-batch result and does not authorize another collection. If the human later completes that same queue, one first final export of its newly completed result is distinct from repeating the earlier partial snapshot; allow it only if no adequate final artifact exists and no export failure is being retried. Record task identity, snapshot kind and counts so the same result is not exported twice.

Record runStatus: needs_user, blockedBy, submissionState (not_submitted/submitted/unknown), taskRef, completedWorkIds, failedWorkIds, pendingWorkIds, completedFiles and pendingFiles. Keep genuinely unattempted items pending under the run blocker; do not call them failed. Use state: blocked only when required evidence depends on the blocker. Already adequate structured evidence can remain successful when only optional media was interrupted, with that limitation noted.

## Human handoff and return

Return one consolidated handoff list alongside successes, preserving every original position. Include platform/query identity, original orders, sanitized link/work ID, observed reason/stage, existing task/artifact references and exactly what the human should provide. Do not include sensitive share parameters; point back to original input. Merge all aliases' orders/problem history.

Add optional **manualHandoff** to an existing record, preserving required keys and state values. Its fields are:

- required: true;
- stage: input, discovery, post, comments, export, media or control;
- observedReason: actual visible error or exact evidence gap;
- taskRef and existingArtifactRefs;
- neededFromHuman: missing text/comments/media or task takeover;
- assistantRetryAllowed: false.

manualHandoff.required excludes a work from collection, not from using successful layers. Keep failed/blocked state as appropriate until sufficient human material is supplied; record useful partial scope in limitations. For a failed keyword without a work ID, keep a query-level handoff keyed by platform+keyword+filters.

Do not create a retry batch, try another alias/mode, visit the original page, search substitutes or let downstream writing/scoring trigger “补读”. The exclusion persists across stages, batches and turns. Remove newly identified aliases before another stage; unknown attempts are not new inputs.

After explicit human handback follow [control handoff rules](browser-control-recovery.md#receive-an-explicit-human-handback). Once-verify supplied existing exports/screenshots/transcripts/media offline, merge by ID and restore order. Use readMethod: 用户材料 where applicable and preserve actual provenance/time. A general “已处理/已采完” is not recollection permission. Only a safe, explicitly returned and definitely unattempted remainder can resume assistant first-pass processing; problem works remain human-owned.

If no useful material is available, report the limitation and deliver remaining successes. Do not substitute search or a title for inaccessible original content.

## Shared handoff index

Across projects, consult **$CODEX_HOME/social-collection-state/manual-handoff-index.json**, using **~/.codex/social-collection-state/manual-handoff-index.json** when CODEX_HOME is unset. It is private runtime state outside the installed skill/package, not a second collection policy or a public evidence cache. Do not create an empty file until there is an actual handoff to record.

Before scheduling, read this index plus the current request's existing ledger/handoff. The active collector merges new problem records before yielding the browser or ending the run; preserve other callers' entries. Use schemaVersion: 1 and an items array. Each item carries platform, a stable work ID or sanitized URL/query identity, sanitized known aliases, observedReason, stage, lastObservedAt, sourceLedgerRefs, original input references, existingArtifactRefs and collectionExcluded: true. Store only public/sanitized identifiers and file locators, never share tokens, cookies, private comment text or complete exports. Failed keywords use platform+keyword+filters as their identity.

The source ledger retains detailed attempts, uncertainty and evidence; the index only makes known exclusions discoverable. A new caller reads referenced relevant records, merges aliases and does not resubmit an excluded work. Evidence-cache expiry never clears an exclusion. Human-provided artifacts may mark evidence resolved and be reused, but do not automatically remove collectionExcluded. Only a new explicit user instruction changing the human-only collection decision can authorize revisiting that work.

An absent index on first use means no recorded shared exclusions, not that reported prior attempts can be ignored. If input/handoff refers to a previous problem or uncertain attempt but its ledger is unavailable, keep that item unknown/human-owned. If an existing index is unreadable or conflicting, hand over the affected scheduling uncertainty rather than overwrite it or treat all links as fresh. Ordinary genuinely new inputs with no problem history still receive their planned first pass.

## Evidence pack

Create one record per normalized unique work, merge its link aliases, and reuse it for every downstream task in the same run:

```json
{
  "platform": "抖音|小红书|B站",
  "inputOrder": 1,
  "sourceInputOrders": [1],
  "state": "pending|success|failed|blocked",
  "autoSkipped": false,
  "rawUrlRef": "input index or sanitized user-supplied URL; retain sensitive parameters only in memory",
  "aliasRefs": ["sanitized references for duplicate short/canonical inputs"],
  "canonicalUrl": "resolved work URL",
  "workId": "platform work ID",
  "author": "visible/exported creator nickname",
  "title": "visible/exported title",
  "bodySummary": "faithful concise summary",
  "summaryBasis": "metadata|transcript|media|mixed",
  "anchors": [
    {
      "claim": "verified line, visual, action, or viewpoint",
      "sourceType": "exported field|transcript|video frame|image|visible comment",
      "locator": "field name, timestamp, frame timestamp, image index, or comment ID"
    }
  ],
  "commentsStatus": "not_requested|collected|unavailable",
  "visibleComments": ["only comments actually collected when needed"],
  "mediaPaths": ["local verified artifacts when downloaded"],
  "readMethod": ["社媒助手字段", "社媒助手媒体", "Chrome原页", "用户材料"],
  "retrievedAt": "ISO-8601",
  "confidenceByAspect": {
    "metadata": "high|medium|limited|not_assessed",
    "audiovisualContent": "high|medium|limited|not_assessed",
    "comments": "high|medium|limited|not_assessed"
  },
  "limitations": [],
  "failureReason": ""
}
```

Keep these failure categories when applicable: `平台不支持`, `需登录`, `验证码`, `私密/删除`, `超时`, `链接无效`, `采集为空`. A control/export/ID-mismatch problem with no matching category retains its exact reason in `manualHandoff`/`limitations`; do not mislabel it to fit a category. Other platforms follow the global Chrome workflow, not this skill's platform enum.

## Evidence rules

- Read each batch artifact as a whole once and reconcile all expected IDs/required evidence locally. Verification does not authorize another acquisition; a failed check goes to humans.
- Structured export can establish author, title/body, tags, publish time, counts, and returned media URLs.
- A metadata-only summary must say it summarizes the post's exported title/body rather than the full audiovisual work.
- To claim a visual action or scene, inspect already-collected images/video frames or a visual observed during the healthy first pass; do not return to a problem original page to fill the claim.
- To claim spoken wording, inspect a subtitle/transcript or transcribe audible media. Do not infer speech from the title.
- Comments are volatile. Label them as visible at retrieval time and never imply that an unavailable comment section was read.
- Use `commentsStatus: not_requested` when comments were intentionally skipped; an empty comment array must not be presented as proof that the post has no comments.
- Verify downloaded artifacts exist, are non-empty, and correspond to the requested work ID before analyzing them.
- Redact passwords, OTPs, cookies, tokens, account identifiers not needed for the task, and private document content from summaries and saved evidence.
- Report partial success per link rather than failing an entire batch.
- Include a precise source locator in every anchor and restore `inputOrder` when presenting results after platform-grouped processing.
- Optional stage/provenance metadata can point to shared artifacts and actual stage counts, attempts and timings. Do not duplicate full exports. Candidate-list success is not post-reading success; metadata is not audiovisual success. Failed required layers remain explicit and human-owned; preserve existing fields and original order.
