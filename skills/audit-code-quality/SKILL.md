---
name: audit-code-quality
description: Measure and reduce maintainability debt — duplication, dead code, complexity, inconsistent patterns, unsafe type escapes, missing error handling — without changing observable behavior. Use when the user wants a code quality audit backed by before/after measurements and behavior-preserving repairs — or when `audit-loop` selects this branch.
---

# Code quality audit

Use this branch when the user selects **Code quality audit**.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Measure and reduce maintainability debt across the codebase **without changing observable behavior**. This branch is not a style debate: every finding is backed by a measurement or a concrete future-failure scenario, and every repair is proven behavior-preserving.

## Rules

- **Behavior is frozen.** Contracts, serialized shapes, URL patterns, permissions, and user-visible copy do not change under this branch. If a behavior looks wrong, it belongs to `audit-api-wiring` or `audit-security`, not here.
- Prefer deletion over abstraction. Do not introduce an abstraction for a single call site; do not create a shared helper that the codebase then ignores.
- No reformat-the-world commits. Keep each change scoped to one finding and reviewable.
- Remove what a change obsoletes in the same change: dead code, dead exports, obsolete comments, superseded aliases, and tests that only assert the old implementation.

## Measurement phase

1. Record the toolchain first: the project's lint, typecheck/compile, format, test, and build commands, and whether CI enforces them.
2. Establish a **baseline before touching code** — raw numbers, not impressions: file/LOC counts, largest files, duplicate blocks, dead exports, TODO/FIXME/HACK markers, `any`/unsafe-cast/`@ts-ignore` (or the language's equivalent escape hatches), disabled lint rules, swallowed errors, and current test/lint/type output. Record it in the progress doc and keep machine output as an artifact.
3. Map the code into units (reuse `docs/ui-tree.md` units where they exist; otherwise group by module/directory).
4. Run the mandatory searches below over the whole codebase, then classify each hit.

## Mandatory searches

- **Duplication and drift** — the same logic, constant, or validation implemented twice with subtle differences; copy-pasted blocks that have already diverged; two conventions for the same job (two HTTP clients, two date formatters, two error shapes).
- **Dead weight** — unreachable branches, never-called exported functions and components, unused parameters/imports/fields, endpoints or wrappers with no consumer, commented-out code, feature flags that are permanently on or off.
- **Complexity and size** — god files/functions by the project's own thresholds, deep nesting, long parameter lists, boolean-flag arguments, functions doing several unrelated things, duplicated conditionals that a single lookup could replace.
- **Error handling** — swallowed catches, empty fallbacks that fabricate success, errors logged and dropped, missing failure paths for I/O and network calls, retries without backoff or idempotency, cleanup that never runs on the error path.
- **Type and contract safety** — escape hatches (`any`, unsafe casts, non-null assertions, ignored diagnostics) that hide real nullability or shape mismatches; hand-written types duplicating generated ones; validation that exists in one layer and is trusted in another.
- **Data access and resources** — queries in loops (N+1), unbounded list loads, missing indexes for hot filters (as evidenced by query shape), connections/handles/timers not released, synchronous I/O on hot paths, work repeated per request that could be computed once.
- **Naming and structure** — names that mislead about behavior or units, modules whose contents no longer match their name, layer violations (a UI module importing persistence internals), inconsistent placement of new code versus established convention.
- **Test quality** — tests asserting implementation details or mock echoes, tests that cannot fail, snapshot sprawl, missing coverage on branching business rules, duplicated fixtures that drift, skipped tests with no owner.
- **Comments and documentation drift** — comments that contradict the code, docblocks for deleted parameters, README/setup steps that no longer work.

## Classification

- `confirmed defect` — a maintainability problem with a concrete failure mode (a bug waiting to happen, a divergence already causing inconsistent behavior, a resource leak), with the failure scenario stated.
- `debt` — measured but not currently harmful; quantified so the trend can be tracked.
- `intentional` — deliberate, with the reason found in code, docs, or history.
- `unproven` — suspected but not established; state the check that would settle it.
- Severity is blast radius × change risk: how much of the system depends on the code, and how dangerous touching it is.

## Repair rules

- One finding, one focused change, behavior preserved.
- Refactor in verifiable steps, keeping the suite green between steps; never combine a refactor with a behavior fix.
- Every removal is proven un-used (search + build + test), not merely assumed unused.
- Prove behavior preservation: the existing suite green, plus a targeted assertion for any behavior the previous tests did not pin.
- Re-measure the same baseline metric after the repair and record the delta.

## Code quality completion criteria

The code quality branch is complete only when:

- The baseline and final measurements are recorded for every metric that was measured.
- Every finding is classified with evidence and a location, and every `confirmed defect` is fixed or explicitly deferred with rationale.
- No behavior change shipped under this branch without a stated reason and proof.
- Lint, typecheck, tests, and build are green at the end, or the remaining failures are pre-existing and named.
- Remaining debt is listed with the reason it was left.
