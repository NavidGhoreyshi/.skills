---
name: audit-live-flow
description: Drive the deployed application end to end on the live domain — every user-facing feature in the journey pass, the new-user path to first value in the onboarding pass — pairing live browser control with shell access to the host, and prove what ships actually works in the right order. Use when the user wants a live user flow audit or an onboarding audit (time-to-value, drop-off, trust signals) against the running domain and host, in reviewed chunks — or when `audit-loop` selects this branch.
---

# Live user flow audit

Use this branch when the user selects **Live user flow audit** or **Onboarding audit**. It runs first, because it establishes the ground truth the other audits then explain.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Passes

One skill, two named passes:

- **Journey pass** — what this skill has always done: drive every user-facing feature end to end and prove each one works, connects to what it must connect to, and happens in the right order.
- **Onboarding pass** — drive a new user from first touch to first meaningful value, measuring time-to-value, drop-off, cognitive load, trust signals, and the promise-to-delivery gap. Executed in reviewed chunks, with the same browser+host pairing as the journey pass.

The onboarding pass narrows the live ground truth to the new-user journey specifically:

- It uses the same live surface, host access, identities, recipes, and data-safety contract established in the journey-pass preflight.
- The onboarding flow inventory is a **subset** of the journey-pass inventory (the new-user entry path + first-value flows).
- Findings from the journey pass that affect onboarding (broken signup, broken email verification, broken first login) are imported as known constraints; they are not re-probed.
- The onboarding pass adds *onboarding-specific* measurements and lenses that the journey pass does not: step timers, hesitation points, copy clarity, empty-state quality for brand-new accounts, default/empty configurations, and the "what now?" moment after first value.

## Goal

Drive the application **as deployed** — real domain, real backend, real database, real cache, real queue — through every user-facing feature end to end, and prove each one works, connects to what it must connect to, and happens in the right order.

Not a smoke test, not a render check, not the local E2E suite against localhost. What makes it different is that both halves are available at once:

- **Browser control over the live surface** — real domain, TLS, proxy, cookies, redirects, viewport.
- **Shell access to the host** — container state, service logs, rows, queue, cache, migrations, environment, deployed revision.

The pairing is what buys causality. "The booking form did nothing" is a symptom; a 500 in the container log beside a row that was never written and a job that never ran is a diagnosis. A finding seen from one half alone is `unproven` until the other agrees.

## Goal — onboarding pass

Drive the application **as deployed** through the *new-user journey* from first touch (landing page, marketing, SEO entry points) through signup, verification, first login, first configuration, to first meaningful value moment (first booking made, first booking received, first payment, first dashboard insight). Measure:

- **Time-to-value** — wall-clock and step count from landing to first value.
- **Drop-off points** — where users stall, abandon, or need external help.
- **Cognitive load** — decisions required, fields filled, concepts explained vs assumed.
- **Trust signals** — security, social proof, guarantees visible at each step.
- **Promise-to-delivery gap** — what marketing/landing promises vs what the product actually delivers in the first session.

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

### Preflight additions — onboarding pass

The onboarding pass re-uses the preflight above; add only:

1. **Onboarding entry points** — the exact URLs a brand-new user might land on (apex, `/`, `/landing`, campaign URLs, locale variants, referral links). Confirm each serves the expected build.
2. **Audit accounts** — fresh accounts created *for this run* (never real users). Use the reserved test range or a domain the user controls. **Never trigger a real outbound message** (SMS, email, push) to prove one works — mint server-side, seed verified state, stub outbound delivery. If the product requires a live OTP/SMS to proceed, the audit either (a) uses a seeded test phone with a known code, or (b) records `unproven` for that gate and proceeds with a pre-verified account.
3. **First-value definition** — agree with the user on what "first meaningful use" means for each role: customer (first booking confirmed), business owner (first booking received), employee (first shift seen), admin (first tenant configured). Record it in the state file.
4. **Persona scripts** — 2–4 representative new-user personas with different entry paths and goals (e.g., "mobile customer from Instagram ad", "desktop owner from search", "referred customer with invite link"). Each script names the entry URL, the expected steps, and the first-value target.

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

## Flow inventory — onboarding pass

Build a focused inventory **before** testing, derived from the journey-pass inventory plus marketing/landing routes. Give each flow a stable ID (`ONB-F01`, …) and record:

- **Persona and entry point** — which persona, which URL, which campaign/referrer if any.
- **Preconditions** — brand-new account (no prior data), or specific seeded state (invite token, referral code).
- **Steps** — the interaction sequence, in order, including all decisions and inputs.
- **Time budget** — expected max minutes/steps for a motivated user (from user research or heuristic).
- **Expected result** — including the *order* of effects (same standard as the journey pass): UI acknowledgement → API success → DB write → job enqueued → job processed → cache invalidated → next page reflects it.
- **Server-side assertion** — what must be visible on the host afterwards.
- **Drop-off risk** — which step is most likely to lose the user (heuristic or data-backed).
- **Cleanup** — none, or exact reversal (delete audit account, purge audit bookings).
- **Verdict** — `pass` / `fail` / `partial` / `blocked` / `unproven` / `not applicable`.
- **Measurements captured** — actual time, actual steps, hesitations (pauses >10s on a field), errors, help clicks, back-button uses.

Order: anonymous landing → signup/verification → first login → first config/wizard → first value → "what now" screen.

## Chunking

Design chunks so that:

