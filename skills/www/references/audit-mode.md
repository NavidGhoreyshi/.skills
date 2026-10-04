# Audit mode — sweeping many sessions

Session retro (the default) mines one conversation. Audit mode sweeps a corpus,
because the same failure usually repeats across sessions before anyone writes it
down. The 2026-10-02 run that produced most of the current `~/.agents/AGENTS.md`
worked this way: 47 items across two weeks of transcripts, judged one at a time.

Audit mode is slower and produces more rejected items. That is the point — the
rejections are what stop a bad rule from becoming permanent.

## Scope the window before scanning

Ask for a window and pick the store set explicitly. Both stores hold history and
neither is complete on its own:

| Store | Path | Shape |
|---|---|---|
| omp | `~/.omp/agent/sessions/**/*.jsonl` | JSON Lines, one object per line |
| opencode | `~/.local/share/opencode/opencode.db` | sqlite: `session_v2` + `session_message` |

Schema detail, including the opencode trap, is in `usage.md`.

`scripts/incidents.py --days 14` reads both stores over a trailing window.

## Write findings somewhere that survives

The first audit wrote 39 KB of findings to `/tmp/miscommunications-audit-2026-10-02.md`
and it was gone within a day. An audit spans hours or sessions; the working
document has to outlive the process that wrote it.

Put it next to the rules it feeds, or in whatever the user already keeps —
`~/.agents/` is the safe default for anything that will end up in
`~/.agents/AGENTS.md`. Verify the path is not on a cleanup timer before writing,
and say which path you used in the report.

## Item format

One incident per item, judged individually. This format is the proven one:

```
**M-01/47 — <project> <short topic>, <date>**
Problem: <what went wrong, in one line, with the concrete evidence>
Decision: worthy | not worthy. <whose fault, and why>
Prevention, pick one:
1. <narrow fix> — <mechanism>
2. <standing rule> — <mechanism>
3. <user-side habit> — <mechanism>
My call: <n> + <n>. <one line: why this combination>. Worth adopting?
Or next → M-02 (<one-line teaser of the next item>)
```

The three options matter. They separate *a fix for this instance* from *a rule
that generalises* from *a habit the user has to keep* — and the third category
is regularly the honest answer. "The agent asked nothing and you assumed the
port" is not fixable by a rule; it is a habit, and saying so prevents a useless
rule.

The running total and the teaser let the user steer without re-reading the file.

## Walk it with the user, one item at a time

The steering vocabulary that worked, worth reusing because it keeps decisions
cheap:

- `add it, then next.` / `adopt globally then next.` / `adopt globally. next.`
- `add it project scoped, then next.`
- `this rule is too niche to be global. how about instead we word it in a way that …`

That last one is the most valuable response available and the easiest to miss.
**A rule that is too narrow is usually a rule whose trigger is worded too
narrowly.** Reword the trigger to name the shape of the situation rather than the
one instance — "when the user asks about a viewport-specific layout change, ask
how every viewport should behave" survives the next repo; "when someone locks a
viewport" does not.

After roughly a dozen items, offer to batch the remainder: `list all remaining
findings and I'll decide at once.` Interactive item-by-item does not scale past
that, and the tail items are usually the weakest.

## Deferral is a first-class outcome

Most findings do not become rules. In the 2026-10-02 audit, roughly 15 of 47
items were adopted; the rest were deferred as too niche, too narrow, or not
actually the agent's fault. Record the deferral and the reason, and move on.

A deferred item is not a failed item. It is the reason the same item does not get
re-proposed in the next audit.

## Parallel scouts, with a negative control

A corpus is too large to read serially. Fan it out: one scout per project
directory or per date slice, each returning a fixed shape so you can merge
mechanically.

```json
{"findings": [{"ref": "M-12", "project": "...", "date": "...", "problem": "...",
               "fault": "agent|user|both|tool", "rule": "...", "quote": "..."}]}
```

An empty `{"findings": []}` is the useful case — it is how you know a slice was
actually read. Two rules make the output trustworthy:

- **A slice that returns nothing still has to prove it read something.** Give it
  a session count to report back. An empty findings list with no count is
  indistinguishable from a scout that gave up.
- **Spot-check by hand before believing a null.** In the first audit, six scouts
  covering 171 files returned empty; 29 regex hits were then opened by hand and
  confirmed clean. The scouts were right, but that was checked, not assumed.

This is the positive-control rule from `~/.agents/AGENTS.md` applied to the audit
itself, which is the right place for it.

## Close the loop

The audit is not done when the findings are collected. It is done when the
adopted rules are in a file and the lint passes:

1. Present the full adopted set in one batch and get one approval.
2. Apply, routing each rule by enforceability (`routing.md`).
3. Re-read every edited region, then run `~/.agents/lint/check.sh` on what changed.
4. Report per rule: evidence → wording → home → how it was verified, plus the
   deferred list with reasons.

If a new skill was created, confirm it is discoverable in a fresh session before
claiming it is live — skill registration is reindexed on restart, not on write.