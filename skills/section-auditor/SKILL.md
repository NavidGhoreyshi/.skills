---
name: section-auditor
description: Audit and repair one frontend page or SPA view with its backend integration. Use when asked to find logical bugs, dead components, abandoned API wiring, missing validation or authorization, bad state handling, edge-case failures, or insufficient tests, then prove the fixes.
---

# Section Auditor

Audit only the supplied work unit, using the tree as a map. Inspect current source, architecture, runtime contracts, and tests.

Trace rendering, loading, empty, error, disabled, responsive, locale, and permission states; state transitions, stale data, concurrency, retries, optimistic updates, navigation; UI requests, routes, actions, validation, authorization, persistence, serialization, external integrations; dead links, hardcoded data, abandoned wiring, mismatched payloads, unsafe assumptions, observability, security, privacy, compatibility, performance.

Prove every control and datum, not just that the page renders:

- **Data source:** every displayed value resolves to a backend field, derived value, or explicit static-by-design element. A hardcoded literal in a data slot is a finding.
- **Action wiring:** every control reaches a backend call or documented client-only behavior. Missing/no-op handler is a finding.
- **Endpoint truth:** resolve every API wrapper to a real route + method with matching request/response shape in `urls.py` + views/serializers — never trust the wrapper's comment.
- **Round-trip:** for each editable field, verify load→save against the serializer's actual field list; swapped/nonexistent fields are findings.
- **Hidden failures:** swallowed errors, `catch {}` → `[]`/`null`/`0`, "best-effort" paths, hardcoded fallbacks, dummy arrays, `Phase 2` / `assumed` / `pending BE confirm` stubs — findings, not degradation.

List findings before fixing; classify each `confirmed bug` / `missing test` / `intentional` / `uncertain`. Repair behavior follows the audit mode (set by the orchestrating audit-loop skill):

- **Auto-fix:** autonomously fix every confirmed in-scope issue; add or strengthen focused tests.
- **Interactive:** change no code; report each confirmed issue with evidence + a concrete recommended fix so the user can decide on each one.

Mode not stated → ask before fixing. No redesigns, no scope creep.

Discover the project's real commands. Run targeted tests, then relevant unit/feature/integration/build/headless-Chromium checks. Prove each mutation with a test hitting the endpoint or a browser action asserting the network request + resulting state — a zero-error render smoke is not proof. Add coverage until checks pass. Never claim success when code, tests, checks, dependencies, or environment are unavailable: distinguish environmental failures and stop with a blocker report.

Report every finding (incl. non-bugs and unresolved), fixes + rationale, changed files, data/security/compat effects, exact commands + pass counts, remaining risks. No commit, deploy, reset, stash, or edits outside the supplied project.
