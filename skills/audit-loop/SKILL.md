---
name: audit-loop
description: Choose between a complete API wiring audit, a code quality audit, a security audit, a live user flow audit against the deployed app, and a user-guided missed-features assessment. Ask two setup questions first (audit type, then fix mode). The wiring audit inspects frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof. The quality audit measures and removes maintainability debt without changing behavior. The security audit hunts exploitable authentication, authorization, tenancy, input-handling, secrets, and data-exposure defects. The live user flow audit drives the real deployed site through every feature end to end with browser control plus shell access to the host, in reviewed chunks. The missed-features assessment walks pages and UI components one by one, proposes possible interactions based on existing product capabilities, and records the user's decision for each proposal.
---

# Complete UI Audit, Code Quality Audit, Security Audit, Live User Flow Audit, and Missed-Features Assessment

## Purpose

This skill supports five deliberately different audit types:

1. **API wiring audit** — inspect frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof for defects or coverage gaps.
2. **Code quality audit** — measure and reduce maintainability debt (duplication, dead code, complexity, inconsistent patterns, unsafe type escapes, missing error handling) without changing observable behavior.
3. **Security audit** — find exploitable authentication, authorization, tenancy/isolation, input-handling, secret-management, and data-exposure defects, with a reproducible probe for each claim.
4. **Live user flow audit** — drive the *deployed* application through every user-facing feature end to end, with browser control over the live domain and shell access to the host, proving that what ships actually works in the right order. Executed in reviewed chunks.
5. **Missed-features assessment** — inspect each page and UI component one by one and propose possible missing interactions, buttons, tools, states, and affordances based on the existing features already available on that surface. The user decides whether each proposal is needed, intentionally omitted, or deferred.

Do not mix these audit types. A feature suggestion is not an API-wiring defect, a wiring gap is not automatically a missing product feature, a maintainability observation is not a security vulnerability, a vulnerability is not a style nit, and a live-flow failure is not automatically a wiring defect. Report each finding under exactly one branch.

When several types are selected, run them in this order — each later branch consumes the earlier map, and behavior-changing fixes land before refactors:

1. Live user flow audit
2. API wiring audit
3. Security audit
4. Code quality audit
5. Missed-features assessment

The live user flow runs first because it produces the ground truth: the actual inventory of what the product does, in the order a real user does it, with the real failures attached. The static branches then explain and generalize what the live run found.

## Required mode selection

At the beginning of every `/audit-loop` run, ask these questions in this order using structured questions.

### Question 1 — audit type

Ask:

> What kind of audit should this run perform?

Options (multiple selections allowed):

- **Live user flow audit (Recommended)** — drive the deployed app end to end on the live domain, with browser control plus host access, in user-reviewed chunks.
- **API wiring audit** — inspect frontend/backend wiring, authorization, persistence, state transitions, privacy, and browser proof.
- **Code quality audit** — measure and reduce maintainability debt without changing behavior.
- **Security audit** — hunt exploitable authentication, authorization, tenancy, input, secret, and data-exposure defects.
- **Missed-features assessment** — walk through every page and UI component one by one and ask the user to decide on possible additional interactions.

Do not proceed until the user chooses at least one. If several are selected, run them in the order above, each as a separately labeled phase with its own ledger.

### Question 2 — fix mode

After the audit type is selected, ask:

> How should confirmed fixes be handled?

Options:

- **Manual fix mode (Recommended)** — report findings and proposed changes, then ask for confirmation before modifying application code.
- **Automatic fix mode** — repair confirmed in-scope defects automatically after discovery, while still asking the user to decide every missed-feature proposal.

The fix-mode choice controls confirmed defects and approved feature additions only. It never permits silently implementing a feature suggestion that the user has not approved, and it never permits a security fix that weakens an existing control to make a test pass.

If the user explicitly says “just fix it,” “commit directly,” or equivalent, automatic fix mode may be selected without another confirmation question, but the audit-type question is still mandatory unless the user already specified it.

**Chunking rule (mandatory for Branch E, both fix modes).** Automatic fix mode in a live user flow audit is *never* a single unattended run. The branch always works in chunks and always stops for the user's go sign between chunks — see Branch E. Automatic mode means "decide and fix without asking per finding", not "run unattended until the end". A single-session sweep of a whole live product is not achievable within a coherent context window, so the chunk boundary is a correctness requirement, not a courtesy.

## Project files

Defaults, configurable per project:

