---
name: roadmap-composition
description: Compose or revise an ompo ROADMAP.md — the multi-session plan `ompo run` executes slice by slice. Use whenever the user wants to write a roadmap, compose/plan/replan a project, split work into slices or phases, restructure a roadmap that keeps wedging, mentions ompo, ROADMAP.md, slice boundaries, or worker context budgets, or asks for a multi-session plan an agent orchestrator will execute — even if they only say "plan this project" or "break this into tasks for ompo". Also use before handing any plan to `ompo run`.
---

# Roadmap composition

A roadmap is the entire world of each worker session: `ompo` spawns one fresh
agent per slice, in its own git worktree, with a prompt compiled from the slice
body + one-line dep summaries — nothing else. Boundaries decide cost: good ones
make cheap workers, bad ones make workers that re-read the same files forever.

## When to use / not to use

Use for: writing or replanning a ROADMAP.md for `ompo`; restructuring a run
that wedged (cap aborts with zero edits, repeated re-reads, cross-slice merge
conflicts); splitting a project into slices/phases for agent execution.

Not for: single-session work (that is a task — just do it); `ompo init`'s
project survey (init discovers, this skill composes).

## The worker's world

| Input | Budget |
|---|---|
| Slice body + `Files` + completion contract | `specBudget`, 12k chars default |
| One-line dep summaries | a few lines |
| Fresh context window | `contextCapTokens`, 120k default |
| Isolated worktree + cap-abort handoff brief | loop-provided |

- Anything the worker must know has to be in the body: a dep summary names an
  outcome, never an interface. Missing detail is re-derived from source at full cost.
- Fresh context per slice means every read is paid again — overlap is a re-read
  tax and a merge-conflict tax.
- A cap abort kills the worker without warning; only committed files and its
  NOTES.md survive.
- Sweeps cannot fit a context window: "walk every page" is a budget-shaped
  instruction, not a slice.

Cost of ignoring this (run `20260916-va5e9b`): 77% of 2,221 worker reads were
re-reads, 30/30 cap handoffs carried no state, and two sweep slices died with
749 and zero edits.

## Workflow

**(a) Survey** the tree, docs, stack, and test commands.

**(b) Map files → slices before writing bodies.** Groups sharing a file are one
slice or an ordered pair (R1/R9). Write the roadmap from this map.

**(c) Order and merge.** `Depends:` only where a slice consumes another slice's
interface, not merely its topic.

**(d) Write bodies that carry interfaces** (R4).

**(e) Assign gates.** Real exit-0 commands; cross-cutting invariants in shared
gates (R5). Trailer semantics: `references/ompo-format.md`.

**(f) Validate** with the loop below until clean.

**(g) Hand off** the slice table (id, title, Files, deps, gate count) plus the
command outputs; confirm boundaries before an `ompo run` spends model budget.

## Composition rules

Why + measured evidence per rule: `references/composition-rules.md`.

- **R1 — One writer per file.** A shared file means a merged slice, or a
  `Depends:` chain whose later body states what it inherits.
- **R2 — Slice by context boundary, not by UI surface or theme.** Read surface
  ≲10 files / ≲2k lines; past that, split by file cluster or script it.
- **R3 — Sweeps are scripts with an explicit manifest.** Codemod + committed
  checklist + a gate that proves coverage.
- **R4 — Bodies carry interfaces.** Exact components, props, classes, tokens,
  and testids a slice consumes or produces.
- **R5 — Global invariants live once, in gates** (`Verify:`/`verifyDefaults`),
  never in repeated body prose.
- **R6 — No audit-only or no-op slices.** Evidence work folds into the
  consuming slice or becomes a gate.
- **R7 — Preflight the tree.** Already-shipped work is not a slice; `Skip:
  true` parks the rest.
- **R8 — Trailer discipline.** `Effort:` always; gates repo-real (no `|| true`,
  no duplicates, `sh -c '...'` when a chain shares shell state); `Timeout:` only
  when >15m; `Retries: 1`; `Files:` accurate.
- **R9 — Dependency shape vs parallelism.** Slices with no dependency path
  between them must have disjoint `Files` sets; overlap needs an ordering edge.
- **R10 — Body is the whole spec.** Stay within `specBudget`; acceptance
  criteria are observable checks, not prose.

## Required validation loop

```bash
ompo lint --roadmap ROADMAP.md
node <skill-dir>/scripts/audit-roadmap.mjs ROADMAP.md
ompo plan --project .
```

- `ompo lint` — errors block execution (gate hygiene); fix them, treat warnings
  as decisions.
- audit — composition shape (overlap, unbounded scope, sweep smell); `--strict`
  exits 1 on findings for CI.
- `ompo plan` — final preview; exits 1 when blocked.

Fix and re-run until lint reports 0 errors, the audit no findings, and the plan
is ready. Then present the roadmap.

## References

- `references/ompo-format.md` — trailers, `Verify` splitting, lint codes, budgets.
- `references/composition-rules.md` — R1–R10 with why and evidence.
- `references/evidence.md` — the run that motivated this skill.
- `scripts/audit-roadmap.mjs` — the composition linter.
- `fixtures/good-roadmap.md`, `fixtures/bad-roadmap.md` — clean composition vs
  the wedge shape.
