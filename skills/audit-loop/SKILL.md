---
name: audit-loop
description: Run a complete project-wide frontend/backend wiring audit in one pass. Exhaustively inspect every user-facing route, SPA view, control, data-bearing element, state transition, API contract, permission boundary, persistence path, cache, privacy rule, failure state, and browser flow; build a finding ledger before repairing. Ask the user up front whether confirmed defects should be fixed automatically or walked through one at a time for approval. Use incremental one-unit mode only when the user explicitly requests it.
---

# Complete UI Wiring Audit

## Step 0: Choose the mode — ask before doing anything else

At the very start of the skill, before mapping, inspecting, or fixing anything, ask the user how they want the audit run to handle defects. Present both modes and let them pick:

**Mode A — Auto-fix (current default behavior).** The skill audits the whole project and then autonomously fixes every confirmed in-scope defect, adds regression coverage, verifies the repairs, and reports the complete ledger at the end.

**Mode B — Interactive.** The skill audits the whole project exactly the same way and builds the complete finding ledger, but it does not fix anything on its own. After discovery, it presents the findings in a summary table, then walks through each confirmed defect one at a time: it introduces and explains the issue, offers a recommended solution, and lets the user decide what to do with it before moving on.

Ask in plain words, e.g.:

> How should I handle the defects this audit finds?
> 1. **Auto-fix** — audit everything, then fix all confirmed defects automatically (default).
> 2. **Interactive** — audit everything, then walk me through each defect one at a time so I can decide what to do.

If the user does not express a preference or says "your call", default to **Mode A (Auto-fix)**. Honor the chosen mode for the entire run; do not switch modes mid-run unless the user explicitly changes their mind. Interactive mode only changes *who decides what gets fixed* — never the depth of the audit itself.

## Default behavior: one complete audit, not a finding-driven loop

When the user asks for a full, complete, project-wide, or end-to-end audit, do **one exhaustive audit run**. Do not stop after one page, one work unit, the first batch of findings, or a successful happy-path smoke. Do not call the next uncovered surface a "next iteration"; it belongs to the same audit run.

The run has two deliberate phases:

