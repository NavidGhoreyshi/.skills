---
name: audit-loop
description: Run a complete project-wide frontend/backend wiring audit in one pass. Exhaustively inspect every user-facing route, SPA view, control, data-bearing element, state transition, API contract, permission boundary, persistence path, cache, privacy rule, failure state, and browser flow; build a finding ledger before repairing. Ask the user up front whether confirmed defects should be fixed automatically or walked through one at a time for approval. Use incremental one-unit mode only when the user explicitly requests it.
---

# Complete UI Wiring Audit

One exhaustive run, not a finding-driven loop. Two phases: **discovery** (map everything, build the ledger, touch no application code) then **repair** (branch on the mode below). Incremental one-unit mode only when explicitly requested; otherwise never let an old one-page boundary truncate the sweep.

## Step 0: Choose the mode first

Before mapping or inspecting, ask the user:

> How should I handle the defects this audit finds?
> 1. **Auto-fix** — audit everything, then fix all confirmed defects automatically (default).
> 2. **Interactive** — audit everything, then walk me through each defect one at a time so I can decide what to do.

- **Auto-fix:** after discovery, autonomously fix every confirmed in-scope defect, add regressions, verify, report the full ledger.
- **Interactive:** identical discovery, repairs nothing. After discovery, present findings in a severity-grouped table, then walk through each defect one at a time — explain it, offer a fix, let the user decide.
- No preference → default to Auto-fix. The mode changes only *who decides what gets fixed*, never what gets audited. Honor it for the whole run.

## Project files

Defaults, configurable per project: `docs/ui-tree.md`, `docs/ui-audit-progress.md`, `docs/wiring-audit-findings.md`, `docs/browser-tools.md`.

## Audit invariants

Incomplete unless:

- Every page/route, layout, shared component, API wrapper, backend route, view, serializer, model, permission, migration, cache key, external integration, and relevant test is mapped or explicitly out of scope.
- Every control and datum has a ledger entry — nothing skipped because it looks correct.
- Every data flow traced end to end: `UI state → API wrapper → URL/method → auth/role → validation → view/service → model persistence → serializer/response → normalizer → rendered state`.
- Findings classified `confirmed bug` / `missing coverage` / `intentional` / `unproven`. "Not observed" ≠ "passed".
- A render-only smoke, clean build, or zero console errors never proves a mutation, privacy rule, persistence round-trip, authorization boundary, cache invalidation, or failure state.
- Discovery completes across all mapped units before repair narrows attention.

## Roles

Responsibilities, not agent names. If a named role/tool is unavailable in the runtime, perform it directly with whatever search/read/test tools exist and continue the sweep.

### Tree-mapper: inventory before selecting work

1. Record the `git status --short --branch` baseline. Dirty tree: freeze it, distinguish pre-existing from audit changes; never reset/stash/stage existing work.
2. Enumerate all frontend routes/pages, layouts, boundaries, components, hooks, utilities, API modules; all backend URLs, views, serializers, models, permissions, signals/tasks, migrations, tests.
3. Verify both directions with code-search/glob/read tools: page → wrapper → backend, and backend route → consumer. Hunt dead wrappers and unconsumed fields.
4. Refresh the tree doc; preserve stable IDs and history; add, don't assume.
5. Per unit, inventory every control (button, link, toggle, tab, filter, form, input, select, upload, rating, report, delete, cancel, approve, reject, pagination, retry, login, logout, navigation) and every datum (list, card, KPI, chart, table, image, avatar, map, date/time, price, status, badge, notification, empty/error), plus every API read/write, cache read/write/invalidation, permission check, persistence side effect, external integration.
6. Mark each entry `proved` / `confirmed gap` / `intentional` / `unproven` / `dead` / `mock` / `unknown`. A unit without this inventory isn't audit-ready.

### Section-auditor: exhaustive state and contract crossing

Audit **every** mapped unit, not just the first pending one.

**State matrix** — per route/view and control/data block, record cells for: anonymous / customer / owner / employee / verifier / wrong role / expired session / missing identity; loading / populated / empty / malformed / 4xx / 5xx / timeout / retry / refresh; first-use / missing optional fields / invalid input / boundaries / duplicate / stale / concurrent / optimistic rollback; pending / approved / rejected / cancelled / inactive / expired / archived; pagination first/middle/last, over page size, zero-result filters, query sync, deep links; mobile/desktop, keyboard/focus, RTL/Persian digits, Jalali/Gregorian dates, currency/large numbers, broken images; privacy on/off, owner preview vs anonymous output, object scope, cache warm vs cold. Cells: `proved` / `confirmed bug` / `unproven` / `n/a` + reason. Never collapse loading/empty/error/unauthorized into "page loads".

**Reads** — for every read: identify the rendered field → trace wrapper URL/method/body/normalization → resolve backend route/permission/queryset/relation/serializer/envelope → check names, nullability, types, nested relations, pagination, labels, image URLs, dates, fallbacks → confirm the serializer the actual endpoint uses (not a similar one) contains the field.

**Writes** — for every write: control validation/disabled/loading → exact URL/method/content-type/payload/role boundary → backend validation, ownership, transactions, persistence, signals/jobs, cache invalidation, response shape → prove load→edit→save→reload incl. optional/invalid states → prove negatives (wrong role/object, duplicate, stale, inactive, expired, rejected, cancelled, failed).

