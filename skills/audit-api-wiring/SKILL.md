---
name: audit-api-wiring
description: "Audit frontend/backend wiring end to end: routes, components, API contracts, permissions, persistence, state transitions, privacy, and browser proof. Use when the user wants a complete API wiring audit of a project's routes and data paths — tracing every read and write, classifying gaps, and repairing confirmed defects with focused regressions — or when `audit-loop` selects this branch."
---

# API wiring audit

Use this branch when the user selects **API wiring audit**.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Discovery phase

Before changing application code:

1. Run `git status --short --branch` and record the baseline.
2. Enumerate all frontend routes/pages, layouts, loading/error boundaries, shared components, hooks, utilities, API modules, backend routes, controllers/views, presenters/serializers, models, policies, middleware, migrations, signals/tasks, external integrations, cache paths, and relevant tests.
3. Refresh `docs/ui-tree.md` while preserving stable IDs and historical entries.
4. Build a global wiring inventory. For every unit, list every control, datum, read/write path, permission check, persistence effect, external integration, and proof status.
5. For every read, trace:

   `UI field → wrapper/visit → URL/method/query → auth/role → validation → controller/service → model/relation → presenter/response → frontend render/fallback`.

6. For every write, trace:

   `control → disabled/loading state → URL/method/content type → payload → auth/ownership → validation → transaction/persistence → events/jobs/cache → response/flash → reload-visible result`.

7. Inspect empty, loading, malformed, 4xx, 5xx, timeout, retry, refresh, duplicate, stale, inactive, archived, deleted, responsive, keyboard, RTL/LTR, and privacy cells as applicable.
8. Perform mandatory searches for wrapper/route mismatches, field/presenter mismatches, catches/fallbacks, mocks/hardcoded data, dead controls/routes, authorization gaps, cache invalidation, pagination, lifecycle transitions, reverse relations, and status-only tests.

Discovery must be completed across all mapped units before repairs are narrowed to individual findings.

## Repair phase

- Re-run affected unit, feature, build, type/lint, translation, accessibility, responsive, and browser checks.

Fix modes, regression rules and unproven handling: the shared protocol in `audit-loop`.

## API audit completion criteria

The API wiring branch is complete only when:

- Every mapped unit has an inventory and state-matrix result.
- Every control and datum has a traced contract or an explicit classification.
- Every confirmed defect has a fix and matching regression, or a documented intentional decision.
- Browser proof distinguishes implementation failures from harness/environment failures.
- Unproven cells, deployment limits, concurrency gaps, and product/schema decisions are listed.
- `docs/audit-progress.md` and `docs/wiring-audit-findings.md` contain the complete audit record.
