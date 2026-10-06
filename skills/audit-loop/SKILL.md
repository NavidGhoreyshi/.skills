---
name: audit-loop
description: Choose between a complete API wiring audit, a code quality audit, a security audit, a live user flow audit against the deployed app, an onboarding audit against the deployed app, and a user-guided missed-features assessment. Ask two setup questions first (audit type, then fix mode). The wiring audit inspects frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof. The quality audit measures and removes maintainability debt without changing behavior. The security audit hunts exploitable authentication, authorization, tenancy, input-handling, secrets, and data-exposure defects. The live user flow audit drives the real deployed site through every feature end to end with browser control plus shell access to the host, in reviewed chunks. The onboarding audit drives the deployed app through the new-user journey from first touch to first value moment. The missed-features assessment walks pages and UI components one by one, proposes possible interactions based on existing product capabilities, and records the user's decision for each proposal.
---

# Complete UI Audit, Code Quality Audit, Security Audit, Live User Flow Audit, Onboarding Audit, and Missed-Features Assessment

## Purpose

This skill supports six deliberately different audit types:

1. **API wiring audit** — inspect frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof for defects or coverage gaps.
2. **Code quality audit** — measure and reduce maintainability debt (duplication, dead code, complexity, inconsistent patterns, unsafe type escapes, missing error handling) without changing observable behavior.
3. **Security audit** — find exploitable authentication, authorization, tenancy/isolation, input-handling, secret-management, and data-exposure defects, with a reproducible probe for each claim.
4. **Live user flow audit** — drive the *deployed* application through every user-facing feature end to end, with browser control over the live domain and shell access to the host, proving that what ships actually works in the right order. Executed in reviewed chunks.
5. **Onboarding audit** — drive the *deployed* application through the new-user journey from first touch (landing, signup, verification) through first meaningful use (first booking, first booking received, first value moment), with browser control over the live domain and shell access to the host. Measures time-to-value, drop-off points, cognitive load, trust signals, and the *promise-to-delivery* gap. Executed in reviewed chunks.
6. **Missed-features assessment** — inspect each page and UI component one by one and propose possible missing interactions, buttons, tools, states, and affordances based on the existing features already available on that surface. The user decides whether each proposal is needed, intentionally omitted, or deferred.

Do not mix these audit types. A feature suggestion is not an API-wiring defect, a wiring gap is not automatically a missing product feature, a maintainability observation is not a security vulnerability, a vulnerability is not a style nit, and a live-flow failure is not automatically a wiring defect. Report each finding under exactly one branch.

When several types are selected, run them in this order — each later branch consumes the earlier map, and behavior-changing fixes land before refactors:

1. Live user flow audit
2. Onboarding audit
3. API wiring audit
4. Security audit
5. Code quality audit
6. Missed-features assessment

The live user flow runs first because it produces the ground truth: the actual inventory of what the product does, in the order a real user does it, with the real failures attached. The onboarding audit runs second because it zooms in on the new-user slice of that ground truth — measuring time-to-value, drop-off, cognitive load, and the promise-to-delivery gap — before the static branches explain and generalize what both live runs found.

## Required mode selection

At the beginning of every `/audit-loop` run, ask these questions in this order using structured questions.

### Question 1 — audit type

Ask:

> What kind of audit should this run perform?

Options (multiple selections allowed):

- **Live user flow audit (Recommended)** — drive the deployed app end to end on the live domain, with browser control plus host access, in user-reviewed chunks.
- **Onboarding audit** — drive the deployed app through the new-user journey from first touch (landing, signup, verification) through first meaningful use, measuring time-to-value, drop-off points, cognitive load, trust signals, and the promise-to-delivery gap.
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

### Question 3 — live deployment authority (Branch E only)

When the selected audit type includes the live user flow audit, ask this. It is mandatory, and asked on **every run, every time** — never cached, never carried over from a previous chunk or session.

> May this run push commits and deploy to the live environment in order to verify fixes?

Options:

- **No — report only (default)** — fixes are committed on the working branch and every one is recorded as `fixed, awaiting live verification`. Nothing reaches production. Correct whenever the environment has real users, real data, or any consequence for being wrong.
- **Yes — push and deploy to verify** — the run may commit, push, deploy, and re-run the failing flow to reach `verified live`. Only for an environment the user controls and is willing to have changed by an autonomous loop.

