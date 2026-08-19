---
name: section-auditor
description: Audit and repair one frontend page or SPA view with its backend integration. Use when asked to find logical bugs, dead components, abandoned API wiring, missing validation or authorization, bad state handling, edge-case failures, or insufficient tests, then prove the fixes.
---

# Section Auditor

Audit only the supplied work unit. Use the tree as a map, then inspect current source, architecture, runtime contracts, and tests.

Trace rendering, loading, empty, error, disabled, responsive, locale, and permission states; state transitions, stale data, concurrency, retries, optimistic updates, and navigation; UI requests, routes, actions, validation, authorization, persistence, serialization, and external integrations; dead links, hardcoded data, abandoned wiring, mismatched payloads, unsafe assumptions, observability, security, privacy, compatibility, and performance.

Prove every control and every datum, not just that the page renders:

- Data source: each displayed value must resolve to a backend field, a derived value, or an explicit static-by-design element. A hardcoded literal in a data slot is a finding.
- Action wiring: each interactive control must reach a backend call or a documented client-only behavior. A missing or no-op handler is a finding.
- Endpoint truth: resolve every API wrapper to a real route + method with a matching request/response shape in `urls.py` + views/serializers — never trust the wrapper's own comment.
- Round-trip: for each editable field, verify load→save against the serializer's actual field list; swapped or nonexistent fields are findings.
- Hidden failures: swallowed errors, `catch {}` → `[]`/`null`/`0`, "best-effort" paths, hardcoded fallbacks, generated/dummy arrays, and `Phase 2` / `assumed` / `pending BE confirm` stubs are findings, not acceptable degradation.

List findings before fixing and classify each as confirmed bug, missing test, intentional behavior, or uncertain. Repair behavior depends on the audit mode chosen by the user (typically set by the orchestrating audit-loop skill):

- **Auto-fix mode:** autonomously fix every confirmed in-scope issue and add or strengthen focused tests.
- **Interactive mode:** do **not** change code. Report every confirmed issue with evidence and a concrete recommended fix so the user can decide on each one.

If the mode is not stated, ask the orchestrator/user before fixing anything. Do not redesign or expand into unrelated work.

Discover the project's real commands. Run targeted tests, then relevant unit, feature, integration, build, and Playwright headless Chromium checks. Prove each mutation with a test that hits the endpoint or a browser action that clicks and asserts the network request and the resulting state — a render-only smoke with no errors is not proof. Add missing coverage and repeat until all relevant checks pass. Do not claim success when code, tests, browser checks, dependencies, or required environment are unavailable; distinguish environmental failures and stop with a blocker report.

Report every finding, including non-bugs and unresolved items; fixes and rationale; changed files and data, security, or compatibility effects; exact commands and pass counts; and remaining risks. Do not commit, deploy, reset, stash, or edit outside the supplied project.
