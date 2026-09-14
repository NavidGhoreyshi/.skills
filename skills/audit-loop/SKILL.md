---
name: audit-loop
description: Choose between a complete API wiring audit, a code quality audit, a security audit, and a user-guided missed-features assessment. Ask two setup questions first (audit type, then fix mode). The wiring audit inspects frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof. The quality audit measures and removes maintainability debt without changing behavior. The security audit hunts exploitable authentication, authorization, tenancy, input-handling, secrets, and data-exposure defects. The missed-features assessment walks pages and UI components one by one, proposes possible interactions based on existing product capabilities, and records the user's decision for each proposal.
---

# Complete UI Audit, Code Quality Audit, Security Audit, and Missed-Features Assessment

## Purpose

This skill supports four deliberately different audit types:

1. **API wiring audit** — inspect frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof for defects or coverage gaps.
2. **Code quality audit** — measure and reduce maintainability debt (duplication, dead code, complexity, inconsistent patterns, unsafe type escapes, missing error handling) without changing observable behavior.
3. **Security audit** — find exploitable authentication, authorization, tenancy/isolation, input-handling, secret-management, and data-exposure defects, with a reproducible probe for each claim.
4. **Missed-features assessment** — inspect each page and UI component one by one and propose possible missing interactions, buttons, tools, states, and affordances based on the existing features already available on that surface. The user decides whether each proposal is needed, intentionally omitted, or deferred.

Do not mix these audit types. A feature suggestion is not an API-wiring defect, a wiring gap is not automatically a missing product feature, a maintainability observation is not a security vulnerability, and a vulnerability is not a style nit. Report each finding under exactly one branch.

When several types are selected, run them in this order — each later branch consumes the earlier map, and behavior-changing fixes land before refactors:

1. API wiring audit
2. Security audit
3. Code quality audit
4. Missed-features assessment

## Required mode selection

At the beginning of every `/audit-loop` run, ask these questions in this order using structured questions.

### Question 1 — audit type

Ask:

> What kind of audit should this run perform?

Options (multiple selections allowed):

- **API wiring audit (Recommended)** — inspect frontend/backend wiring, authorization, persistence, state transitions, privacy, and browser proof.
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
- Unproven cells and environmental limitations.
- Remaining repair/feature queue and next order.

Do not claim the project is complete when unresolved or unproven cells remain. Do not commit, push, deploy, reset, stash, or stage broadly unless the user explicitly requests it.
