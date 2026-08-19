# .skills — Project Audit Skills

A collection of agent skills for running deep, evidence-backed audits of full-stack web applications (frontend + backend wiring), originally developed while auditing a Django REST Framework + Next.js reservation platform.

## Skills

| Skill | Purpose |
|---|---|
| `audit-loop` | Run a complete project-wide frontend/backend wiring audit in one pass. Exhaustively inspect every user-facing route, SPA view, control, data-bearing element, state transition, API contract, permission boundary, persistence path, cache, privacy rule, failure state, and browser flow, then build a finding ledger before repairing. |
| `tree-mapper` | Build or refresh `docs/ui-tree.md` — the frontend/backend integration tree and per-unit wiring inventory that audits depend on. |
| `section-auditor` | Audit and repair one frontend page or SPA view with its backend integration, proving every control and every datum rather than just that the page renders. |

## Install

Install all three skills into the current project (works with any agent that supports `SKILL.md`):

```bash
npx skills add NavidGhoreyshi/.skills --skill '*' --yes
```

Or install them individually:

```bash
npx skills add NavidGhoreyshi/.skills --skill audit-loop --yes
npx skills add NavidGhoreyshi/.skills --skill tree-mapper --yes
npx skills add NavidGhoreyshi/.skills --skill section-auditor --yes
```

See what's available without installing:

```bash
npx skills add NavidGhoreyshi/.skills --list
```

## Usage

### audit-loop

At the very start, `audit-loop` asks the user to choose a mode:

- **Auto-fix** (default) — audit the whole project, then autonomously fix every confirmed defect, add regression coverage, verify the repairs, and report the complete ledger at the end.
- **Interactive** — audit the whole project exactly the same way, then present the findings in a severity-grouped summary table and walk through each defect one at a time: explain the issue, offer a recommended solution, and let the user decide what to do with it (implement the proposal / describe a different approach / skip / mark already resolved).

Discovery and proof are identical in both modes; only *who decides what gets fixed* changes. Interactive mode never narrows the audit itself.

#### Interactive mode, in practice

```text
> How should I handle the defects this audit finds?
> 1. Auto-fix — audit everything, then fix all confirmed defects automatically (default).
> 2. Interactive — audit everything, then walk me through each defect one at a time
>    so I can decide what to do.
→ 2

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

### tree-mapper / section-auditor

These are the child skills `audit-loop` orchestrates, and both work standalone:

- `tree-mapper` — inventory a project's routes, views, components, API wiring, permissions, and tests before any audit work.
- `section-auditor` — audit a single page/view with its backend integration, classify findings, and (in auto-fix mode) repair them with regression coverage.

## How it works

- Roles such as "tree-mapper" and "section-auditor" are **responsibilities, not required agent names**. If a matching sub-agent is unavailable in the runtime, the orchestrator performs the responsibility directly with the tools at hand.
- The skill documents are runtime-agnostic — any agent that loads `SKILL.md` (Claude Code, Codex, Cursor, and similar) can run them.
- Audit documents default to `docs/ui-tree.md`, `docs/ui-audit-progress.md`, `docs/wiring-audit-findings.md`, and `docs/browser-tools.md`; the paths are configurable per project.

## License

MIT © 2026 Navid Ghoreyshi