This is asked because whether an unattended model may deploy to production is not a property the skill can infer. A zero-user environment absorbs a nonstop tweaking agent; one with live customers does not, and a run that assumes the former on the latter is an incident. The answer belongs to the user, per run.

- **No** — the run never pushes, deploys, restarts, migrates, or reconfigures the live host. Each defect is reported with the exact flow to re-run once the user deploys.
- **Yes** — the project's normal deploy path only. Still no hand-editing a running container, no editing the live database to force a pass, and no restarts or reconfiguration outside a deploy. Report every deploy with its sha.

The answer never carries forward: a later chunk, session, or run asks again, because the environment may have gained real users since. The state file records it as history, not as standing permission.

**Chunking rule (mandatory for Branch E and Branch F, both fix modes).** Automatic fix mode in a live user flow audit or onboarding audit is *never* a single unattended run. Each branch always works in chunks and always stops for the user's go sign between chunks — see Branch E and Branch F. Automatic mode means "decide and fix without asking per finding", not "run unattended until the end". A single-session sweep of a whole live product is not achievable within a coherent context window, so the chunk boundary is a correctness requirement, not a courtesy.

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
| `docs/onboarding-audit.md` | Branch F state file: environment, identities, persona scripts, first-value definitions, onboarding flow inventory, chunk plan, per-chunk verdicts, defect ledger, measurements ledger, resume instructions. The single document a fresh session reads to continue. |
| `docs/onboarding-findings.md` | Branch F defect ledger (`ONB-001`…), with the flow, persona, exact reproduction, observed vs expected, host-side proof, measurements (time, steps, hesitations, errors, help clicks, back uses, drop-off step), and status. Optional — the state file may hold the ledger if the project prefers one file. |
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

Use this branch when the user selects **Live user flow audit**. It is documented last but runs first, because it establishes the ground truth the other branches then explain.

## Goal

Drive the application **as deployed** — real domain, real backend, real database, real cache, real queue — through every user-facing feature end to end, and prove each one works, connects to what it must connect to, and happens in the right order.

Not a smoke test, not a render check, not the local E2E suite against localhost. What makes it different is that both halves are available at once:

- **Browser control over the live surface** — real domain, TLS, proxy, cookies, redirects, viewport.
- **Shell access to the host** — container state, service logs, rows, queue, cache, migrations, environment, deployed revision.

The pairing is what buys causality. "The booking form did nothing" is a symptom; a 500 in the container log beside a row that was never written and a job that never ran is a diagnosis. A finding seen from one half alone is `unproven` until the other agrees.

## Preflight

Record all of this before any flow runs; do not test until each item is confirmed or explicitly waived.

1. **Live surface** — the exact URLs under test, including apex/`www` and locale variants. Confirm it serves the expected build.
2. **Host access** — ssh target and user, reachable non-interactively; the topology behind it (which containers, which compose project, which proxy fronts them).
3. **Deployed revision vs local tree** — the sha the live stack runs, against the local working tree. Every verdict is relative to a revision; re-check if the deployment changes mid-audit. A locally-fixed, undeployed defect is `unproven live`, never `passed`.
4. **Identities** — one account per role the flows need, plus a second tenant/business for isolation and denial tests. For each: how it authenticates live, which flows it may run, what data it owns. **Prefer dedicated audit accounts over real ones**; if only real accounts exist, say so and get consent before any flow mutates their data.
   - Audit accounts must be purpose-made and unable to reach a real person: use a reserved test range or a domain the user controls, and **never trigger a real outbound message** to prove one works. If signup or verification sends SMS, email, or push, do not walk that path to "confirm" the account — mint it server-side, seed the verified state, and stub outbound delivery. A live audit that texts a stranger is an incident, not a test.
5. **Data-safety contract** — which flows are read-only, which create data (and how it is later cleaned up or left tagged as audit residue), and which are forbidden outright: mass delete, payment, dispatch to real people, role changes to real staff, anything irreversible. Write it into the state file and follow it without re-asking per flow.
6. **Server-side recipes** — the concrete, already-validated commands for container status, frontend/backend logs, database reads, queue, cache, migrations, disk. Validate each during preflight; a recipe that fails later is an environment blocker, not a product defect.
7. **Browser runtime** — which harness, at what viewport, and how to tell a live run from a local one. Confirm by loading a page with a live-only marker.
8. **Deployment authority** — the Question 3 answer for this run, verbatim. It governs every push, deploy, and live data change for the rest of the chunk, and is re-asked at the next boundary.
9. **Baseline health** — services up, key public pages loading, no pre-existing error storm. Without it, later log noise cannot be attributed.

