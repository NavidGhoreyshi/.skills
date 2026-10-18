# .skills — Agent Skills for Agentic Workflows

A collection of agent skills for running deep, evidence-backed audits of full-stack web applications (frontend + backend wiring), originally developed while auditing a Django REST Framework + Next.js reservation platform. `audit-loop` is the router parent: it asks the setup questions and routes each selected audit to its own branch skill — each of the seven audits (live flow, onboarding, API wiring, security, SEO, code quality, missed features) is its own skill that owns its branch body. `roadmap-composition` goes one level up: it plans the work — composing the multi-session `ROADMAP.md` an [ompo](https://github.com/NavidGhoreyshi/ompo) orchestrator executes slice by slice. `checkpoint` covers the other axis: keeping a long-running piece of work resumable across a shutdown.

## Skills

| Skill | Purpose |
| `audit-loop` | Route a project-wide audit across nine branch skills: ask the setup questions (audit type, fix mode, live deployment authority), invoke one skill per selected branch in run order, and merge the aggregate report. |
| `audit-live-flow` | Drive the deployed app end to end on the live domain with browser control plus host access, in reviewed chunks — journey pass for every feature, onboarding pass for the new-user path to first value. |
| `audit-deployment` | Prove the serving artifact matches the repo and the project can be deployed, reverted, and restored. |
| `audit-secrets` | Audit every credential across code, stores, logs, and hosts with placement, echo, liveness, and separation probes. |
| `audit-authorization` | Prove who may do what to which resource with paired entitled and unentitled probes. |
| `audit-api-wiring` | Trace frontend/backend contracts, permissions, persistence, state transitions, privacy, and browser proof. |
| `audit-security` | Hunt exploitable authentication, authorization, tenancy, input, secret, and data-exposure defects with a probe per claim. |
| `audit-seo` | Audit crawlability, on-page elements, structured data, authority, and AI answer-engine visibility. |
| `audit-code-quality` | Measure and reduce maintainability debt without changing observable behavior. |
| `audit-missed-features` | Propose missing interactions grounded in existing capabilities; the user decides each one. |
| `tree-mapper` | Build or refresh `docs/ui-tree.md` — the frontend/backend integration tree and per-unit wiring inventory that audits depend on. |
| `section-auditor` | Audit and repair one frontend page or SPA view with its backend integration, proving every control and every datum rather than just that the page renders. |
| `context-pack` | Package the source files relevant to a prompt into a portable context pack (XML + manifest) for another LLM, without solving the request. |
| `deep-research` | Research anything on the internet with platform breadth (agent-reach) and extraction depth (scrapling, patchright-enhanced fallback). |
| `roadmap-composition` | Compose or revise an ompo `ROADMAP.md` — the multi-session plan an ompo orchestrator executes slice by slice. Splits work by file ownership and context budget, carries interfaces into slice bodies, and ships an audit script that flags overlapping, unbounded, or sweep-shaped slices. |
| `www` | Turn a session's mistakes, near misses and miscommunication into durable rules. Two modes — retro on the current conversation, or a corpus audit sweeping past transcripts — then routes each lesson to the strongest mechanism that prevents it recurring: a linter rule, a skill, a global or project `AGENTS.md` line, or nothing at all. Ships a zero-dependency scanner that ranks candidate turns across the omp and opencode transcript stores. |
| `checkpoint` | Save a session to a durable checkpoint and reload it later — the plan, locked decisions, in-flight jobs and the next action. Save freezes the tree, snapshots it, writes `STATE.md` and flushes it to disk; resume ages that file against the tree, corrects it, then continues with a fresh agent briefed on the partial state. Built for a machine going down mid-work: the in-flight job's brief is quoted verbatim, because the brief dies with the session that wrote it. |

## Install

Requires [Node.js](https://nodejs.org) — the `skills` CLI is fetched on demand via `npx`.

Install every skill into the current project (works with any agent that supports `SKILL.md`):

```bash
npx skills add NavidGhoreyshi/.skills --all
```

Or install them individually:

npx skills add NavidGhoreyshi/.skills --skill audit-loop --yes
npx skills add NavidGhoreyshi/.skills --skill audit-live-flow --yes
npx skills add NavidGhoreyshi/.skills --skill audit-deployment --yes
npx skills add NavidGhoreyshi/.skills --skill audit-secrets --yes
npx skills add NavidGhoreyshi/.skills --skill audit-authorization --yes
npx skills add NavidGhoreyshi/.skills --skill audit-api-wiring --yes
npx skills add NavidGhoreyshi/.skills --skill audit-security --yes
npx skills add NavidGhoreyshi/.skills --skill audit-seo --yes
npx skills add NavidGhoreyshi/.skills --skill audit-code-quality --yes
npx skills add NavidGhoreyshi/.skills --skill audit-missed-features --yes
npx skills add NavidGhoreyshi/.skills --skill tree-mapper --yes
npx skills add NavidGhoreyshi/.skills --skill section-auditor --yes
npx skills add NavidGhoreyshi/.skills --skill context-pack --yes
npx skills add NavidGhoreyshi/.skills --skill deep-research --yes
npx skills add NavidGhoreyshi/.skills --skill roadmap-composition --yes
npx skills add NavidGhoreyshi/.skills --skill www --yes
npx skills add NavidGhoreyshi/.skills --skill checkpoint --yes
```

See what's available without installing anything:

```bash
npx skills add NavidGhoreyshi/.skills --list
```

## Usage

### audit-loop

`audit-loop` is the router: it asks three setup questions, then invokes one branch skill per selected audit in run order and merges the aggregate report.

**Question 1 — audit type** (several may be selected; they run in this order, each as a separate labeled phase driven by its branch skill):

- **Live user flow** (`audit-live-flow`, recommended) — drive the *deployed* app through every user-facing feature end to end, on the live domain, with browser control **and** shell access to the host so a browser symptom can be confirmed or refuted server-side. Runs in reviewed chunks — journey pass for the full surface, onboarding pass for the new-user journey to first value (time-to-value, drop-off, cognitive load, trust signals, promise-to-delivery gap).
- **Deployment** (`audit-deployment`) — prove the serving artifact matches the repo: artifact, schema, env, and flag parity per environment, plus rollback and restore-into-scratch evidence naming the next operator command.
- **Secrets** (`audit-secrets`) — audit every credential across code, stores, logs, and hosts: placement, echo surface, liveness and rotation, and separation across environments, with blast radius and the exact operator rotation step per finding.
- **Authorization** (`audit-authorization`) — prove who may do what to which resource with paired entitled and unentitled probes per resource path, refusing without a passing twin never counting as proof.
- **API wiring** (`audit-api-wiring`) — trace every control and datum through frontend → API → auth/role → validation → persistence → response → rendered state, prove reads and writes end to end, and exercise loading/empty/error/unauthorized/privacy/pagination cells.
- **Security** (`audit-security`) — probe every trust boundary: authentication, authorization and tenancy isolation, input handling, secret management, data exposure, abuse resistance, and configuration. Each finding needs a reproducible non-destructive probe; a negative result needs the recorded attempt too.
- **SEO** (`audit-seo`) — audit crawlability, indexation, technical and on-page elements, structured data, authority, and AI answer-engine visibility.
- **Code quality** (`audit-code-quality`) — measure maintainability debt (duplication, dead code, complexity, unsafe type escapes, swallowed errors, N+1 access, test quality) on a recorded baseline, then reduce it without changing observable behavior.
- **Missed features** (`audit-missed-features`) — walk pages and components one by one, propose only interactions the product's existing data, routes, and permissions already support, and let you classify each as needed / intentionally left out / defer / not applicable.

**Question 2 — fix mode**:

- **Manual fix mode** (recommended) — audit the whole project, then present the findings and ask before modifying application code.
- **Automatic fix mode** — audit the whole project, then autonomously fix every confirmed in-scope defect, add regression coverage, verify the repairs, and report the complete ledger at the end.
- **Report-only mode** — record findings and evidence and change nothing, installing nothing; the ledger, proof standards, and completion criteria still apply, only repairs stop.

Discovery and proof are identical in all three fix modes; only *who decides what gets fixed* changes. Neither mode permits silently implementing a missed-feature proposal that was not classified as needed.

**Automatic fix mode is still chunked in a live audit.** The run always stops at a chunk boundary for your go sign, because a whole-product live sweep will not fit in one coherent context window. Automatic means "decide and fix without asking per finding" — not "run unattended until the end".

**Question 3 — live deployment authority** (live flow audit, both passes) asks whether the run may push and deploy to verify fixes, defaulting to *no — report only*. It is asked on every run and every chunk boundary, never cached: an unattended model deploying to production is a decision only the user can make, and the right answer changes as an environment gains real users.

#### Router driving the live-flow branch, in practice

```text
> What kind of audit should this run perform?
→ 1. Live user flow audit

Live URL + ssh host + identities confirmed. 43 flows inventoried, split into 6 chunks.
Full plan written to docs/live-flow-audit.md. Starting chunk 1.

── Chunk 1 — anonymous discovery (go sign: pending) ─────────────────

| Flow | Verdict | Note |
|------|---------|------|
| LF-F01 home / hero | pass | |
| LF-F02 search + filters | pass | |
| LF-F03 public business profile | fail | phone tap does nothing |
| ...  | | |

LF-003 · Critical · public business profile · phone tap does nothing
  repro:   open /b/demo-b-1, tap the phone number
  observed: no navigation, no request in the network log
  expected: tel: intent fires
  host:     no backend hit — so this is a frontend-only defect, not an API one
  fix:      anchor renders as <a href="tel:..."> but is wrapped in a div with
            onClick that swallows the default
  status:   fixed, awaiting live verification

Audit data left on live: 1 test appointment (chunk 1, id #4821). Cleanup listed in state file.
Next up: chunk 2 — authentication and account recovery (LF-F09..LF-F16)

Go sign for chunk 2?
```

Everything needed to resume lives in `docs/live-flow-audit.md`, so the next chunk can run in a **fresh session** with no conversational memory — the state file names the next chunk and its first flow.

#### Router driving the wiring branch in manual fix mode, in practice

```text
> What kind of audit should this run perform?
> 1. API wiring audit (Recommended)
> 2. Code quality audit
> 3. Security audit
> 4. Missed-features assessment
→ 1

> How should confirmed fixes be handled?
> 1. Manual fix mode (Recommended) — report findings and proposed changes first.
> 2. Automatic fix mode — repair confirmed in-scope defects after discovery.
→ 1

Full audit complete: 4 confirmed defects, 2 missing-coverage items. Code untouched.

| ID   | Severity    | Location                          | Issue                                        | Status          |
|------|-------------|-----------------------------------|----------------------------------------------|-----------------|
| F-01 | 🔴 Critical | backend/apps/business/views.py    | Public subresources skip the verified gate   | ⏳ Pending decision |
| F-02 | 🟠 High     | frontend/app/user/settings/page.tsx | Notification prefs are localStorage-only    | ⏳ Pending decision |
| ...  |             |                                   |                                              |                 |

── Finding F-01 (1/4) ───────────────────────────────────────────────

| Field          | Value                                                      |
|----------------|------------------------------------------------------------|
| ID             | F-01                                                       |
| Severity       | 🔴 Critical                                                 |
| Location       | backend/apps/business/views.py                            |
| Description    | Public detail subresources ignore the VERIFIED gate.      |
| Impact         | Anonymous callers can read unverified businesses.         |
| Evidence       | confirmed bug — public-gate probe, tests_public_gate.py   |
| Recommendation | Route reads through a shared verification-aware helper.   |

Proposed fix: extract a public-access helper in apps/business/public_access.py,
apply it to the subresource reads, add pending/rejected/verified regressions.

How would you like to solve this?
1. Your proposed solution — implement as described.
2. Different approach — describe it and I'll implement that.
3. Skip this issue.
4. Already resolved.
→ 1
✅ Fixed and verified: 4 new tests pass, affected matrix cells re-run.

── Finding F-02 (2/4) ───────────────────────────────────────────────
…
```

Each finding gets the same treatment — introduced, a fix proposed, a decision, and (if approved) a verified fix — until every row in the summary table has a terminal status. The final report includes the full ledger: what was fixed, skipped, deferred, and left unproven.

### the audit branches

One line per branch skill the router dispatches to, in run order:

- `audit-live-flow` — drive the deployed app end to end on the live domain with browser control plus host access, in reviewed chunks — journey pass for every feature, onboarding pass for the new-user path to first value.
- `audit-deployment` — prove the serving artifact matches the repo and recovery works, naming the next operator command.
- `audit-secrets` — prove every credential is known, minimally placed, unexposed, and separated across environments.
- `audit-authorization` — prove who may do what to which resource with paired entitled and unentitled probes.
- `audit-api-wiring` — trace every control and datum through contract, auth, validation, persistence, and rendered state, with browser proof.
- `audit-security` — probe every trust boundary with a reproducible non-destructive probe per claim.
- `audit-seo` — audit crawlability, on-page elements, structured data, authority, and AI answer-engine visibility.
- `audit-code-quality` — measure maintainability debt on a baseline, then reduce it without changing behavior.
- `audit-missed-features` — propose only interactions the existing data, routes, and permissions already support, including competitor feature gaps; the user classifies each.

### tree-mapper / section-auditor

These are the child skills `audit-loop` orchestrates, and both work standalone:

- `tree-mapper` — inventory a project's routes, views, components, API wiring, permissions, and tests before any audit work.
- `section-auditor` — audit a single page/view with its backend integration, classify findings, and (in automatic fix mode) repair them with regression coverage.

### context-pack

Prepares context for another LLM — nothing else. Given a prompt, the skill scopes the change (**contained** = only the files being modified, or **broad** = primary files plus everything they depend on), copies the selected source files verbatim into `context_*.txt` files, and writes a `context_manifest.txt` summary — all in the project root.

- Context files are XML with the prompt, project root, part number, and each source file wrapped in CDATA.
- Media/binary files are referenced by path only (manifest + XML) — their contents are never exported.
- Files split across `context_01.txt`, `context_02.txt`, … when output approaches the model limit; a source file is never split across parts.
- The skill reports only statistics at the end; it never answers the original request.

### deep-research

Research with breadth then depth: `agent-reach` across web search, social, video, GitHub, RSS; `scrapling` to extract blocked or JS-heavy pages (`get` → `fetch` → `stealthy-fetch`); `patchright-enhanced` only when stealth browsing or login interaction is unavoidable. Primary sources only, every claim cited.

### roadmap-composition

Write the ROADMAP.md that `ompo run` executes — and restructure one that keeps wedging.

- Builds a file → slice ownership map *before* writing bodies, so no file is touched by two slices without an ordering edge.
- Sizes each slice to the worker's context budget (12k-char spec, 120k-token context) and turns sweeps into codemods with a committed manifest.
- Carries the interfaces dependencies established into each slice body, instead of leaving workers to re-derive them from source.
- Validates with `ompo lint`, a bundled composition audit (`scripts/audit-roadmap.mjs`: overlap, unbounded scope, sweep smell), and `ompo plan`.
- Ships two calibration fixtures: a clean roadmap and one reproducing a real wedge, so the rules stay checkable.

### www

Turn what went wrong into something that cannot happen again — an agent rules file that only accumulates advice is the failure mode this replaces.

- **Two modes.** *Session retro* reads the current conversation. *Audit mode* sweeps a corpus of past transcripts — the shape that produced most of one user's global rules, 47 items judged one at a time.
- **Finds incidents from evidence, not recall.** A bundled zero-dependency scanner (`scripts/incidents.py`) ranks candidate turns as `retro` / `correction` / `repair` / `error`, reading both the omp JSONL store and the opencode sqlite store — including the `session_v2`/`session_message` tables, since the legacy ones are empty and will convince you the history is gone.
- **Routes every lesson to the weakest mechanism that still prevents it recurring:** a linter rule with a bad/good fixture pair, a branched skill, one line in a global or project `AGENTS.md`, or *nothing at all* — some lessons are real, unwriteable, and better said than filed.
- **Treats "too narrow" as a trigger-wording problem.** Rewording a viewport-lock rule to name the shape of the situation rather than the instance that produced it is how a rejected rule becomes a general one.
- **Records rejections too**, so the same non-lesson stops being re-proposed next time.

Depends on `python3` and nothing else. Reads the default omp and opencode stores under `~`; both paths are overridable.

### checkpoint

Keep a session's state alive across a shutdown, and pick it up in a fresh session.

- **One directory per session** under `~/.agents/state/` — `STATE.md` beside `git log`, `status` and `diff` snapshots — never the OS temp dir, which a reboot clears, and never the repo, where it becomes `git status` noise.
- **Refresh on every settled decision, and always *before* dispatching a long job.** Shutdowns are not announced, so a checkpoint written at the end is missing exactly when it is needed; `Updated:` heads the file and it is flushed to disk, so a stale one cannot pass for the current one.
- **Quotes the in-flight job's brief verbatim** — the brief dies with the session that wrote it, which makes it the one thing that cannot be reconstructed afterwards.
- **Resume ages the file against the tree.** An in-flight job is unknown until its own record and its files are read; the file is corrected first, then a fresh agent is briefed on the partial state rather than on the original brief.
- No scripts, no dependencies — markdown files and the standard tools.


## How it works

- Roles such as "tree-mapper" and "section-auditor" are **responsibilities, not required agent names**. If a matching sub-agent is unavailable in the runtime, the orchestrator performs the responsibility directly with the tools at hand.
- The skill documents are runtime-agnostic — any agent that loads `SKILL.md` (Claude Code, Codex, Cursor, and similar) can run them.
- Audit documents default to `docs/ui-tree.md`, `docs/ui-audit-progress.md`, `docs/wiring-audit-findings.md`, `docs/live-flow-audit.md`, and `docs/browser-tools.md`; the paths are configurable per project.

## License

MIT © 2026 Navid Ghoreyshi