Relationships checked in both states: no related rows and ≥1 active/inactive related row. Reverse relations, annotations, soft delete, cached responses are prime contract-gap territory.

**Mandatory searches** (all must run before discovery ends): wrapper paths vs every URL pattern incl. method/trailing slash; frontend field names vs serializer/model fields (typos, FK-vs-nested, aliases); `catch` fallbacks to `[]`/`null`/`0`/""; hardcoded/mock data, dead endpoints, no-op handlers, swallowed errors, "best effort" writes; permission classes, role checks, ownership, anonymous access, privacy redaction, verified filters; cache read keys vs write-side invalidation incl. versioned keys and auth scopes; pagination envelopes, caps, filters, query params, empty/error states; lifecycle transitions approve/reject/cancel/delete/restore/resubmit and whether the UI distinguishes terminal states; model fields added by migrations vs reverse/relation fields the frontend expects; tests asserting only 200 without persistence/fields/privacy/ownership/UI state.

Findings, not acceptable degradation: hardcoded values in data slots, dummy arrays, missing handlers, dead wrappers, mismatched payloads, `catch {}` fallbacks, `Phase 2` / `assumed` / `pending BE confirm` stubs, silent auth failures, stale cache, render-only tests.

## Browser proof

1. Read the project's browser-tools doc if present; check system browser and any project-local Chromium/Playwright.
2. Prefer project-local Chromium + Playwright Core against a production build, proxies disabled. A dev/HMR server is not production proof; use a bounded alternate-port harness rather than changing app code.
3. Run every relevant harness, not just the first that passes. For gaps, add a temporary project-local smoke; remove it after.
4. Prove each mutation with action + observed network request + resulting rendered/persisted state. Exercise anonymous/public privacy and wrong-role boundaries. A zero-error render is insufficient.
5. Missing credentials/fixtures/services: mark cells `unproven` explicitly, continue the sweep. Distinguish implementation failures from harness/environment failures; record failed commands and diagnosis instead of retrying forever.

## Repair — Mode A: auto-fix

1. Order confirmed findings and missing coverage by severity + dependency. Never restart the audit after the first fix.
2. Fix every confirmed in-scope issue (audit-only request → leave code untouched, report the repair queue).
3. Add focused regressions per defect class: state transitions, privacy, cache, relations, optional fields, pagination, cancellation/rejection, error states.
4. Re-run affected matrix cells + relevant lint/typecheck/build/unit/integration/browser checks.
5. Use a code-review agent when available; fix its findings, re-run validation.
6. A passing build never resolves a finding — resolution requires a matching regression or action-level proof, or a documented intentional-behavior reason.
7. Report the complete ledger once; don't pause mid-run with "continue?".

## Repair — Mode B: interactive

Keep code untouched through discovery. Then:

1. Present the full ledger as a severity-grouped summary table (🔴 Critical, 🟠 High, 🟡 Medium, ⚪ Low), ordered by severity then dependency, status starting ⏳:

   | ID | Severity | Location | Issue | Status |
   |---|---|---|---|---|
   | F-01 | 🔴 Critical | `frontend/app/user/settings/page.tsx` | Notification prefs stored in `localStorage` only | ⏳ Pending decision |

2. Walk through each defect one at a time, highest severity first; no batching, no skipping.

### Per-finding workflow

1. **Introduce** — detail table in the audit-fix layout:

   | Field | Value |
   |---|---|
   | **ID** | F-01 |
   | **Severity** | 🔴 Critical |
   | **Location** | `frontend/app/user/settings/page.tsx` |
   | **Description** | What's wrong, plainly. |
   | **Impact** | What breaks, for whom. |
   | **Evidence / proof status** | `confirmed bug` / `missing coverage` + cites. |
   | **Recommendation** | Fix direction from the ledger. |

2. **Recommend** — concise implementation plan (files, behavior, tests).
3. **Ask** — "How would you like to solve this?":
   1. **Your proposed solution** — implement as described.
   2. **Different approach** — user describes it; implement that.
   3. **Skip this issue** — log skipped/deferred, move on.
   4. **Already resolved** — record resolved, move on.
4. **Act** — approved fix: minimal change, focused regression, re-run affected cells + relevant checks, prove it like the audit proves findings; update status ✅ fixed / ✖ skipped / ⏸ deferred. Skipped/resolved: status only, no code.
5. **Next** — report what was done, show updated status, present the next issue. Finish when every row has a terminal status.
6. Report the final ledger: every fix, every skipped/deferred/unproven item. Nothing silently dropped.

Commit only with authorization, only this audit's files, explicit paths — never broad staging, deploy, reset, or stash.

## Completion criteria

- every unit inventoried with state-matrix results;
- every control/datum classified and traced;
- every read/write contract checked end to end;
- findings reported with severity, evidence, files/flows, proof status, repair order;
- auto-fix: all confirmed fixes have regressions + validation results;
- interactive: every finding has a terminal decision, and each approved fix has regressions + validation results;
- unproven cells and environmental limits listed explicitly;
- docs updated without converting "unproven" into "done."

## Documentation and reporting

Update the progress doc: audit ID/date, scope, findings count, mode, commands, pass counts, browser evidence, unproven cells. Update the findings doc with evidence/status incl. interactive decisions. Preserve history and stable unit IDs.

Report scope, matrix/data-flow coverage, every finding/fix, files changed, exact commands + pass counts, browser evidence, unresolved/unproven items, environmental limits, next repair order.