## Flow inventory

Build the inventory **before** testing, from the product itself — live nav, route table, role dashboards, and `docs/ui-tree.md` when present — never from imagination. Give each flow a stable ID (`LF-F01`, …) and record:

- **Actor and entry point** — role, and the URL or path the user takes to reach it.
- **Preconditions** — what must already hold, including prior flows that produce the state.
- **Steps** — the interaction sequence, in order.
- **Expected result** — including the *order* of effects: redirect target, DB write, queue side effect, cache invalidation, what the next page shows. "Happens in the right order" is the explicit target, so state the ordering, not just the end state.
- **Server-side assertion** — what must be visible on the host afterwards: row present or absent, log line, job processed.
- **Cleanup** — none, or the exact reversal.
- **Verdict** — `pass` / `fail` / `partial` / `blocked` / `unproven` / `not applicable`.

Order it the way a person uses the product: anonymous discovery and marketing → authentication and recovery → the primary authenticated journey → secondary and role-specific journeys → cross-cutting behavior. Declare dependencies explicitly: a flow that consumes an earlier flow's output says so, and the earlier verdict gates it.

## Chunking

**This branch always runs in chunks, in both fix modes, including automatic.** The user reviews each chunk and gives an explicit go sign before the next starts. Automatic mode means "decide and fix without asking per finding" — not "run unattended".

Design chunks so that:

- Each is one coherent slice — a journey, a role's surface, a functional area — ending where a user would say "that's a feature", not at an arbitrary page count.
- Each fits in one fresh context window including ledger and report. When in doubt, make it smaller: an oversized chunk degrades and produces false findings.
- Each holds a bounded number of flows (roughly 8–15, or one role-journey) so the ledger stays reviewable.
- Dependent flows stay together. Splitting a precondition from its consumer manufactures false `fail` verdicts.
- The last chunk carries cross-chunk checks: whatever only breaks when two journeys meet.

Present the whole plan up front and let the user reorder or resize it before chunk 1. Chunks are numbered and fixed; a go sign advances the pointer to exactly one chunk.

### State file

`docs/live-flow-audit.md` is the handoff surface. Use this structure:

```markdown
# Live User Flow Audit

- Run ID / started / last updated:
- Live URL(s):            https://app.example.com  (apex/www/locale variants)
- SSH host:               user@host   (topology: <what runs where>)
- Deployed revision:      <sha>   (local tree: <branch @ sha, dirty?>)
- Browser harness / viewport:
- Fix mode:               manual | automatic  (chunked, go sign per chunk)
- Deployment authority:   push+deploy allowed? YES/NO  (re-asked every run and chunk)
- Baseline health:        services up / public pages load / log state

## Identities
| Role | Account | Authenticates live via | Data owned | Flows allowed |
|---|---|---|---|---|

## Data-safety contract
- Read-only: ...
- Creates data: ... (cleanup: ...)
- Forbidden without explicit approval: ...

## Server-side recipes (validated)
- containers: <cmd>   - logs: <cmd>   - db: <cmd>   - queue/cache/migrations: <cmd>

## Flow inventory
| ID | Flow | Actor | Entry | Preconditions | Expected (incl. ordering) | Server assertion | Cleanup | Verdict | Chunk |
|---|---|---|---|---|---|---|---|---|---|

## Chunk plan
| Chunk | Goal | Flows | Status |
|---|---|---|---|
| 1 | ... | LF-F01..LF-F08 | pending |

## Defect ledger
| ID | Flow | Severity | Symptom | Host proof | Root cause | Fix | Live verification | Status |
|---|---|---|---|---|---|---|---|---|

## Chunk reports
### Chunk 1 — <goal>   (go sign: <yes/no, date>)
<verdicts, evidence, fixes, unproven, data left, next chunk>

## Next up
- Chunk: N — <goal>
- First flow: LF-Fxx (<what to do first>)
- Open questions for the user:
```

