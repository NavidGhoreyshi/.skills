# Routing a lesson

One lesson, one home. The question is not "where is this most relevant" but
"what is the weakest mechanism that still makes this failure impossible to
repeat". `SKILL.md` §3 has the table; this file is the reasoning behind the rows.

## Linter rule

The failure has a textual signature a parser can see: a banned call, a hardcoded
literal, a decorative comment, a lockfile that moved. If you can write the check
without making a judgement call, it belongs here.

Two homes, matched to lifetime:

- **Repo-local** (`<repo>/tools/lint/check.py`, or `.semgrep/`): that codebase's conventions. Discovered via the repo `AGENTS.md` pointer; enforced by `pre-commit`/CI.
- **Global** (`~/.agents/lint/`): rules about how the agent works everywhere. Repo agents cannot discover these, so the global `AGENTS.md` carries the pointer.

Recipe, zero dependencies:

1. One check function returning `file:line: [rule-id] message`.
2. A **fail fixture** and a **pass fixture**. Not optional — a rule with no failing fixture has never been shown to fail.
3. Run both. Fail fixture reports ≥1 finding and exits non-zero; pass fixture reports zero and exits zero.
4. Existing violations → baseline file of known offenders, report `hits beyond baseline`. A rule firing on 400 existing lines gets deleted, not baselined into meaninglessness.
5. Run `~/.agents/lint/check.sh` on everything touched.

Mechanical rules with no file to attach to — "claimed done without running it",
"declined without answering" — are **not** linter rules. They need a response
hook, and the honest answer is that one does not exist yet.

## Skill

Use when correct behaviour is a *procedure that branches* rather than a single
line, or when the failure only occurs in a context the description can name.

The description is the whole mechanism — it is the only part of a skill always in
context. Front-load the leading trigger word, one trigger per branch, collapse
synonyms: `Use when the user says X, mentions Y, or asks about Z.`

It must earn its per-turn context cost. If the lesson fits one `AGENTS.md` line,
it is not a skill. If a skill already covers the branch, extend that one rather
than adding a near-duplicate name.

## Global vs project AGENTS.md

Global scope is expensive and permanent. A rule earns it only when the failure
shape survives translation to a codebase you have never seen. "Pair a negative
test with a positive control" does. "Never import `can()` from `app/api/**`" is
that one repo's problem.

Project is the default home: stack conventions, layout, database names, runbooks,
deploy gates, that repo's flaky-test pair. Cheap to add, cheap to retire, and it
does not pollute unrelated sessions.

## Do not write it

Some lessons are real and unwriteable: "steelman the user's theory", "ask one
grounding question before coding". No mechanism enforces them, a lint rule would
be theatre, and a skill adds context for a judgement call. State the principle in
the conversation and let it stay there.

Writing it into `AGENTS.md` anyway is not free — every line is read on every turn
of every session forever, and rules that cannot be followed erode the ones that
can.

## Promotion

When a rule has caught the same failure twice, stop asking and start enforcing:
build the linter rule or hook, then keep the text line as the discovery pointer.
Note the promotion in the report so the debt stays visible.