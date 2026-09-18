# ompo ROADMAP.md format

Cross-checked against `src/parse.ts`, `src/lint.ts`, `src/config.ts`,
`src/worker.ts`, `src/loop.ts`. If a future ompo version disagrees, the code
wins — and `ompo lint` tells you.

## Shape

```markdown
# Anything (H1 and prose before the first ## are ignored)

## [slice-id] Human title
Body (markdown; may contain ###+ and fenced code).
Depends: other-id, another-id
Agent: task
Effort: med
Verify: bun test
Files: src/a.ts, src/b.ts
Retries: 1
Timeout: 30m
Skip: true
```

- `## ` opens a slice; `###`+ never does. `[id]` pins the id (else slug of the
  title). Ids are stable across runs — rename titles, never ids.
- Trailers are `Key: value`, case-insensitive, stripped from the body, and may
  appear anywhere in the section **except inside fenced code** (kept verbatim).
- Parser rejects (all `ompo lint` errors): zero slices, duplicate ids, unknown
  `Depends`, dependency cycles, invalid `Effort`/`Retries`/`Timeout`.

## Trailers

| Trailer | Values | Semantics |
|---|---|---|
| `Depends:` | slice ids, comma/space separated | Must exist; no cycles. Dep summaries are inlined into the worker spec, one line each. A skipped dep counts as satisfied. |
| `Agent:` | `task`, `sonic`, a model pattern, or an `agentModels:` key | Anything else warns (`unknown-agent`) and falls back to `workerModel`. |
| `Effort:` | `lo`/`low`, `med`/`medium`, `hi`/`high` | Planning hint; `hi` also escalates the worker to the deep model slot. Missing warns (`no-effort`). |
| `Verify:` | repeatable | Gate commands; see below. |
| `Files:` | repo-relative paths, comma/space separated | Worker allowlist and audit input. Absolute or `..` warns (`files-escape`). |
| `Retries:` | 0..10 | Retries after the first attempt; default **1**; >3 warns. |
| `Skip:` | `true`/`yes`/`1`/`skip` | Parks the slice (status `skipped`); still a valid dep target. |
| `Timeout:` | `Ns`/`Nm`/`Nh` (bare = seconds), 1m..8h | Per-slice worker budget; default 15m; >60m warns. |

## Verify semantics

- Gates run in the slice worktree (cwd = worktree root); `verifyDefaults` from
  `.omp/roadmap.yml` are prepended.
- Each `Verify:` line's top-level `&&` chain splits into separate gates, each
  in its own shell. Quote-aware: `sh -c 'cd e2e && npx playwright test'` stays
  one gate — use it when a chain shares shell state.
- `||` never splits (warns `or-gate`: fallbacks mask failures).
- A gate that only mutates shell state (`cd`, `export`, …) is an **error**
  (`state-split`): it cannot affect the next gate.
- No `Verify:` and no `verifyDefaults` is an **error** (`no-verify`).

## Lint codes

Errors fail the command (exit 1) and block `ompo plan`; warnings pass.

| Level | Codes |
|---|---|
| error | `parse`, `no-verify`, `state-split` |
| warn | `or-gate`, `dup-gate`, `big-timeout` (>60m), `big-retries` (>3), `no-effort`, `thin-body` (<20 chars), `files-escape`, `unknown-agent`, `skip-with-dependents`, `dep-on-skipped` |

`ompo plan --project .` renders parsed rows (id, title, Effort, gate count,
deps, findings) and exits 1 when any lint error makes the preview `blocked`.

## Budgets and defaults (worker-visible)

| Knob | Default | Set by |
|---|---|---|
| Spec budget | 12,000 chars | `.omp/roadmap.yml` `specBudget` |
| Context cap | 120,000 tokens | `contextCapTokens`, `--context-cap N`, `--no-handoff` (0 disables) |
| Worker timeout | 15m | `Timeout:`, `workerTimeoutSec`, `--timeout-sec` |
| Retries | 1 | `Retries:`, `maxRetries`, `--max-retries` |
| Debugger / unblock budgets | 30m / 2 sessions | `debugTimeoutSec`, `maxUnblocks` |

On a context-cap abort the loop preserves the branch, writes a handoff brief
(preserved commits/diff, NOTES.md tail, worker log tail, absolute artifact
paths), and respawns the same attempt — no retry consumed. Repeated cap aborts
with no file progress fail the slice as `context_thrash`: the answer is to
split the slice, not raise the cap. Workers are also asked to maintain a
per-slice `NOTES.md`, whose tail is handed to the next generation.

The worker spec (compiled by `src/spec.ts`) carries, in budget order: header,
body, `Files`, repo conventions (`AGENTS.md`), completion contract, review
notes, dep summaries. Under pressure it truncates dep summaries first, then the
body; a body alone over budget is an error — split the slice.