### Chunk loop

Per chunk, in both fix modes:

1. **Announce** the chunk id, goal, and flows in a few lines. Do not re-ask about scope.
2. **Execute** every flow in order, recording the verdict as you go. Capture evidence at the moment of the result — URL, visible state, the request/response that mattered, the host observation. Evidence gathered afterwards is reconstruction; label it so.
3. **Confirm every failure host-side** before calling it a product defect. A browser failure with a clean server is still a defect (frontend, proxy, TLS, cookie, cache) — classify it as one rather than dismissing it.
4. **In automatic fix mode**, repair this chunk's confirmed in-scope defects as you go: fix, focused regression, deploy if authorized, re-run the exact failing flow, record before/after. In manual fix mode, collect and present; do not touch application code.
5. **Update the state file** before reporting — verdicts, new defects with stable IDs, unproven flows, data left behind.
6. **Stop and report.** Never start the next chunk in the same go sign. The report carries:
   - chunk id, goal, and each covered flow with a one-line verdict;
   - every `fail`/`partial` with the smallest reproduction, observed vs expected, host-side proof, and its `LF-###` ID;
   - what was fixed, with the commit, the sha deployed, and the re-run result;
   - unproven items, each with the one check that would settle it;
   - data created or left behind, and its cleanup status;
   - the next chunk's id and flow list, so the go sign is informed;
   - the resume line.
7. **Re-ask the deployment-authority question** before any chunk that involves a fix. The previous answer is history in the state file, never standing permission.
8. **Wait for the go sign**, then advance exactly one chunk. Plan changes (merge, split, reorder, drop) are applied to the plan before proceeding. Requested fixes are batched, the affected flows re-verified, and re-reported before advancing.

Never run two chunks per go sign, never run ahead "while waiting", never treat silence as approval. If the user says "keep going without stopping", honor it for the remaining chunks but still emit a report at every boundary so the trail exists.

### Resuming in a fresh session

A chunk boundary is designed to be a session boundary. `docs/live-flow-audit.md` must be sufficient to continue with **no conversational memory**: environment, identities, data-safety contract, full inventory with preconditions, chunk plan, every verdict, defect ledger with statuses, deployed revision, cleanup state, and a `## Next up` block naming the next chunk and its first flow. At the end of each chunk, check that a fresh reader could continue; if not, the state file is not finished. Use the `context-pack` skill when the resuming session needs the source behind a specific defective flow.

## Per-flow protocol

1. State actor, entry, and preconditions; verify the preconditions actually hold.
2. Perform the steps live, in order. Watch for what only breaks in production: session expiring mid-flow, login redirect losing the intended destination, cookie flags, CORS through the real proxy, CDN-cached stale assets, service-worker caching, lazy chunks failing, real mobile viewport, RTL and locale rendering.
3. At the decision point, assert the **order** of effects, not the end state: UI acknowledgement → API success → DB write → job enqueued → job processed → cache invalidated → next page reflects it. Name any step that fired out of order or not at all.
4. On failure, take the host observation immediately — logs around the request timestamp, row state, queue, cache — and correlate by timestamp.
5. Classify. `fail` needs a reproduction someone else can repeat. `blocked` names the environment blocker. `unproven` names the check that would settle it.
6. Re-run any `fail` once to rule out flake and record whether it reproduced. A non-reproduction is `unproven (flaky)`, not a pass.

## Cross-cutting checks