| File | Purpose |
|---|---|
| `docs/ui-tree.md` | Route/component/endpoint inventory and per-unit wiring tree (shared by all branches). |
| `docs/audit-progress.md` | Run log: audit ID/date, types, fix mode, scope, commands, pass counts, evidence, unproven cells. Legacy projects may keep using `docs/ui-audit-progress.md` — continue that name if it already exists. |
| `docs/wiring-audit-findings.md` | API wiring ledger. |
| `docs/code-quality-audit-findings.md` | Code quality ledger (baseline vs final measurements, debt classification). |
| `docs/security-audit-findings.md` | Security ledger (severity, exploitability, probe, status). |
| `docs/missed-features-assessment.md` | Missed-features ledger and per-proposal decisions. |
| `docs/live-flow-audit.md` | Branch E state file: environment, identities, flow inventory, chunk plan, per-chunk verdicts, defect ledger, resume instructions. The single document a fresh session reads to continue. |
| `docs/live-flow-findings.md` | Branch E live defect ledger (`LF-001`…), with the flow, the exact reproduction, the observed vs expected result, the host-side proof, and status. Optional — the state file may hold the ledger if the project prefers one file. |
| `docs/browser-tools.md` | How to launch the project's browser runtime for proof (when present). |

## Shared invariants

- Run the selected audit type(s) completely; do not stop at the first page, file, or finding.
- Inspect the current working tree before consequential changes. Preserve unrelated edits and generated artifacts; never reset, stash, or stage unrelated work.
- Never treat a clean build, render-only smoke, absence of console errors, or a green typecheck as proof of persistence, mutation behavior, authorization, privacy, caching, security, or failure handling.
- Classify each result as `confirmed bug`, `confirmed defect`, `missing coverage`, `intentional behavior`, `approved feature`, `deferred feature`, `unproven`, `dead`, `mock`, or `unknown` — using only the labels that apply to that branch. “Not observed” is never “passed.”
- Every finding carries: location, evidence (cite + excerpt or probe output), impact, classification, and proof status.
- Preserve historical findings and stable IDs in the project audit documents. Append a new dated run; never rewrite prior history.
- Do not use external reference E2E tests as production test artifacts.
- Do not invent domain behavior, identities, data, permissions, or product commitments from a visual reference.
- Do not implement a missed-feature proposal until the user classifies it as needed/approved.
- Do not commit, push, deploy, reset, stash, or stage broadly unless the user explicitly requests it.
- In Branch E, a live environment is the user's real system. Never delete, bulk-modify, or irreversibly mutate data you did not create in this run; never restart, redeploy, roll back, or reconfigure a service without explicit per-instance approval; never print secrets, tokens, session cookies, or personal data into the ledger — record the credential name and redact the value.

---

# Branch A — API wiring audit

Use this branch when the user selects **API wiring audit**.

## Discovery phase

Before changing application code:

1. Run `git status --short --branch` and record the baseline.
2. Enumerate all frontend routes/pages, layouts, loading/error boundaries, shared components, hooks, utilities, API modules, backend routes, controllers/views, presenters/serializers, models, policies, middleware, migrations, signals/tasks, external integrations, cache paths, and relevant tests.
3. Refresh `docs/ui-tree.md` while preserving stable IDs and historical entries.
4. Build a global wiring inventory. For every unit, list every control, datum, read/write path, permission check, persistence effect, external integration, and proof status.
5. For every read, trace:

   `UI field → wrapper/visit → URL/method/query → auth/role → validation → controller/service → model/relation → presenter/response → frontend render/fallback`.

6. For every write, trace:

   `control → disabled/loading state → URL/method/content type → payload → auth/ownership → validation → transaction/persistence → events/jobs/cache → response/flash → reload-visible result`.

7. Inspect empty, loading, malformed, 4xx, 5xx, timeout, retry, refresh, duplicate, stale, inactive, archived, deleted, responsive, keyboard, RTL/LTR, and privacy cells as applicable.
8. Perform mandatory searches for wrapper/route mismatches, field/presenter mismatches, catches/fallbacks, mocks/hardcoded data, dead controls/routes, authorization gaps, cache invalidation, pagination, lifecycle transitions, reverse relations, and status-only tests.

Discovery must be completed across all mapped units before repairs are narrowed to individual findings.

## Repair phase

- In manual fix mode, present the confirmed defect/coverage ledger and ask before changing code.
- In automatic fix mode, repair confirmed in-scope defects after the global ledger is complete.
- Add focused regressions for every repair. Do not weaken or delete existing tests.
- Re-run affected unit, feature, build, type/lint, translation, accessibility, responsive, and browser checks.
- Keep missing coverage and environmental limits explicitly unproven.

## API audit completion criteria

The API wiring branch is complete only when:

- Every mapped unit has an inventory and state-matrix result.
- Every control and datum has a traced contract or an explicit classification.
- Every confirmed defect has a fix and matching regression, or a documented intentional decision.
- Browser proof distinguishes implementation failures from harness/environment failures.
- Unproven cells, deployment limits, concurrency gaps, and product/schema decisions are listed.
- `docs/audit-progress.md` and `docs/wiring-audit-findings.md` contain the complete audit record.