- Each is one coherent slice — a journey, a role's surface, a functional area — ending where a user would say "that's a feature", not at an arbitrary page count.
- Each fits in one fresh context window including ledger and report. When in doubt, make it smaller: an oversized chunk degrades and produces false findings.
- Each holds a bounded number of flows (roughly 8–15, or one role-journey) so the ledger stays reviewable.
- Dependent flows stay together. Splitting a precondition from its consumer manufactures false `fail` verdicts.
- The last chunk carries cross-chunk checks: whatever only breaks when two journeys meet.

Present the whole plan up front and let the user reorder or resize it before chunk 1. Chunks are numbered and fixed; a go sign advances the pointer to exactly one chunk.

The onboarding pass follows the same rules: chunks are coherent slices (e.g., "landing → verified account", "first login → first booking"), each fits one context window, dependent flows stay together, go sign per chunk, re-ask deployment authority before any fix that deploys.

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

### State file — onboarding pass

`docs/onboarding-audit.md` (same pattern as `live-flow-audit.md`):

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

In the onboarding pass, `fail`/`partial` rows carry `ONB-###` IDs, and each chunk additionally generates its HTML report (see `references/onboarding-report.md`).

### Resuming in a fresh session

A chunk boundary is designed to be a session boundary. `docs/live-flow-audit.md` must be sufficient to continue with **no conversational memory**: environment, identities, data-safety contract, full inventory with preconditions, chunk plan, every verdict, defect ledger with statuses, deployed revision, cleanup state, and a `## Next up` block naming the next chunk and its first flow. At the end of each chunk, check that a fresh reader could continue; if not, the state file is not finished. Use the `context-pack` skill when the resuming session needs the source behind a specific defective flow.

The same holds for the onboarding pass with `docs/onboarding-audit.md`: identities, first-value definitions, persona scripts, measurements ledger, and `## Next up` naming the next chunk and its first `ONB-Fxx` flow.

## Per-flow protocol

1. State actor, entry, and preconditions; verify the preconditions actually hold.
2. Perform the steps live, in order. Watch for what only breaks in production: session expiring mid-flow, login redirect losing the intended destination, cookie flags, CORS through the real proxy, CDN-cached stale assets, service-worker caching, lazy chunks failing, real mobile viewport, RTL and locale rendering.
3. Classify. `fail` needs a reproduction someone else can repeat. `blocked` names the environment blocker. `unproven` names the check that would settle it.

### Per-flow protocol — onboarding lens

Adds the onboarding lens to the protocol above:

1. State persona, entry, preconditions; verify preconditions hold (fresh account, no prior data).
2. Start step timer. Perform steps live, in order. Capture:
   - **Hesitation**: pause >10s on a field/decision (record field, duration).
   - **Error**: validation, 4xx, 5xx, timeout, toast, inline message (record exact text).
   - **Help click**: "?", tooltip, docs link, support button (record target).
   - **Back use**: browser back or in-app back from a step (record from→to).
3. Classify. `fail` needs a reproduction. `blocked` names the environment blocker. `unproven` names the settling check.
4. Record measurements in the measurements ledger.

## Cross-cutting checks

Fold these into the relevant chunks rather than a separate pass: session lifecycle (login, refresh, logout invalidation, expiry mid-flow); role boundaries (each role's surface plus a denied case per role-gated capability); cross-account isolation; empty / loading / error / retry states; validation and error surfacing; double-submit and duplicate writes; pagination, sorting, search, filters; upload and media display; notification delivery; localization and RTL; mobile width; keyboard reachability of the primary action.

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

## Fixing live defects

- **Deployment authority (Question 3) decides whether a fix may ship.** Without it: commit on the working branch, report `fixed, awaiting live verification`, and name the exact flow to re-run after the user deploys — do not report the defect closed. With it: use the project's normal deploy path, report the sha, re-run the failing flow.
- Even with authority the live stack is read-mostly: restarts, migrations, scaling, and config changes happen only as part of a deploy, never as a debugging shortcut.

## Completion criteria

- Every user-facing feature on the live surface has a verdict; anything out of scope is listed with a reason.
- Every chunk was executed and reviewed, with a go sign recorded for each transition.
- Every `fail`/`partial` is fixed and re-verified live, or explicitly deferred with a reason.
- Every defect is confirmed host-side, or recorded `unproven` with the settling check named.
- Cleanup is accurate: what the audit created, what was removed, what remains and why.
- The data-safety contract held; no unauthorized or irreversible live action was taken.
- `docs/live-flow-audit.md` holds the full run and a final summary, and `docs/live-flow-findings.md` (if used) the complete ledger with terminal statuses.

## Completion criteria — onboarding pass

- Every onboarding entry point and first-value flow has a verdict; out-of-scope listed with reason.
- Every chunk executed and reviewed, go sign recorded for each transition.
- Every `fail`/`partial` fixed and re-verified live, or explicitly deferred with reason.
- Every defect confirmed host-side, or recorded `unproven` with settling check named.
- Measurements ledger complete for every persona × flow.
- Cleanup accurate: audit accounts, bookings, data created, removed, remaining.
- Data-safety contract held.
- `docs/onboarding-audit.md` holds the full run, measurements ledger, and final summary.
- `docs/onboarding-findings.md` (optional, if split) holds the defect ledger with terminal statuses.
- `docs/onboarding-report-final.html` generated and committed (or offered as artifact).

## Visual HTML report — onboarding pass

The onboarding pass produces a per-chunk HTML report (`docs/onboarding-report-chunk-<N>.html`) and a cumulative final report (`docs/onboarding-report-final.html`): time-to-value funnel per persona, hesitation heatmap, trust-signal checklist, defect ledger, and measurements table. Onboarding sections, filenames, and data source live in `references/onboarding-report.md`; the generic shell, severity, evidence, and offline rules live in `skill://audit-loop/references/html-report` — read both when generating a report.