1. **Discovery and proof phase:** map and inspect the entire project, build the state/data-flow matrix, and record every confirmed bug, missing test, intentional behavior, and unproven surface before changing application code. This phase is identical in both modes.
2. **Repair and verification phase:** depends on the mode chosen in Step 0 — see [Repair and review phase](#repair-and-review-phase) and [Interactive mode: per-finding workflow](#interactive-mode-per-finding-workflow).

If the user explicitly asks for one page, one route, one work unit, or an incremental iteration, use incremental mode and stop at that requested boundary. Otherwise, never let the old one-page loop boundary truncate a full audit.

## Project files

Unless the user or project specifies otherwise, use these files (create them if missing; treat these paths as configurable defaults):

- `docs/ui-tree.md` — the wiring inventory produced by Tree Mapper
- `docs/ui-audit-progress.md` — audit run history and per-unit status
- `docs/wiring-audit-findings.md` — the finding ledger, when present
- `docs/browser-tools.md` — browser harness instructions, when present

## Non-negotiable audit invariants

A full audit is incomplete unless all of these are true:

- Every frontend page/route, layout, shared component, API wrapper, backend route, view, serializer, model, permission, migration, cache key, external integration, and relevant test is mapped or explicitly marked out of scope.
- Every interactive control and every data-bearing element has a ledger entry. No control or datum may be skipped because it looks correct.
- Every data flow is traced end to end:
  `UI state → API wrapper → URL/method → auth/role → validation → view/service → model persistence → serializer/response → normalizer → rendered state`.
- Every finding is classified as `confirmed bug`, `missing coverage`, `intentional behavior`, or `unproven`; "not observed" is not the same as "passed."
- A render-only smoke, clean build, or absence of console errors never proves a mutation, privacy rule, persistence round-trip, authorization boundary, cache invalidation, or failure state.
- Discovery is completed across all mapped units before repairs are allowed to narrow attention to the first findings.

## Tool and role mapping

Do not attempt to spawn a specialist by a role name unless that agent is actually available in the current runtime. The roles below are responsibilities, not required agent names. If a named role or tool is unavailable, perform the responsibility directly with whatever search, read, and test tools the runtime provides and continue the full sweep.

### Tree-mapper role: complete inventory before selecting work

1. Run `git status --short --branch` and record the baseline. Do not overwrite, reset, stash, or stage existing changes. If the worktree is dirty, freeze the baseline and distinguish pre-existing changes from audit changes; a dirty tree is not a reason to abandon an audit-only inspection.
2. Enumerate **all** frontend routes/pages, layouts, loading/error boundaries, shared components, hooks, utilities, and API modules. Enumerate **all** backend app URLs, views, serializers, models, permissions, signals/tasks, migrations, and tests that serve or affect those surfaces.
3. Use your runtime's code-search, file-glob, subtree-read, and file-read tools (for example ripgrep-based search, `glob`, `list_directory`, and `read_files`) to verify the map. Search both directions: page → wrapper → backend and backend route → frontend consumer. Search for dead wrappers/routes and backend fields with no consumer.
4. Refresh the tree document while preserving stable IDs and historical entries. Add missing views and dependencies instead of assuming the existing tree is complete.
5. Produce a **global wiring inventory** before section auditing. For every unit, list every:
   - button, link, toggle, tab, filter, form, input, select, upload, rating, report, delete, cancel, approve, reject, pagination, retry, login, logout, and navigation control;
   - list, card, KPI, chart, table, image, avatar, map, date/time, price, status, badge, notification, and empty/error message;
   - API read/write, cache read/write/invalidation, permission check, persistence side effect, and external integration.
6. Mark each ledger entry with its source/target contract and proof status: `proved`, `confirmed gap`, `intentional`, `unproven`, `dead`, `mock`, or `unknown`. A unit without this inventory is not audit-ready.

### Section-auditor role: exhaustive state and contract crossing

For **every** mapped unit in the full audit, inspect current source and tests. Do not audit only the first pending unit.

#### A. Required state matrix

For each route/view and each meaningful control/data block, consider and record the relevant cells:

- anonymous, authenticated customer, owner, employee, verifier/superadmin, wrong role, expired session, and missing/invalid identity context;
- loading, success with populated data, successful empty dataset, malformed/partial response, backend `4xx`, backend `5xx`, timeout/network failure, retry, and refresh;
- first-use/incomplete profile, missing optional fields, invalid input, boundary values, duplicate submission, stale data, concurrent action, and optimistic-update rollback;
- pending, approved, rejected, cancelled, inactive/soft-deleted, expired, and archived records;
- pagination first/middle/last page, more-than-page-size data, filters with zero results, search/query synchronization, and URL deep-link state;
- mobile/desktop responsive layout, keyboard/focus semantics, RTL/Persian digits, Jalali/Gregorian dates, currency/large numbers, and image missing/broken states;
- privacy settings enabled/disabled, owner preview versus anonymous public output, authorization object scope, and cache warm versus cold reads.

A matrix cell may be `proved`, `confirmed bug`, `unproven`, or `not applicable` only with a reason. Do not collapse loading, empty, error, and unauthorized into one generic "page loads" result.

#### B. Required end-to-end data-flow checks

For every read:

1. Identify the exact frontend field rendered.
2. Trace the wrapper's URL, method, query/body shape, headers, and normalization.
3. Resolve the backend route, permission, view branch, queryset filters, model relation, serializer field, and response envelope.
4. Check field names, nullability, types, nested/reverse relations, pagination, status labels, image URLs, dates, and fallback behavior.
5. Verify that the serializer used by the actual endpoint—not a similar endpoint—contains the field the UI consumes.

For every write:

1. Trace the control's validation and disabled/loading behavior.
2. Assert the exact request URL, method, content type, payload names, IDs/slugs, and role boundary.
3. Verify backend validation, ownership/authorization, transaction behavior, model persistence, signals/jobs, cache invalidation, and response shape.
4. Prove load → edit → save → reload round-trip, including optional/incomplete and invalid states.
5. Prove negative cases: wrong role/object, duplicate, stale record, inactive record, expired record, rejection, cancellation, and failed request where applicable.

Always inspect relationships in both database states: no related rows and at least one active/inactive related row. Reverse relations, annotations, soft deletion, and cached responses are frequent contract gaps and require explicit checks.

#### C. Mandatory defect searches

Do not finish discovery until these searches have been performed across the project:

- wrapper paths versus every backend URL pattern, including HTTP method and trailing slash;
- frontend field names versus serializer/model fields, including typos, FK IDs versus nested names, and image/date/status aliases;
- all `catch` blocks and response fallbacks to `[]`, `null`, `0`, empty strings, or fabricated defaults;
- hardcoded/mock/generated data in data slots, dead endpoints/components, no-op handlers, swallowed errors, and "best effort" writes;
- permission classes, role checks, object ownership, anonymous public access, privacy redaction, and inactive/verified filters;
- every cache read key against every write-side invalidation path, including versioned keys and authorization scopes;
- pagination envelopes, page-size caps, filters, query parameters, and empty/error states;
- lifecycle state transitions for approve/reject/cancel/delete/restore/resubmit and whether the UI can distinguish each terminal state;
- all model fields added by migrations and all reverse/relation fields expected by the frontend;
- existing tests that assert only status `200` without asserting persistence, response fields, privacy, ownership, or resulting UI state.

These are findings or coverage gaps, not acceptable degradation: hardcoded values in data slots, generated/dummy arrays, missing handlers, dead wrappers, mismatched payloads, `catch {}` fallbacks, `Phase 2`, `assumed`, `pending BE confirm`, silent authorization failures, stale cache behavior, and render-only tests.

### Browser and test proof

1. Read the project's browser-tools document (if any) before browser work.
2. Check both system browser availability and any project-local Chromium/Playwright runtime.
3. Prefer project-local Chromium + Playwright Core over CDP against a completed production build with proxies disabled. A supervised dev/HMR server is not production browser proof; if the documented port is occupied by dev mode, use the project's supported way to run a production server or a bounded alternate-port harness without changing application code.
4. Run every existing relevant harness, not just the first one that passes. For uncovered flows, create a temporary project-local browser smoke or extend a test harness; keep it out of application code and remove temporary artifacts afterward.
5. Browser-proof each mutation with the action, observed network request, and resulting rendered or persisted state. Also exercise anonymous/public privacy output and wrong-role boundaries. A page render with zero errors is insufficient.
6. If credentials, fixtures, backend services, or a harness are missing, continue the audit and mark the exact matrix cells `unproven`; do not call them passed and do not stop the rest of the sweep.
7. Distinguish implementation failures from harness/environment failures. Do not retry an environmental failure indefinitely, but record the failed command, diagnosis, and unproven cells.

## Repair and review phase

After the global discovery ledger is complete, branch on the mode chosen in Step 0.

### Mode A — Auto-fix

1. List all confirmed findings and missing coverage, ordered by severity and dependency. Do not fix the first finding and restart the audit from zero.
2. Repair all confirmed in-scope issues autonomously. (If the user requested audit-only, leave code untouched and report the repair queue instead.)
3. Add focused backend/frontend/browser regressions for each defect class, especially state transitions, privacy, cache, relations, optional fields, pagination, cancellation/rejection, and error states.
4. Re-run the exact matrix cells affected by each repair and run the project's relevant full lint, typecheck, build, unit, integration, and browser checks.
5. Use a code-review agent when one is available in the runtime (for example `code-reviewer-luna`); fix review findings and rerun affected validation.
6. Never mark a unit or finding resolved because a build passes. Resolution requires a matching regression or action-level proof, or an explicitly documented reason the behavior is intentional.
7. Report the complete ledger, every fix, and every unresolved/unproven item in one final report — do not stop to ask "continue?" in the middle.

### Mode B — Interactive

The discovery ledger is the same; only the repair loop differs.

1. Do **not** fix confirmed issues yet. Keep the code untouched through the end of discovery.
2. Present the full finding ledger as a **summary table**, grouped and ordered by severity (🔴 Critical, 🟠 High, 🟡 Medium, ⚪ Low/Info) and then by dependency, with a status column that starts at "⏳ pending decision" for every row:

   | ID | Severity | Location | Issue | Status |
   |---|---|---|---|---|
   | F-01 | 🔴 Critical | `frontend/app/user/settings/page.tsx` | Notification preferences are stored in `localStorage` only | ⏳ Pending decision |
   | F-02 | 🟠 High | `backend/apps/business/views.py` | Public subresources skip the verified-business gate | ⏳ Pending decision |

   Include every confirmed defect and every missing-coverage item that is worth a decision. Mention the counts per severity above the table.
3. Then walk through each confirmed defect **one at a time**, highest severity first, following the per-finding workflow below. Do not batch, do not skip ahead, and do not move to the next issue until the current one is decided and (if approved) verified.

#### Interactive mode: per-finding workflow

For each finding, in order:

1. **Introduce the issue.** Present a detail table with the same layout the audit-fix workflow uses:

   | Field | Value |
   |---|---|
   | **ID** | F-01 |
   | **Severity** | 🔴 Critical |
   | **Location** | `frontend/app/user/settings/page.tsx`, `frontend/lib/api/auth.ts` |
   | **Description** | What is actually wrong, in plain terms. |
   | **Impact** | What breaks or risks what, for whom. |
   | **Evidence / proof status** | `confirmed bug` / `missing coverage` — cite the files, tests, or browser run that proved it. |
   | **Recommendation** | The concrete fix direction from the ledger. |

2. **Offer your recommended solution.** Based on the ledger recommendation, present a concise, actionable implementation plan (files to touch, behavior to change, tests to add).
3. **Ask for confirmation.** Ask: "How would you like to solve this?" with the options:
   1. **Your proposed solution** — implement exactly as described.
   2. **Different approach** — the user describes their preferred approach; implement that instead.
   3. **Skip this issue** — leave it unfixed, log it in the ledger as skipped/deferred, and move to the next.
   4. **Mark as done (already resolved)** — the user says it was fixed outside this session; record it as resolved with a note and move on.
4. **Act on their choice.**
   - If a fix was approved (option 1 or 2): make the minimal, focused change following the project's conventions; add the focused regression for that defect class; re-run the affected matrix cells plus the relevant lint/typecheck/build/unit/integration/browser checks; prove the fix the same way the audit proves findings. Update the ledger row's status to ✅ fixed (or ✖ skipped / ⏸ deferred / ✅ already resolved).
   - If skipped or already resolved: update the ledger row's status and do not change code.
5. **Confirm and move on.** Tell the user what was done for this finding, show the updated status, then present the **next** issue with the same workflow. Continue until every ledger row has a terminal status.
6. At the end, report the complete ledger with final statuses, every fix made, and every skipped/deferred/unproven item, so nothing is silently dropped.

Do not commit, push, deploy, or reset anything unless the user explicitly authorizes it; if committing is authorized, commit only this audit's files with explicit paths and never use broad staging.

## Completion criteria

A full audit is complete only when:

- every mapped unit has an inventory and state-matrix result;
- every control and datum is classified and traced;
- every read/write contract has been checked end to end;
- all findings are reported with severity, evidence, affected files/flows, proof status, and repair order;
- in Auto-fix mode, all confirmed fixes have regression coverage and validation results;
- in Interactive mode, every finding has a terminal user decision (fixed, skipped, deferred, or already resolved) recorded in the ledger, and each approved fix has regression coverage and validation results;
- all unproven cells and environmental limitations are listed explicitly;
- the audit documents are updated without silently converting "unproven" into "done."

## Documentation and reporting

Update the progress document with the full audit ID/date, scope, findings count, commands, pass counts, browser evidence, unproven cells, and the mode that was run. Update the findings document with each finding and its evidence/status, including interactive-mode decision outcomes. Preserve historical findings and stable unit IDs.

Report the complete scope audited, state matrix coverage, data-flow coverage, every finding/fix, files changed, exact commands and pass counts, browser runtime and viewport evidence, unresolved/unproven concerns, environmental limitations, and the next repair order. If committing is authorized, commit only this audit's files with explicit paths; never use broad staging, deploy, reset, stash, or touch unrelated work. Do not stop at "continue?" until the complete requested audit run has reached the completion criteria.