---

# Branch B — Security audit

Use this branch when the user selects **Security audit**.

## Goal

Find defects an attacker could actually use: authentication, authorization and tenancy isolation, input handling, secret management, data exposure, abuse resistance, and configuration. Prefer provable exploit paths over theory, and prove denial of access as deliberately as you prove access.

## Rules of engagement

- **Non-destructive and authorized.** Probe only local, staging, or self-owned instances. Never attack production, a third party, or real user data. No destructive payloads, no denial-of-service, no brute force, no data exfiltration beyond the minimum needed to prove the issue.
- Prove leakage with the least data that settles it (a count, a redacted field, a single row you created). Never paste real secrets, tokens, or personal data into the ledger; record the credential name and redact the value.
- Rotate any credential that was committed or exposed; record the action taken, not the value.
- Severity is impact × exploitability, not code aesthetics. Always state who can reach the defect: anonymous, any authenticated user, any member of a tenant, an admin of the same tenant, or only a privileged insider.

## Inventory phase

1. Enumerate every trust boundary: public routes, authenticated routes, role-gated routes, admin routes, webhooks, cron/task endpoints, background jobs, share/public-token endpoints, file uploads and downloads, outbound fetches, third-party callbacks, and the authentication/session layer itself.
2. For every state-changing endpoint, record: required authentication, required role, object ownership rule, tenancy scoping rule, validation rule, and rate limit.
3. Then run the probe set below. Each probe ends as `proved vulnerable`, `proved denied`, `unproven` (with the precondition that would settle it), or `not applicable` (with a reason).

## Probe set

