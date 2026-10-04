---
name: www
description: What Went Wrong. Turning a session's mistakes, near misses and miscommunication into durable rules. Use when the user asks why the agent made a mistake or a near miss, why a bug happened and got fixed in flight, why their intent was not conveyed, what to prevent next time, or asks to add a lesson to AGENTS.md.
---

Mine what went wrong, then file each lesson where it can actually be enforced.

**Session retro** (default) reads the current conversation. **Audit mode** sweeps
a corpus — read `references/audit-mode.md` when the ask spans projects or dates.
Most of the current global rules came from an audit, not a retro.

## 1. Find the incidents

Evidence lives in the transcripts, not in your recall. Run `scripts/incidents.py`
(`references/usage.md`) to rank candidate turns, then confirm each against the
tool output it refers to. It ranks leads; it does not decide what was an
incident. Both stores matter — omp JSONL, and opencode sqlite in
`session_v2`/`session_message`, where the legacy `message`/`part` tables are empty
and will convince you the history is gone.

Three kinds worth mining:

- **Agent mistake** — wrong file, tool, or assumption; a defect found and patched in flight. Read what the session reported as *fixed*, not what it shipped.
- **Miscommunication** — the ask was ambiguous, underspecified, or contradicted an earlier instruction. Not the user's error by default: ask whether one grounding question would have pinned it down (`clarify-change`), and file against whichever side held the information.
- **Process skip** — a check that exists was not run. Most valuable kind: the cheapest to make automatic.

Tool and harness failures count too (degraded lookup, silent fallback). Those
become "state the degradation" rules, never "avoid the tool" rules.

Nothing found means nothing found. Do not manufacture lessons from ordinary work.

## 2. Write the rule

Imperative, at most two sentences, naming the failure shape and the specific lie
it produces.

- **Recognition test:** could a reader spot a new instance from the rule alone, never having read the story? If not, rewrite.
- A concrete counter-example is what makes a rule stick: *"A 375px run that rendered at 780px reports a clean pass."* Generic advice does not survive a deadline.
- **Too narrow is a trigger problem, not a rejection.** Reword the trigger to name the situation's *shape*, not the instance: "when the user asks about a viewport-specific layout change, ask how every viewport behaves" generalises; "when someone locks a viewport" does not.
- **Dedupe first.** Grep `~/.agents/AGENTS.md`, the project `AGENTS.md`, `~/.agents/skills/`. Restating an existing line is a duplicate, not a lesson — cite the existing line.
- No anecdote, dates, or session ids in rule text. They belong in the evidence column.

## 3. Route it

Weakest mechanism that still prevents recurrence wins. Criteria in
`references/routing.md`.

| Failure shape | Home |
|---|---|
| Deterministic and file-shaped | linter rule + bad/good fixture pair |
| Branched procedure, low frequency, strong keywords | new skill |
| Applies every turn, cheap to hold | one line in `~/.agents/AGENTS.md` |
| Only true inside one repo | that repo's `AGENTS.md` |
| Judgment, no mechanism to enforce | don't write it — say it out loud |

- **Default to project scope.** Promote to global only when the failure shape is both stack- and repo-agnostic. A wrongly-global rule taxes every session forever; a wrongly-project rule taxes one repo.
- Never add a linter rule without a fixture pair and a run showing bad fails, good passes.
- Lintable but no linter exists yet? Write the rule as text and name the lint rule as explicit follow-up.

## 4. Apply, verify, report

Propose the whole set first; one approval for the batch, not one per rule.

- Edit with `edit`, then re-read the region. An anchored edit lands on the wrong line once the file has moved, and the syntax error is the cheap detector.
- Run `~/.agents/lint/check.sh` on everything touched.
- A new skill is not live until a fresh session discovers it — registration is reindexed on restart, not on write.

Report one row per lesson: incident (with evidence) → rule text → home → how it
was verified. Then the rejections and why: already covered, not enforceable, too
narrow, or the user's habit rather than an agent rule. Rejections are how the
same non-lesson stops being re-proposed.

Done when every candidate is filed with evidence or explicitly rejected, and the
verification actually ran.