Fold these into the relevant chunks rather than a separate pass: session lifecycle (login, refresh, logout invalidation, expiry mid-flow); role boundaries (each role's surface plus a denied case per role-gated capability); cross-account isolation; empty / loading / error / retry states; validation and error surfacing; double-submit and duplicate writes; pagination, sorting, search, filters; upload and media display; notification delivery; localization and RTL; mobile width; keyboard reachability of the primary action.

## Fixing live defects

- Fixes go in the repository, never on the host. No hand-editing a running container, no editing the live database to force a pass.
- **Deployment authority (Question 3) decides whether a fix may ship.** Without it: commit on the working branch, report `fixed, awaiting live verification`, and name the exact flow to re-run after the user deploys — do not report the defect closed. With it: use the project's normal deploy path, report the sha, re-run the failing flow.
- Even with authority the live stack is read-mostly: restarts, migrations, scaling, and config changes happen only as part of a deploy, never as a debugging shortcut.
- A fix is `verified live` only after a deploy **and** a re-run of the failing flow. Otherwise `fixed, awaiting live verification`. Never report an unverified fix as closed.
- Call out behavior changes affecting real users (data shape, permissions, validation, sessions) as breaking.

## Branch E completion criteria

- Every user-facing feature on the live surface has a verdict; anything out of scope is listed with a reason.
- Every chunk was executed and reviewed, with a go sign recorded for each transition.
- Every `fail`/`partial` is fixed and re-verified live, or explicitly deferred with a reason.
- Every defect is confirmed host-side, or recorded `unproven` with the settling check named.
- Cleanup is accurate: what the audit created, what was removed, what remains and why.
- The data-safety contract held; no unauthorized or irreversible live action was taken.
- `docs/live-flow-audit.md` holds the full run and a final summary, and `docs/live-flow-findings.md` (if used) the complete ledger with terminal statuses.

---

# Branch F — Onboarding audit

Use this branch when the user selects **Onboarding audit**. It runs second (after Branch E live user flow) because it narrows the live ground truth to the new-user journey specifically.

## Goal

Drive the application **as deployed** through the *new-user journey* from first touch (landing page, marketing, SEO entry points) through signup, verification, first login, first configuration, to first meaningful value moment (first booking made, first booking received, first payment, first dashboard insight). Measure:

- **Time-to-value** — wall-clock and step count from landing to first value.
- **Drop-off points** — where users stall, abandon, or need external help.
- **Cognitive load** — decisions required, fields filled, concepts explained vs assumed.
- **Trust signals** — security, social proof, guarantees visible at each step.
- **Promise-to-delivery gap** — what marketing/landing promises vs what the product actually delivers in the first session.

Executed in reviewed chunks, with the same browser+host pairing as Branch E.

## Relationship to Branch E

- Uses the same live surface, host access, identities, recipes, and data-safety contract established in Branch E preflight.
- The onboarding flow inventory is a **subset** of the Branch E inventory (the new-user entry path + first-value flows).
- Findings from Branch E that affect onboarding (broken signup, broken email verification, broken first login) are imported as known constraints; they are not re-probed.
- Branch F adds *onboarding-specific* measurements and lenses that Branch E does not: step timers, hesitation points, copy clarity, empty-state quality for brand-new accounts, default/empty configurations, and the "what now?" moment after first value.

## Preflight (re-uses Branch E preflight; add only)

1. **Onboarding entry points** — the exact URLs a brand-new user might land on (apex, `/`, `/landing`, campaign URLs, locale variants, referral links). Confirm each serves the expected build.
2. **Audit accounts** — fresh accounts created *for this run* (never real users). Use the reserved test range or a domain the user controls. **Never trigger a real outbound message** (SMS, email, push) to prove one works — mint server-side, seed verified state, stub outbound delivery. If the product requires a live OTP/SMS to proceed, the audit either (a) uses a seeded test phone with a known code, or (b) records `unproven` for that gate and proceeds with a pre-verified account.
3. **First-value definition** — agree with the user on what "first meaningful use" means for each role: customer (first booking confirmed), business owner (first booking received), employee (first shift seen), admin (first tenant configured). Record it in the state file.
4. **Persona scripts** — 2–4 representative new-user personas with different entry paths and goals (e.g., "mobile customer from Instagram ad", "desktop owner from search", "referred customer with invite link"). Each script names the entry URL, the expected steps, and the first-value target.

## Flow inventory (onboarding-specific)

Build a focused inventory **before** testing, derived from the Branch E inventory plus marketing/landing routes. Give each flow a stable ID (`ONB-F01`, …) and record:

- **Persona and entry point** — which persona, which URL, which campaign/referrer if any.
- **Preconditions** — brand-new account (no prior data), or specific seeded state (invite token, referral code).
- **Steps** — the interaction sequence, in order, including all decisions and inputs.
- **Time budget** — expected max minutes/steps for a motivated user (from user research or heuristic).
- **Expected result** — including the *order* of effects (same standard as Branch E): UI acknowledgement → API success → DB write → job enqueued → job processed → cache invalidated → next page reflects it.
- **Server-side assertion** — what must be visible on the host afterwards.
- **Drop-off risk** — which step is most likely to lose the user (heuristic or data-backed).
- **Cleanup** — none, or exact reversal (delete audit account, purge audit bookings).
- **Verdict** — `pass` / `fail` / `partial` / `blocked` / `unproven` / `not applicable`.
- **Measurements captured** — actual time, actual steps, hesitations (pauses >10s on a field), errors, help clicks, back-button uses.

Order: anonymous landing → signup/verification → first login → first config/wizard → first value → "what now" screen.

## Chunking

Same rules as Branch E: chunks are coherent slices (e.g., "landing → verified account", "first login → first booking"), each fits one context window, dependent flows stay together, go sign per chunk, re-ask deployment authority before any fix that deploys.

### State file

`docs/onboarding-audit.md` (new file, same pattern as `live-flow-audit.md`):

```markdown
# Onboarding Audit

- Run ID / started / last updated:
- Live URL(s):            https://app.example.com  (apex/www/locale/campaign variants)
- SSH host:               user@host   (topology: <what runs where>)
- Deployed revision:      <sha>   (local tree: <branch @ sha, dirty?>)
- Browser harness / viewport:
- Fix mode:               manual | automatic  (chunked, go sign per chunk)
- Deployment authority:   push+deploy allowed? YES/NO  (re-asked every run and chunk)
- Baseline health:        services up / public pages load / log state

## Identities (audit accounts, pre-seeded)
| Role | Account | Authenticates live via | Data owned | Flows allowed |
|---|---|---|---|---|

## First-value definitions
| Role | First-value moment | Success criteria |
|---|---|---|

## Persona scripts
| Persona | Entry URL | Expected steps | First-value target | Time budget |
|---|---|---|---|---|

## Data-safety contract
- Read-only: ...
- Creates data: ... (cleanup: ...)
- Forbidden without explicit approval: ...

## Server-side recipes (validated)
- containers: <cmd>   - logs: <cmd>   - db: <cmd>   - queue/cache/migrations: <cmd>

## Onboarding flow inventory
| ID | Flow | Persona | Entry | Preconditions | Expected (incl. ordering) | Server assertion | Drop-off risk | Cleanup | Verdict | Chunk |
|---|---|---|---|---|---|---|---|---|---|---|

## Chunk plan
| Chunk | Goal | Flows | Status |
|---|---|---|---|
| 1 | Landing → verified account | ONB-F01..ONB-F04 | pending |

## Defect ledger
| ID | Flow | Severity | Symptom | Host proof | Root cause | Fix | Live verification | Status |
|---|---|---|---|---|---|---|---|---|

## Measurements ledger
| Flow | Persona | Actual time | Actual steps | Hesitations | Errors | Help clicks | Back uses | Drop-off step |
|---|---|---|---|---|---|---|---|---|

## Chunk reports
### Chunk 1 — <goal>   (go sign: <yes/no, date>)
<verdicts, evidence, fixes, unproven, data left, next chunk>

## Next up
- Chunk: N — <goal>
- First flow: ONB-Fxx (<what to do first>)
- Open questions for the user:
```

### Per-flow protocol (adds onboarding lens to Branch E)

1. State persona, entry, preconditions; verify preconditions hold (fresh account, no prior data).
2. Start step timer. Perform steps live, in order. Capture:
   - **Hesitation**: pause >10s on a field/decision (record field, duration).
   - **Error**: validation, 4xx, 5xx, timeout, toast, inline message (record exact text).
   - **Help click**: "?", tooltip, docs link, support button (record target).
   - **Back use**: browser back or in-app back from a step (record from→to).
3. At each decision point, assert the **order** of effects (same as Branch E).
4. On failure, take host observation immediately (logs, row state, queue, cache) and correlate by timestamp.
5. Classify. `fail` needs a reproduction. `blocked` names the environment blocker. `unproven` names the settling check.
6. Re-run any `fail` once to rule out flake.
7. Record measurements in the measurements ledger.

## Cross-cutting onboarding checks

Fold into relevant chunks:

- **Landing promise vs delivery** — does the landing page/CTA promise match the first screen after signup?
- **Empty-state quality** — brand-new account sees helpful empty states with CTAs, not blank tables.
- **Default configuration** — sensible defaults pre-filled; user can reach value without a settings detour.
- **Progress visibility** — user knows where they are in the journey (steps left, what's next).
- **Recovery from interruption** — session expiry mid-flow, tab close, back-button, refresh — does the user resume or restart?
- **Trust signals at each gate** — security badges, testimonials, guarantees visible at signup, payment, first booking.
- **Mobile-first** — the primary onboarding path must work at 375px without horizontal scroll or truncated text.
- **RTL/Locale** — Persian/Farsi copy, digit input, calendar, date formats at every step.
- **Accessibility** — labels, focus order, announcements for dynamic steps, keyboard reach of primary CTA.
- **Referral/invite handling** — invite link lands on the right page with pre-filled context; no "invalid token" for valid links.

## Fixing onboarding defects

Same rules as Branch E: fixes in repo, never on host; deployment authority decides if a fix ships; `verified live` only after deploy + re-run; behavior changes called out as breaking.

## Branch F completion criteria

- Every onboarding entry point and first-value flow has a verdict; out-of-scope listed with reason.
- Every chunk executed and reviewed, go sign recorded for each transition.
- Every `fail`/`partial` fixed and re-verified live, or explicitly deferred with reason.
- Every defect confirmed host-side, or recorded `unproven` with settling check named.
- Measurements ledger complete for every persona × flow.
- Cleanup accurate: audit accounts, bookings, data created, removed, remaining.
- Data-safety contract held.
- `docs/onboarding-audit.md` holds the full run, measurements ledger, and final summary.
- `docs/onboarding-findings.md` (optional, if split) holds the defect ledger with terminal statuses.

## Visual HTML report (onboarding audit)

At the end of each chunk and at the final summary, generate a standalone **HTML report** at `docs/onboarding-report-<chunk-id>.html` (per chunk) and `docs/onboarding-report-final.html` (cumulative). The report must be a single file with embedded CSS/JS (no external dependencies) so it can be opened directly in a browser or shared as an artifact.

### Report structure

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <title>Onboarding Audit Report — <project> — Chunk <N> / Final</title>
  <style>
    /* Embedded: CSS custom properties for theming, responsive grid, print styles */
    :root { --bg:#0b1020; --fg:#e8eefc; --muted:#7a8bb8; --accent:#f0b800; --accent-ink:#0b1020; --card:#121830; --border:#223058; --ok:#22c55e; --warn:#f59e0b; --fail:#ef4444; }
    @media (prefers-color-scheme: light) { :root { --bg:#ffffff; --fg:#0b1b3a; --muted:#5a6d8a; --card:#f8faff; --border:#d5ddec; } }
    /* ... rest of embedded styles ... */
  </style>
</head>
<body>
  <header class="report-header">
    <h1>Onboarding Audit — <Project> — <Chunk N / Final></h1>
    <div class="meta">Run ID: <id> | Deployed: <sha> | Live: <url> | Personas: <N> | Flows: <M> | Generated: <ISO timestamp></div>
  </header>

  <!-- 1. EXECUTIVE FUNNEL -->
  <section id="funnel" class="section">
    <h2>Time-to-Value Funnel</h2>
    <div class="funnel-grid">
      <!-- One card per persona: entry → verified → first login → first value -->
      <article class="persona-funnel" data-persona="mobile-customer">
        <header><h3>Mobile Customer (Instagram)</h3><span class="badge">3:42 min</span></header>
        <div class="steps">
          <div class="step ok" data-step="landing" data-time="0:00">Landing</div>
          <div class="step ok" data-step="signup" data-time="0:38">Signup</div>
          <div class="step warn" data-step="verify" data-time="1:12">OTP Verify</div>
          <div class="step ok" data-step="first-login" data-time="1:45">First Login</div>
          <div class="step ok" data-step="first-booking" data-time="3:42">First Booking ✓</div>
        </div>
        <div class="drop-off">Drop-off: OTP Verify (22s hesitation)</div>
      </article>
      <!-- repeat per persona -->
    </div>
  </section>

  <!-- 2. HESITATION HEATMAP -->
  <section id="hesitation" class="section">
    <h2>Hesitation Heatmap (pauses >10s)</h2>
    <table class="heatmap">
      <thead><tr><th>Flow</th><th>Persona</th><th>Field / Decision</th><th>Duration</th><th>Context</th></tr></thead>
      <tbody>
        <tr><td>ONB-F03</td><td>Mobile Customer</td><td>Phone input (OTP)</td><td>22s</td><td>Persian digits not auto-normalized</td></tr>
        <!-- rows from measurements ledger -->
      </tbody>
    </table>
  </section>

  <!-- 3. TRUST SIGNAL CHECKLIST -->
  <section id="trust" class="section">
    <h2>Trust Signals by Gate</h2>
    <div class="gate-grid">
      <article class="gate"><h4>Signup</h4><ul><li class="ok">SSL badge</li><li class="ok">Testimonial</li><li class="fail">Money-back guarantee</li></ul></article>
      <!-- per gate: signup, verify, payment, first booking -->
    </div>
  </section>

  <!-- 4. DEFECT LEDGER -->
  <section id="defects" class="section">
    <h2>Defects (ONB-###)</h2>
    <ul class="defect-list">
      <li class="defect fail" data-id="ONB-003">
        <strong>ONB-003</strong> — OTP verify fails on Persian digits
        <span class="persona">Mobile Customer</span>
        <span class="flow">ONB-F03</span>
        <span class="status">fixed, awaiting live verification</span>
        <details><summary>Reproduction</summary><pre>...</pre></details>
      </li>
    </ul>
  </section>

  <!-- 5. MEASUREMENTS TABLE -->
  <section id="measurements" class="section">
    <h2>Measurements Ledger</h2>
    <table class="measurements">
      <thead><tr><th>Flow</th><th>Persona</th><th>Time</th><th>Steps</th><th>Hesitations</th><th>Errors</th><th>Help clicks</th><th>Back uses</th><th>Drop-off step</th></tr></thead>
      <tbody>
        <tr><td>ONB-F03</td><td>Mobile Customer</td><td>3:42</td><td>7</td><td>2</td><td>1</td><td>0</td><td>1</td><td>OTP Verify</td></tr>
      </tbody>
    </table>
  </section>

  <footer class="report-footer">
    <p>Generated by audit-loop Branch F. <a href="#funnel">Back to funnel</a></p>
  </footer>

  <script>
    /* Embedded: tiny interactions — foldable defect details, persona filter, print-to-PDF hint */
  </script>
</body>
</html>
```

### Generation rules

- **Per chunk**: After each chunk's go sign, write `docs/onboarding-report-chunk-<N>.html` with only that chunk's flows + cumulative defect ledger.
- **Final**: After the last chunk, write `docs/onboarding-report-final.html` with all chunks, all personas, complete measurements ledger, and a summary row per persona (total time, total steps, drop-off step, pass/fail).
- **Data source**: Read `docs/onboarding-audit.md` (state file) and `docs/onboarding-findings.md` (or the defect ledger section within the state file) to populate the report. Do not re-run flows.
- **Styling**: Dark-first (matches the app's dark mode), high contrast, Persian/Farsi RTL support in tables, print stylesheet for PDF export.
- **No external assets**: All CSS/JS inlined. No CDN, no images (use inline SVG for icons/checkmarks).
- **Accessibility**: Semantic HTML, ARIA labels on interactive elements, focus-visible outlines, color-blind safe palette.

### Integration

Add this step to the **Chunk loop** (Branch F):
> 7. **Generate chunk HTML report** — write `docs/onboarding-report-chunk-<N>.html` from the current state file. Commit it alongside the chunk's changes if the user wants history.

Add this step to **Branch F completion**:
> - `docs/onboarding-report-final.html` generated and committed (or offered as artifact).

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
- For a live user flow audit: the live URL and host, the deployed revision, the chunk id and its flow verdicts, the confirmed defects, each fix as `verified live` or `awaiting live verification`, the audit data left on the live system, and the next chunk awaiting a go sign.
- For an onboarding audit: the live URL and host, the deployed revision, the persona scripts, the measurements ledger (time, steps, hesitations, errors, help clicks, back uses, drop-off step per flow), the chunk id and its flow verdicts, the confirmed defects, each fix as `verified live` or `awaiting live verification`, the audit accounts and data left on the live system, and the next chunk awaiting a go sign.
- Unproven cells and environmental limitations.
- Remaining repair/feature queue and next order.

Do not claim the project is complete when unresolved or unproven cells remain. Do not commit, push, deploy, reset, stash, or stage broadly unless the user explicitly requests it.