1. **Authentication** — session/token issuance and validation, expiry and revocation, magic-link/OTP replay, password or code reset paths, session fixation, cookie flags (HttpOnly/Secure/SameSite), CSRF protection on state-changing requests, logout invalidation, remember-me semantics.
2. **Authorization** — every state-changing endpoint probed with: no session, wrong role, and a second tenant's object id. Include mass-assignment of role/status/ownership fields, hidden-field writes, IDOR on ids supplied by the client, admin-only routes, and "hidden" UI actions that the API still accepts.
3. **Tenancy isolation** — for read and write paths, prove that a client-supplied id (workspace/tenant/account/record) cannot reach another tenant's data when the server derives the scope from the session, and that any path which trusts a client-supplied scope is closed.
4. **Input handling** — injection (SQL/ORM, template/HTML, header, log), XSS sinks (raw HTML injection, unescaped user content), path traversal, SSRF on server-side fetches of user-supplied URLs, open redirects, unsafe deserialization, file upload type/size/executable handling, and CSV/formula injection on export where applicable.
5. **Secrets and cryptography** — hardcoded keys or tokens, secrets in client bundles, logs, or error messages, committed env files, encryption-at-rest for personal data, hashing vs reversible encryption, HMAC/signature verification (constant-time compare, correct secret, replay window), key rotation, tokens leaked into URLs, referrers, or analytics.
6. **Data exposure** — API responses returning more than the surface needs (tokens, internal ids, personal data, other tenants' rows), stack/SQL detail in errors, public or share-token endpoints' scope, cache keys that mix tenants, and debug/diagnostic endpoints that leak infrastructure detail.
7. **Abuse resistance** — rate limits on authentication, expensive, and outbound-facing routes; webhook replay protection and idempotency for side-effecting operations; pagination caps and unbounded queries; resumable/retryable operations that can double-charge, double-send, or double-write.
8. **Platform and configuration** — dependency advisories for the pinned versions, permissive CORS, missing security headers, TLS assumptions, default credentials, verbose errors in production, and overly broad file or bucket permissions.

## Proof standards

- A finding is `confirmed` only with a reproducible probe: the exact request/action, the observed result, the expected result, and the code path that permits it. Keep the probe in the ledger in a form a reviewer can re-run against a local instance.
- If the defect is only visible in code, classify it `unproven` and state the exact precondition plus the smallest check that would confirm it.
- A negative result ("no IDOR here") still needs the attempt recorded: request, response, and why access was denied.

## Repair rules

- Fix at the boundary, not the call site: if a missing check recurs across sibling endpoints, add the shared guard and sweep every sibling in the same change.
- Add red/green regressions: the probe must fail against the previous code and pass after the fix. For authorization defects, the regression is the cross-tenant or wrong-role attempt being denied.
- Never weaken or delete an existing control to make a test or a UI flow pass; never log a secret to explain a fix.
- Behavior changes that affect real users (session invalidation, stricter validation, rotated credentials) are recorded as breaking and called out explicitly in the report.

## Security completion criteria

The security branch is complete only when:

- Every trust boundary and state-changing endpoint has an authentication/role/ownership/validation classification with evidence.
- Every confirmed vulnerability has a fix plus a matching red/green regression, or an explicitly deferred entry with rationale and risk.
- Non-exploitable and unproven items list their preconditions.
- The ledger contains no unredacted secrets or personal data.
- `docs/audit-progress.md` and `docs/security-audit-findings.md` contain the complete record.

---

# Branch C — Code quality audit

Use this branch when the user selects **Code quality audit**.

## Goal

Measure and reduce maintainability debt across the codebase **without changing observable behavior**. This branch is not a style debate: every finding is backed by a measurement or a concrete future-failure scenario, and every repair is proven behavior-preserving.

## Rules

- **Behavior is frozen.** Contracts, serialized shapes, URL patterns, permissions, and user-visible copy do not change under this branch. If a behavior looks wrong, it belongs to Branch A (wiring) or Branch B (security), not here.
- Prefer deletion over abstraction. Do not introduce an abstraction for a single call site; do not create a shared helper that the codebase then ignores.
- No reformat-the-world commits. Keep each change scoped to one finding and reviewable.
- Remove what a change obsoletes in the same change: dead code, dead exports, obsolete comments, superseded aliases, and tests that only assert the old implementation.

## Measurement phase

1. Record the toolchain first: the project's lint, typecheck/compile, format, test, and build commands, and whether CI enforces them.
2. Establish a **baseline before touching code** — raw numbers, not impressions: file/LOC counts, largest files, duplicate blocks, dead exports, TODO/FIXME/HACK markers, `any`/unsafe-cast/`@ts-ignore` (or the language's equivalent escape hatches), disabled lint rules, swallowed errors, and current test/lint/type output. Record it in the progress doc and keep machine output as an artifact.
3. Map the code into units (reuse `docs/ui-tree.md` units where they exist; otherwise group by module/directory).
4. Run the mandatory searches below over the whole codebase, then classify each hit.

## Mandatory searches

- **Duplication and drift** — the same logic, constant, or validation implemented twice with subtle differences; copy-pasted blocks that have already diverged; two conventions for the same job (two HTTP clients, two date formatters, two error shapes).
- **Dead weight** — unreachable branches, never-called exported functions and components, unused parameters/imports/fields, endpoints or wrappers with no consumer, commented-out code, feature flags that are permanently on or off.
- **Complexity and size** — god files/functions by the project's own thresholds, deep nesting, long parameter lists, boolean-flag arguments, functions doing several unrelated things, duplicated conditionals that a single lookup could replace.
- **Error handling** — swallowed catches, empty fallbacks that fabricate success, errors logged and dropped, missing failure paths for I/O and network calls, retries without backoff or idempotency, cleanup that never runs on the error path.
- **Type and contract safety** — escape hatches (`any`, unsafe casts, non-null assertions, ignored diagnostics) that hide real nullability or shape mismatches; hand-written types duplicating generated ones; validation that exists in one layer and is trusted in another.
- **Data access and resources** — queries in loops (N+1), unbounded list loads, missing indexes for hot filters (as evidenced by query shape), connections/handles/timers not released, synchronous I/O on hot paths, work repeated per request that could be computed once.
- **Naming and structure** — names that mislead about behavior or units, modules whose contents no longer match their name, layer violations (a UI module importing persistence internals), inconsistent placement of new code versus established convention.
- **Test quality** — tests asserting implementation details or mock echoes, tests that cannot fail, snapshot sprawl, missing coverage on branching business rules, duplicated fixtures that drift, skipped tests with no owner.
- **Comments and documentation drift** — comments that contradict the code, docblocks for deleted parameters, README/setup steps that no longer work.

## Classification

- `confirmed defect` — a maintainability problem with a concrete failure mode (a bug waiting to happen, a divergence already causing inconsistent behavior, a resource leak), with the failure scenario stated.
- `debt` — measured but not currently harmful; quantified so the trend can be tracked.
- `intentional` — deliberate, with the reason found in code, docs, or history.
- `unproven` — suspected but not established; state the check that would settle it.
- Severity is blast radius × change risk: how much of the system depends on the code, and how dangerous touching it is.

## Repair rules

- One finding, one focused change, behavior preserved.
- Refactor in verifiable steps, keeping the suite green between steps; never combine a refactor with a behavior fix.
- Every removal is proven un-used (search + build + test), not merely assumed unused.
- Prove behavior preservation: the existing suite green, plus a targeted assertion for any behavior the previous tests did not pin.
- Re-measure the same baseline metric after the repair and record the delta.

## Code quality completion criteria

The code quality branch is complete only when:

- The baseline and final measurements are recorded for every metric that was measured.
- Every finding is classified with evidence and a location, and every `confirmed defect` is fixed or explicitly deferred with rationale.
- No behavior change shipped under this branch without a stated reason and proof.
- Lint, typecheck, tests, and build are green at the end, or the remaining failures are pre-existing and named.
- Remaining debt is listed with the reason it was left.

---

# Branch D — Missed-features assessment

Use this branch when the user selects **Missed-features assessment**.

## Goal

Find potentially useful interactions that are absent from an existing page or component even though the product already has related data, routes, actions, or workflow concepts. This is a product-discovery conversation, not a bug hunt.

The assessor may suggest:

- Missing navigation or contextual links.
- Add/edit/delete/restore/archive/retry/cancel controls.
- Filters, search, sorting, pagination, saved views, clear filters, or deep-link state.
- Preview, compare, print, export, download, copy, share, or “open in related workflow” actions.
- Status transition controls and visible next actions.
- Empty/loading/error/retry/success/disabled states.
- Bulk actions where the existing model and permissions already support them.
- Accessibility affordances: labels, keyboard actions, focus restoration, announcements, and non-color status.
- Locale/theme/direction affordances.
- Responsive/mobile equivalents of desktop interactions.
- Related-record context already available elsewhere in the product.

The assessor must not suggest unrelated features such as billing, booking, subscriptions, public registration, automatic notifications, or other roadmap non-goals unless the user explicitly asks to reconsider product scope.

## Stable one-by-one order

Create the inventory before starting discussion. Use this order unless the user asks for a different order:

1. Public layouts and public pages.
2. Authentication and recovery pages.
3. Primary authenticated layout and pages.
4. Secondary/role-specific layouts and pages.
5. Shared components that are not fully covered by their owning page.
6. Cross-cutting controls: locale, theme, navigation, dialogs, uploads, status chips, empty/error states.

Within each unit, inspect in DOM/product order: page header/navigation, primary action, filters/tabs, forms, lists/cards/tables, row actions, related links, status/state feedback, empty/loading/error states, responsive behavior, and accessibility affordances.

## Per-unit protocol

For each page or component, do all of the following before moving on:

1. Identify the page's purpose, role boundary, route, existing data, existing actions, and related workflows.
2. Enumerate every current control and data-bearing element.
3. Compare the available product capabilities against what the surface exposes.
4. Propose only concrete candidate additions grounded in existing features, routes, data, permissions, or established UI patterns.
5. Present a short numbered list of proposals to the user. Each proposal must include:
   - a concise name;
   - the proposed interaction/tool;
   - why it follows from existing page/product capabilities;
   - any dependency or privacy/authorization concern.
6. Ask the user to classify each proposal:
   - **Needed** — approve it for implementation or the next repair queue.
   - **Intentionally left out** — record it as an explicit product decision; do not implement.
   - **Defer** — record it for a later roadmap item; do not implement now.
   - **Not applicable** — discard it with a reason.
7. Record the user's decisions immediately in the assessment ledger before presenting the next unit.
8. If no candidates exist, record `No additional interaction identified after review` and move on.

Never silently infer “needed” from the user's silence. If the user skips a proposal, mark it `unresolved` and ask again before implementation or before closing the assessment.

## Assessment ledger

Maintain a ledger in `docs/missed-features-assessment.md` unless the user explicitly requests another location. Each unit should include:

```markdown
## Unit: <page or component>

- Route/file:
- Role/access:
- Existing capabilities:
- Existing controls/data reviewed:

| ID | Candidate interaction | Existing capability basis | User decision | Notes/dependencies |
|---|---|---|---|---|
| MF-001 | ... | ... | Needed / Intentionally left out / Defer / Not applicable / Unresolved | ... |
```

Use stable IDs (`MF-001`, `MF-002`, …). Never overwrite prior assessment history; append a new dated run if the same unit is reassessed.

## Missed-feature implementation rules

- In **manual fix mode**, after the one-by-one assessment has finished, show the approved `Needed` list and ask which approved items to implement. Do not modify code during the conversational assessment unless the user explicitly requests an immediate implementation for that item.
- In **automatic fix mode**, automatically implement only proposals classified `Needed`, and only after the entire selected inventory has been assessed. Still ask the user for every unit and every proposal; automatic mode means automatic execution after approval, not automatic product decisions.
- `Intentionally left out`, `Defer`, `Not applicable`, and `Unresolved` items must not change application code.
- New backend-backed capabilities require the API wiring branch's full contract: migration compatibility, authorization, validation, persistence, focused tests, and freshly authored E2E coverage.
- Presentation-only additions still require build, accessibility, responsive, translation, and relevant browser verification.
- Every approved item must have a decision rationale and a proposed acceptance check before implementation.

## Missed-features completion criteria

The branch is complete only when:

- Every inventory unit has been reviewed in order or explicitly marked out of scope.
- Every proposal has a user decision; no silent approvals.
- The ledger distinguishes approved, intentionally omitted, deferred, not-applicable, and unresolved ideas.
- Approved implementation work is separated from discovery and has acceptance checks.
- Backend-backed approvals are promoted into the API wiring contract and receive focused tests/E2E.
- `docs/missed-features-assessment.md` records the full dated run and remaining deferred ideas.

---

# Branch E — Live user flow audit

Use this branch when the user selects **Live user flow audit**. It is documented last but runs first when selected together with other branches, because it establishes the ground truth the static branches then explain.

## Goal

Drive the application **as it is actually deployed** — on the real domain, against the real backend, real database, real cache, real queue — through every user-facing feature, end to end, and prove that each one works, that each thing connects to the thing it must connect to, and that steps happen in the right order.

This branch is the ground truth for the product. It is not a smoke test, not a render check, and not a re-run of the project's local E2E suite against localhost. Its distinguishing property is that it has both halves of the system available at once:

- **Browser control over the live surface** — the real domain, the real TLS, the real CDN/proxy, the real cookies, the real redirects, the real responsive behavior.
- **Shell access to the host running it** — so a browser-observed symptom can be confirmed, refuted, or explained from the server side: container health, service logs, database rows, queue state, cache, migrations, environment, disk, and the deployed revision.

The point of the pairing is causality. "The booking form did nothing in the browser" is a symptom; the backend 500 in the container log plus the row that was never written plus the queued job that never ran is a diagnosis. A finding recorded from only one half is `unproven` until the other half agrees.

## Preflight

Before any flow runs, establish and record all of this. Do not start testing until every item is either confirmed or explicitly waived by the user.

1. **Live surface** — the exact public URL(s) under test, including `www`/apex, locale prefixes, and any environment differences. Confirm it resolves and serves the expected build.
2. **Host access** — the ssh target, the user, and confirmation that you can reach it non-interactively. Verify the deployment topology from the host: which containers/services run, which compose project, which proxy/ingress fronts them.
3. **Deployed revision vs local revision** — the commit sha the live stack is running, compared with the local working tree. Every flow result is relative to a revision; record it once and re-check it if the deployment changes mid-audit. A fix verified locally but not deployed is `unproven live`, never `passed`.
4. **Identities** — the account(s) for each role the flows need (anonymous, customer, owner, employee, staff, admin/superadmin, plus any second tenant/business needed to test isolation and cross-account denial). For each: how to authenticate on the live surface, which flows it may safely run, and which data it owns. **Prefer dedicated audit accounts over real user accounts.** If only real accounts exist, say so explicitly and get the user's consent for any flow that mutates their data.
5. **Data safety contract** — which flows are read-only; which create data (and how that data is later cleaned up or left tagged as audit residue); which are explicitly forbidden (mass delete, payment, message dispatch to real people, permission/role changes to real staff, anything irreversible). Write this contract into the state file and follow it without re-asking per flow.
6. **Server-side observation recipes** — the concrete, already-validated commands for: service/container status, recent logs for the frontend and backend, database read access, queue/worker state, cache state, migration state, and disk. Validate each one during preflight. A recipe that fails at finding-time is an environment blocker, not a product defect.
7. **Browser runtime** — which browser harness is available, its viewport, whether it can reach the live domain, and whether it can be told apart from a local run. Confirm by loading a known live page and comparing a live-only marker.
8. **Baseline health** — before the first flow, record that the live app is healthy (services up, key public pages load, no pre-existing error storm in the logs). Without this baseline, later log noise cannot be attributed.

## Flow inventory

Build the inventory **before** testing, in real user order, and write it to the state file. Inventory is derived from the product itself — the live nav, route table, role dashboards, and the existing `docs/ui-tree.md` when present — not from imagination. Mark each candidate flow with a stable ID (`LF-F01`, `LF-F02`, …) and give it:

- **Actor / role** and **entry point** (URL or how the user reaches it).
- **Preconditions** — what must already be true, including prior flows in the same session that produce that state.
- **Steps** — the actual interaction sequence, in order.
- **Expected result** — including the *order* of observable effects: redirect target, DB write, notification/queue side effect, cache invalidation, and what the next page must show. "Everything happens in the right order" is the explicit target, so state ordering expectations per flow, not just a final state.
- **Server-side assertion** — what must be visible on the host afterwards (row present/absent, log line, job processed).
- **Cleanup** — none, or the exact reversal.
- **Verdict** — `pass` / `fail` / `partial` / `blocked` / `unproven` / `not applicable`.

Order the inventory the way a person actually uses the product: anonymous discovery and marketing surfaces → authentication and account recovery → primary authenticated journey end to end → secondary and role-specific journeys → cross-cutting behavior (locale, theme, direction, responsive, notification delivery, permissions, empty/error/loading states). Dependencies are explicit: a later flow that needs an earlier flow's output declares it, and the earlier flow's result gates it.

## Chunking

**A live user flow audit always runs in chunks, in both fix modes, including automatic fix mode.** The user reviews each completed chunk and gives an explicit go sign before the next chunk starts.

Design chunks so that:

- Each chunk is one coherent slice of the product — a journey, a role's surface, or a functional area — not an arbitrary page count. A chunk ends where a user would say "that's a feature."
- Each chunk fits comfortably in one fresh context window, including its ledger updates and report. When in doubt, make the chunk smaller. A chunk that will not fit is guaranteed to degrade, and a degraded chunk produces false findings.
- Each chunk has a bounded number of flows (a rough guide: 8–15 flows, or one role-journey) so the ledger stays reviewable.
- Flows that share state and depend on each other stay in the same chunk; splitting a precondition from its consumer produces false `fail` verdicts.
- The final chunk is reserved for cross-chunk checks: anything that only breaks when two journeys meet (e.g. an entity created in chunk 2 edited in chunk 6).

Present the full chunk plan up front, in the state file, and let the user reorder or resize it before chunk 1 starts. Chunks are numbered and fixed; the go sign advances the pointer to exactly one next chunk.

### State file format

`docs/live-flow-audit.md` is the handoff surface. Use this structure:

```markdown
# Live User Flow Audit

- Run ID / started / last updated:
- Live URL(s):            https://app.example.com  (www/apex/locale variants)
- SSH host:               user@host   (topology: <what runs where>)
- Deployed revision:      <sha>   (local tree: <branch @ sha + dirty?>)
- Browser harness / viewport:
- Fix mode:               manual | automatic  (chunked, go sign per chunk)
- Baseline health:        services up / public pages load / log state

## Identities
| Role | Account | How to authenticate live | Data owned | Flows allowed |
|---|---|---|---|---|

## Data-safety contract
- Read-only flows: ...
- Flows that create data: ... (cleanup: ...)
- Forbidden without explicit approval: ...

## Server-side recipes (validated)
- containers: <cmd>
- backend logs: <cmd>
- db read: <cmd>
- queue / cache / migrations: <cmd>

## Flow inventory
| ID | Flow | Actor | Entry | Preconditions | Expected result (incl. ordering) | Server assertion | Cleanup | Verdict | Chunk |
|---|---|---|---|---|---|---|---|---|---|

## Chunk plan
| Chunk | Goal | Flows | Status |
|---|---|---|---|
| 1 | ... | LF-F01..LF-F08 | pending |

## Defect ledger
| ID | Flow | Severity | Symptom | Host-side proof | Root cause | Fix | Live verification | Status |
|---|---|---|---|---|---|---|---|---|

## Chunk reports
### Chunk 1 — <goal>  (go sign: <yes/no + date>)
<verdicts, evidence, fixes, unproven, data left, next chunk>

## Next up
- Chunk: N — <goal>
- First flow: LF-Fxx (<one line: what to do first>)
- Open questions for the user:
```

### The chunk loop

For each chunk, in both fix modes:

1. **Announce** the chunk id, its flows, and its goal in one short block. Do not re-ask about scope.
2. **Execute** every flow in the chunk, in order, and record the verdict as you go. Capture evidence at the moment of the result: the URL, the visible state, the request/response that mattered, the host-side observation. Evidence captured after the fact is reconstruction, and label it as such.
3. **Confirm every failure on the host side** before recording it as a product defect. If the browser shows a failure and the server shows nothing wrong, that is still a real defect (frontend, proxy, TLS, cookie, caching) — classify it that way rather than dismissing it.
4. **In automatic fix mode**, fix the confirmed in-scope defects from this chunk as you go: local code fix, focused regression, deploy, re-run the exact failing flow, and record the before/after. In manual fix mode, collect and present them; do not touch application code.
5. **Update the state file** before reporting: verdicts, new defect entries with stable IDs, flows that remain unproven, and data left behind by the chunk.
6. **Stop and report.** Do not begin the next chunk. The report is the review artifact:

   - chunk id, goal, and the flows covered with one-line verdicts;
   - every `fail` / `partial` with the smallest reproduction, observed vs expected, host-side proof, and its `LF-###` ID;
   - everything fixed in this chunk (in automatic mode) with the commit/deploy and the re-run result;
   - unproven items and why, each with the one check that would settle it;
   - data created or left behind, and its cleanup status;
   - the next chunk's id and its flow list, so the user can approve it with full knowledge;
   - the resume line, so a fresh session can continue.

7. **Wait for the go sign.** Then advance the pointer and start only the next chunk. If the user asks to change the plan (merge, split, reorder, drop flows), update the plan first, then proceed. If the user replies with fixes, batch them, re-verify the affected flows, and re-report before advancing.

Never: run two chunks in one go sign, run ahead "while waiting", or treat silence as approval. When the user explicitly says "keep going without stopping", honor it for the remaining chunks but still emit a report at every chunk boundary so the trail exists.

### Resuming in a fresh session

A chunk boundary is designed to be a session boundary. `docs/live-flow-audit.md` must be sufficient to resume with **no conversational memory**: environment, identities, data-safety contract, full flow inventory with preconditions, the chunk plan, every verdict so far, the defect ledger with statuses, the deployed revision, cleanup state, and an explicit "next up" block naming the next chunk and its first flow. At the end of every chunk, verify that a fresh reader could continue correctly; if not, the state file is not finished. Suggest the `context-pack` skill when the resuming session needs the source of a specific defective flow.

## Per-flow protocol

For every flow:

1. State the actor, entry point, and preconditions; verify preconditions actually hold before starting.
2. Perform the steps in the live browser, in order. Watch for the failure modes that only appear live: expired session mid-flow, redirect to login losing the intended destination, cookie flags, cross-origin/CORS behavior through the real proxy, CDN-cached stale assets, service-worker caching, lazy-loaded chunks failing, real mobile viewport behavior, RTL rendering, Persian digits and calendar.
3. At the decision point, assert the **order** of effects, not just the end state: UI acknowledgement → API success → DB write → job enqueued → job processed → cache invalidated → next page reflects it. Name explicitly any step that fired out of order or not at all.
4. On failure, gather the host-side observation immediately: relevant service logs around the request timestamp, the row state, the queue, the cache. Use the preflight recipes. Correlate by timestamp.
5. Classify the result. `fail` requires a reproduction someone else can repeat. `blocked` means the environment stopped you (missing credential, unreachable host, deployment in progress) and names the blocker. `unproven` means you could not settle it and names the check that would.
6. Re-run any `fail` once to rule out flake, and record whether it reproduced. A non-reproducing failure is `unproven (flaky)`, not a pass.

## Cross-cutting checks

Include these inside the relevant chunks rather than as a separate pass: authentication and session lifecycle (login, refresh, logout invalidation, expired-mid-flow); role and permission boundaries (each role's surface, and a denied case for each role-gated capability); cross-tenant/cross-account isolation on the live surface; empty / loading / error / retry states; validation and error message surfacing; form double-submit and duplicate writes; pagination and sorting; search and filters; file upload and media display; notifications and their delivery; localization and RTL; responsive behavior at mobile width; keyboard reachability of the primary action.

## Fixing live defects

- Fixes are made in the repository, not on the host. Never hand-edit files in a running container or edit the live database to make a flow pass; record the required change and apply it properly, or fix it locally and report that the live verification is pending a deploy.
- Treat the live stack as read-mostly. Deploy, restart, migrate, scale, or reconfigure only with explicit approval for that specific instance, and prefer the project's normal deploy path.
- A fix is `verified live` only after a deploy *and* a re-run of the exact flow that failed. Until then it is `fixed, awaiting live verification`. Say which one it is; never report an unverified fix as closed.
- When a fix changes behavior for real users (data shape, permissions, validation, session handling), call it out as breaking in the report.

## Branch E completion criteria

The branch is complete only when:

- The flow inventory covers every user-facing feature reachable on the live surface, each with a verdict; anything deliberately out of scope is listed with a reason.
- Every chunk was executed and reviewed, with a go sign recorded for each transition.
- Every `fail`/`partial` is either fixed and re-verified live, or carries an explicit decision to defer, with the reason.
- Every defect was confirmed host-side, or is recorded as `unproven` with the settling check named.
- Cleanup state is accurate: what the audit created on the live system, what was removed, what remains and why.
- The data-safety contract held; no unauthorized or irreversible live action was taken.
- `docs/live-flow-audit.md` records the full run and a final summary table, and `docs/live-flow-findings.md` (if used) holds the complete ledger with terminal statuses.

---

# Documentation and reporting

For every run, report:

- Selected audit type(s) and fix mode.
- Scope/inventory counts and files inspected.
- Every finding or feature proposal with classification and evidence.
- Files changed, if any, separated from pre-existing worktree changes.
- Exact verification commands and results.
- Browser runtime, projects, and viewport evidence where applicable.
- Baseline versus final measurements for a code quality audit.
- Severity, exploitability, probe, and status for a security audit.
- For a live user flow audit: the live URL and host, the deployed revision, the chunk id and its flow verdicts, the confirmed defects, the fixes and whether each is `verified live` or `awaiting live verification`, the audit data left on the live system, and the next chunk awaiting a go sign.
- Unproven cells and environmental limitations.
- Remaining repair/feature queue and next order.

Do not claim the project is complete when unresolved or unproven cells remain. Do not commit, push, deploy, reset, stash, or stage broadly unless the user explicitly requests it.
