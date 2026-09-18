# Composition rules — why and evidence

Companion to SKILL.md; full run numbers in `evidence.md`.

**R1 — One writer per file.** A file listed by >1 slice must be merged into one
slice or chained with `Depends:`, and the later body must state the exact state
it inherits. Fresh contexts re-read everything, so overlap doubles reads and
merge conflicts. *Evidence:* 27 of 68 edited files were touched by >1 slice
(`Modal.jsx` and `MembersPage.jsx` ×4 each); 77% of 2,221 reads were re-reads.

**R2 — Slice by context boundary, not by UI surface or theme.** A slice's read
surface should stay ≲10 files / ≲2,000 lines; past that, split by file cluster
or script it. A finite context (120k default) shared between reading, editing,
and verifying means a huge read surface dies at the cap with nothing written.
*Evidence:* `s10-language-rtl-digits`: 13 generations, 749 reads, zero edits,
killed; `s11a-responsive`: killed after 3 generations, zero edits.

**R3 — Sweeps are scripts with an explicit manifest.** Localization, RTL,
responsive, a11y: a codemod against a committed checklist plus a gate that
proves coverage — never "walk every page and fix X". "Every page" is unbounded,
so the worker cannot know when it is done and keeps reading. *Evidence:* the
`s10` wedge; `s10c-localization-sweep` had the same shape.

**R4 — Bodies carry interfaces.** Name the exact components, props, classes,
tokens, endpoints, and testids a slice consumes or produces. Dep summaries are
one line and never enough, so a missing interface is re-derived from source by
every worker that needs it. *Evidence:* 382 read calls re-derived shared-layer
APIs; 871 re-derived peer slice patterns.

**R5 — Global invariants live once, in gates.** Cross-cutting checks (no
arbitrary values, testids intact, no gradients) go in one shared script invoked
via `Verify:`/`verifyDefaults`, not in every body's prose checklist — prose is
advisory, a gate fails the build. *Evidence:* 49 guard greps re-run across
workers and reviewers instead of living in one gate.

**R6 — No audit-only or no-op slices.** Evidence work folds into the consuming
slice or becomes a gate; a slice whose deliverable is evidence must also
produce the change that consumes it. An audit-only slice has no observable done
state, so it loops or reports done with nothing. *Evidence:*
`s10b-topbar-clock` was a zero-diff no-op (shipped in `s2-shell`); `s11a` was
evidence-only.

**R7 — Preflight the tree before authoring.** Work that already exists never
becomes a slice; `Skip: true` parks the rest. Roadmaps are authored against
plan documents, not the current tree, so re-specifying shipped work spends a
full pipeline on a zero-diff slice. *Evidence:* `s10b` above.

**R8 — Trailer discipline.** `Effort:` always; `Verify:` repo-real exit-0
commands (no `|| true`, no duplicates, `sh -c '...'` when a chain shares shell
state); `Timeout:` only when >15m; `Retries: 1`; `Files:` accurate — it bounds
the worker and feeds the audit. Trailers are executable policy: a vacuous gate
lands broken code silently, a split state chain is a no-op gate (lint error).
Details: `ompo-format.md`.

**R9 — Dependency shape vs parallelism.** Slices with no dependency path
between them must have disjoint `Files` sets; overlap needs an ordering edge.
`ompo run --jobs N` runs independent slices concurrently, so unordered overlap
becomes concurrent edits to the same files off the same base — which surfaces
as failed slices, not a plan bug. *Evidence:* 27 shared files across slices
with no ordering discipline.

**R10 — Body is the whole spec.** Stay within `specBudget` (12k chars default);
acceptance criteria are observable checks, not prose. The compiler truncates
dep summaries first and the body second, and errors when the body alone exceeds
the budget. *Evidence:* the 77% re-read rate is this failure at read time.
