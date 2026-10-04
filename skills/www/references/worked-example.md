# Worked examples

Two real runs, for calibrating output shape — not templates to copy.

# Example A — session retro, 2026-10-03, rezervman chunk 13

**Trigger.** Mid-session: *"if you wanted to prevent your near mistakes or
mistakes that happened and then you found and fixed in the process of this
session, what would you add to the global agents.md?"*

Seven lessons, all landing in `~/.agents/AGENTS.md` under a new `## Tests and
probes` section the file did not previously have. The absence of a home was why
none had been written down before. Three are quoted because they show the target
wording; the other four are in that file today.

> **Pair every negative with a positive control.** A test expecting a refusal
> proves nothing until the identical request shape succeeds for something
> entitled. A wrong URL, a missing header, or an ambient value quietly satisfying
> the request all read as "the refusal worked".

Three consecutive wrong readings produced that one: a 404 from
`/api/v1/accounts/token/refresh/` instead of `/api/v1/token/refresh/`, a 403 from
a missing CSRF header, and twice a 200 that was really the view reading a
`refresh_token` cookie instead of the body under test. The rule has to survive
the middle case, where the reading was *true for the wrong reason*.

> **Verify the instrument before trusting the reading.** Assert viewport, locale,
> timezone, config — not just the outcome they produce. A "375px" run that
> rendered at 780px reports a clean pass.

Already in that repo's `CLAUDE.md`, where a general agent never sees it — which is
what made global scope correct here rather than duplicative.

> **After a multi-line patch, re-read the region and confirm it parses.** An
> anchored edit lands on the wrong line once the file has moved; the syntax error
> is the cheap detector, not the incident.

Four occurrences in one session — a clobbered `withBrowser` wrapper, two
duplicated kwargs, one anchor past EOF — every one caught by a syntax error
rather than by review. That is the entire argument for the rule.

## What the escalation taught

All seven were judgment-shaped, so all landed as `AGENTS.md` lines. None was
lintable, and none should have been forced into a linter rule — a check for "did
you re-read the region" is theatre.

The eighth finding was the instructive one: the agent had fallen back *correctly*
but *silently*, when `find` degraded on an OpenRouter 402. The missing rule was
not "fall back", it was **"say you fell back"**. An unannounced fallback is
indistinguishable from a negative finding, and that gap is the whole risk.

## Two things worth copying

**The evidence column carries the weight, not the prose.** One line per rule; the
reason it is not generic is the specific story underneath. Story in the report,
out of the rule.

**Flag the unversioned file.** `~/.agents/AGENTS.md` is not under version control.
Seven new rules landed with no history and no review trail — reported rather than
buried, because a guardrail a machine wipe erases is not a guardrail.

**Routing check.** "Re-read the region after a patch" overlaps the *Verify*
section of that same file; it was filed under *Tests and probes* only because the
failure was in test code. Two of seven were arguably misfiled. The dedupe grep
exists to catch exactly that next run.

# Example B — corpus audit, 2026-10-02/03, 47 items

**Trigger.** *"go over every omp and opencode transcript I've had with agents in
the past two weeks… take note of every single time I failed to convey my exact
intent… you and I will go over them one by one and you can offer me ways we could
prevent these miscommunications from happening again."*

47 items judged individually over ~13 hours. ~15 became global `AGENTS.md` rules,
one became a project rule in `rezervman/development/CLAUDE.md`, the rest were
deferred. The adopted set was later split into `~/.agents/lint/` rules and
branched skills — the escalation path `routing.md` describes.

## What the shape taught

**Findings documents must survive.** 39 KB went to
`/tmp/miscommunications-audit-2026-10-02.md` and were gone within a day. An audit
spans sessions; its working document cannot live on a cleanup timer.

**The user's rejections were the most instructive output.** Three verbatim
responses:

- `adopt globally then next.` — the common case, cheap to handle.
- `add it project scoped, then next.` — the routing decision, made per item.
- `this rule is too niche to be global. how about instead we word it in a way that when I demand changes like viewport-lock the model should ask me how I want them on other viewports as well.`

That last one rewrote a viewport-lock rule into a general "UI/layout directives
that could differ by viewport: ask how each target should behave" rule. The
instance was discarded; the shape kept. That is why "too narrow" is step 2 of
`SKILL.md` rather than a rejection.

**Deferral was normal.** M-18, M-20, M-36/37, M-44, M-45, M-19 all deferred.
Roughly two thirds of a 47-item audit not becoming rules is the expected outcome.

**The empty result was checked, not trusted.** Six parallel scouts over 171 files
from the preceding fortnight each returned `{"findings": []}`. Rather than
conclude the fortnight was clean, 29 regex hits were opened by hand and confirmed.
The scouts were right — but that was verified.

## Cost

A 14-day window across both stores takes ~40 seconds and returns a few hundred
ranked leads. The reading, not the scanning, is the expensive part — which is why
audit mode batches the tail decisions instead of walking all 47 interactively.