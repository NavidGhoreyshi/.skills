# Evidence — run `20260916-va5e9b`

One real ompo run against a React dashboard (68 files edited, 22 slice dirs).
Artifacts live at `<project>/.omp/roadmap/runs/20260916-va5e9b/`. These numbers
motivate both the runtime handoff fixes in ompo and this skill.

- **66 worker generations, 4,684 tool calls.**
- **30 context-cap handoffs, 30/30 briefs carried no state** — every notes
  section read `(none — reconstruct state from the worker log tail and the
  branch diff below.)`, and there was no diff below. Workers resumed from
  nothing.
- **77% of reads were re-reads:** 1,715 of 2,221 reads hit files an earlier
  generation or slice had already read; 763 of 2,058 reads in multi-generation
  slices were cross-generation.
- **Top-10 files were 35% of all reads** (`MembersPage.jsx`: 152 reads across
  12 slices).
- **27 of 68 edited files were edited by >1 slice** — `Modal.jsx` and
  `MembersPage.jsx` ×4, `index.css` and `CameraModal.jsx` ×3.
- **49 global guard greps** re-run across workers and reviewers instead of
  living in one gate.

The wedges:

- `s10-language-rtl-digits`: 13 generations, 749 reads, **zero edits**, killed —
  a "walk every page" sweep with no manifest and no bounded `Files`.
- `s11a-responsive`: killed after 3 generations, zero edits (read-only recon).
- `s10b-topbar-clock`: zero-diff no-op — work had already shipped in `s2-shell`.
- `s11a`: evidence-only deliverable, so it could never finish.

The handoff failure, concretely: a cap abort kills the worker at the token cap;
the only state channel was the brief, which carried no notes, no diff, and
run-dir-relative refs while the worker's cwd was the worktree — generations
burned turns on `ls slices/…` → `tool bash FAILED`, then hunted with `find`.

Runtime fixes now ship in ompo: the brief carries preserved commits, a bounded
diff, the NOTES.md tail, the worker log tail, and absolute paths; the contract
asks workers to maintain NOTES.md; and cap generations with no file progress
stop respawning. Composition is what prevents the wedge in the first place.
