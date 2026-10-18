---
name: audit-security
description: Hunt exploitable authentication, authorization, tenancy-isolation, input-handling, secret-management, and data-exposure defects, with a reproducible probe for every claim. Use when the user wants a security audit proven at trust boundaries rather than argued from theory — or when `audit-loop` selects this branch.
---

# Security audit

Use this branch when the user selects **Security audit**.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Find defects an attacker could actually use: authentication, authorization and tenancy isolation, input handling, secret management, data exposure, abuse resistance, and configuration. Prefer provable exploit paths over theory, and prove denial of access as deliberately as you prove access.

## Rules of engagement

- **Non-destructive and authorized.** Probe only local, staging, or self-owned instances. Never attack production, a third party, or real user data. No destructive payloads, no denial-of-service, no brute force, no data exfiltration beyond the minimum needed to prove the issue.
- Prove leakage with the least data that settles it (a count, a redacted field, a single row you created). Never paste real secrets, tokens, or personal data into the ledger; record the credential name and redact the value.
- Rotate any credential that was committed or exposed; record the action taken, not the value.
- Severity is impact × exploitability, not code aesthetics. Always state who can reach the defect: anonymous, any authenticated user, any member of a tenant, an admin of the same tenant, or only a privileged insider.

## Inventory phase

1. Enumerate every trust boundary: public routes, authenticated routes, role-gated routes, admin routes, webhooks, cron/task endpoints, background jobs, share/public-token endpoints, file uploads and downloads, outbound fetches, third-party callbacks, and the authentication/session layer itself.
2. For every state-changing endpoint, record: required authentication, required role, object ownership rule, tenancy scoping rule, validation rule, and rate limit.
3. Then run the probe set below. Each probe ends as `proved vulnerable`, `proved denied`, `unproven` (with the precondition that would settle it), or `not applicable` (with a reason).

## Probe set

1. **Authentication** — session/token issuance and validation, expiry and revocation, magic-link/OTP replay, password or code reset paths, session fixation, cookie flags (HttpOnly/Secure/SameSite), CSRF protection on state-changing requests, logout invalidation, remember-me semantics.
2. **Authorization** — every state-changing endpoint probed with: no session, wrong role, and a second tenant's object id. Include mass-assignment of role/status/ownership fields, hidden-field writes, IDOR on ids supplied by the client, admin-only routes, and "hidden" UI actions that the API still accepts.
3. **Tenancy isolation** — for read and write paths, prove that a client-supplied id (workspace/tenant/account/record) cannot reach another tenant's data when the server derives the scope from the session, and that any path which trusts a client-supplied scope is closed.
4. **Input handling** — injection (SQL/ORM, template/HTML, header, log), XSS sinks (raw HTML injection, unescaped user content), path traversal, SSRF on server-side fetches of user-supplied URLs, open redirects, unsafe deserialization, file upload type/size/executable handling, and CSV/formula injection on export where applicable.
5. **Secrets and cryptography** — hardcoded keys or tokens, secrets in client bundles, logs, or error messages, committed env files, encryption-at-rest for personal data, hashing vs reversible encryption, HMAC/signature verification (constant-time compare, correct secret, replay window), key rotation, tokens leaked into URLs, referrers, or analytics.
6. **Data exposure** — API responses returning more than the surface needs (tokens, internal ids, personal data, other tenants' rows), stack/SQL detail in errors, public or share-token endpoints' scope, cache keys that mix tenants, and debug/diagnostic endpoints that leak infrastructure detail.
7. **Abuse resistance** — rate limits on authentication, expensive, and outbound-facing routes; webhook replay protection and idempotency for side-effecting operations; pagination caps and unbounded queries; resumable/retryable operations that can double-charge, double-send, or double-write.
8. **Platform and configuration** — dependency advisories for the pinned versions, permissive CORS, missing security headers, TLS assumptions, default credentials, verbose errors in production, and overly broad file or bucket permissions.

## Proof standards

- A finding is `confirmed` only with a reproducible probe: the exact request/action, the observed result, the expected result, and the code path that permits it. Keep the probe in the ledger in a form a reviewer can re-run against a local instance.

Protocol for the cut proof-status items is stated in `audit-loop`.

## Repair rules

- Fix at the boundary, not the call site: if a missing check recurs across sibling endpoints, add the shared guard and sweep every sibling in the same change.
- Add red/green regressions: the probe must fail against the previous code and pass after the fix. For authorization defects, the regression is the cross-tenant or wrong-role attempt being denied.
- Never weaken or delete an existing control to make a test or a UI flow pass; never log a secret to explain a fix.
- Behavior changes that affect real users (session invalidation, stricter validation, rotated credentials) are recorded as breaking and called out explicitly in the report.

## Security completion criteria

The security branch is complete only when:

- Every trust boundary and state-changing endpoint has an authentication/role/ownership/validation classification with evidence.
- Every confirmed vulnerability has a fix plus a matching red/green regression, or an explicitly deferred entry with rationale and risk.
- Non-exploitable and unproven items list their preconditions.
- The ledger contains no unredacted secrets or personal data.
- `docs/audit-progress.md` and `docs/security-audit-findings.md` contain the complete record.
