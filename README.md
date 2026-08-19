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
