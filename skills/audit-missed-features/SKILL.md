---
name: audit-missed-features
description: Walk the product page by page and component by component, propose missing interactions grounded in existing capabilities, and record the user's decision on each. Use when the user wants a missed-features assessment, feature-gap review, or "what is missing here" pass — or when `audit-loop` selects this branch.
---

# Missed-features assessment

Use this branch when the user selects **Missed-features assessment**.

## Goal

Find potentially useful interactions that are absent from an existing page or component even though the product already has related data, routes, actions, or workflow concepts. This is a product-discovery conversation, not a bug hunt.

The assessor may suggest:

- Missing navigation or contextual links.
- Add/edit/delete/restore/archive/retry/cancel controls.
- Filters, search, sorting, pagination, saved views, clear filters, or deep-link state.
- Preview, compare, print, export, download, copy, share, or “open in related workflow” actions.
- Status transition controls and visible next actions.
- Empty/loading/error/retry/success/disabled states.
- Bulk actions where the existing model and permissions already support them.
- Accessibility affordances: labels, keyboard actions, focus restoration, announcements, and non-color status.
- Locale/theme/direction affordances.
- Responsive/mobile equivalents of desktop interactions.
- Related-record context already available elsewhere in the product.

The assessor must not suggest unrelated features such as billing, booking, subscriptions, public registration, automatic notifications, or other roadmap non-goals unless the user explicitly asks to reconsider product scope.

## Stable one-by-one order

Create the inventory before starting discussion. Use this order unless the user asks for a different order:

1. Public layouts and public pages.
2. Authentication and recovery pages.
3. Primary authenticated layout and pages.
4. Secondary/role-specific layouts and pages.
5. Shared components that are not fully covered by their owning page.
6. Cross-cutting controls: locale, theme, navigation, dialogs, uploads, status chips, empty/error states.

Within each unit, inspect in DOM/product order: page header/navigation, primary action, filters/tabs, forms, lists/cards/tables, row actions, related links, status/state feedback, empty/loading/error states, responsive behavior, and accessibility affordances.

## Per-unit protocol

For each page or component, do all of the following before moving on:

1. Identify the page's purpose, role boundary, route, existing data, existing actions, and related workflows.
2. Enumerate every current control and data-bearing element.
3. Compare the available product capabilities against what the surface exposes.
4. Propose only concrete candidate additions grounded in existing features, routes, data, permissions, or established UI patterns.
5. Present a short numbered list of proposals to the user. Each proposal must include:
   - a concise name;
   - the proposed interaction/tool;
   - why it follows from existing page/product capabilities;
   - any dependency or privacy/authorization concern.
6. Ask the user to classify each proposal:
   - **Needed** — approve it for implementation or the next repair queue.
   - **Intentionally left out** — record it as an explicit product decision; do not implement.
   - **Defer** — record it for a later roadmap item; do not implement now.
   - **Not applicable** — discard it with a reason.
7. Record the user's decisions immediately in the assessment ledger before presenting the next unit.
8. If no candidates exist, record `No additional interaction identified after review` and move on.

Never silently infer “needed” from the user's silence. If the user skips a proposal, mark it `unresolved` and ask again before implementation or before closing the assessment.

## Assessment ledger

Maintain a ledger in `docs/missed-features-assessment.md` unless the user explicitly requests another location. Each unit should include:

```markdown
## Unit: <page or component>

- Route/file:
- Role/access:
- Existing capabilities:
- Existing controls/data reviewed:

| ID | Candidate interaction | Existing capability basis | User decision | Notes/dependencies |
|---|---|---|---|---|
| MF-001 | ... | ... | Needed / Intentionally left out / Defer / Not applicable / Unresolved | ... |
```

Use stable IDs (`MF-001`, `MF-002`, …). Never overwrite prior assessment history; append a new dated run if the same unit is reassessed.

## Missed-feature implementation rules

- In **manual fix mode**, after the one-by-one assessment has finished, show the approved `Needed` list and ask which approved items to implement. Do not modify code during the conversational assessment unless the user explicitly requests an immediate implementation for that item.
- In **automatic fix mode**, automatically implement only proposals classified `Needed`, and only after the entire selected inventory has been assessed. Still ask the user for every unit and every proposal; automatic mode means automatic execution after approval, not automatic product decisions.
- `Intentionally left out`, `Defer`, `Not applicable`, and `Unresolved` items must not change application code.
- New backend-backed capabilities require `audit-api-wiring`'s full contract: migration compatibility, authorization, validation, persistence, focused tests, and freshly authored E2E coverage.
- Presentation-only additions still require build, accessibility, responsive, translation, and relevant browser verification.
- Every approved item must have a decision rationale and a proposed acceptance check before implementation.

## Missed-features completion criteria

The branch is complete only when:

- Every inventory unit has been reviewed in order or explicitly marked out of scope.
- Every proposal has a user decision; no silent approvals.
- The ledger distinguishes approved, intentionally omitted, deferred, not-applicable, and unresolved ideas.
- Approved implementation work is separated from discovery and has acceptance checks.
- Backend-backed approvals are promoted into the `audit-api-wiring` contract and receive focused tests/E2E.
- `docs/missed-features-assessment.md` records the full dated run and remaining deferred ideas.
