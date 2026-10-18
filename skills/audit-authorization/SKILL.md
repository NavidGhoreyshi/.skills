---
name: audit-authorization
description: Prove who may do what to which resource with paired entitled and unentitled probes across the whole project. Use when the user wants an authorization, access-control, or permissions audit — or when `audit-loop` selects this branch.
---

# Authorization audit

Use this branch when the user selects **Authorization audit**.

> Shared protocol — fix-mode contract, ledger convention, order-of-effects, repo-not-host fixes, unproven handling — is stated once in `audit-loop`.

## Goal

Prove the complete grid of who may do what to which resource, at every boundary in code. Scope is the **whole project**, not a sample — every resource path, every subject, every enforcement point, proven or marked unchecked.
One missed scope check is a cross-tenant read, and a route guarded only in the UI is reachable by a request.

## Rules of engagement

- **Probe only owned instances.** Local or staging with seeded tenants. Never probe production tenants or real user data.
- **Seed one identity per subject.** Paired probes need distinct anonymous, member, owner, admin, and service callers against the same seeded records.
- **Least access first.** Start anonymous, then escalate one subject at a time. Stop at the first unexpected allow and record it.
- **Destructive routes need the operator's call.** State-changing admin, billing, membership, and delete paths run only against seeded data, or with explicit approval.
- **Never print secrets or personal data.** Record fingerprints and counts, never values or rows you did not create.
- **No UI verdicts.** A hidden button proves nothing about the route behind it.

## Subject and enforcement inventory

1. **List subjects.** Anonymous, authenticated user, workspace or tenant member, owner, platform admin, service accounts, scheduled jobs.
2. **List objects.** Tenant or workspace, record, file, endpoint, job, money, other users data.
3. **Enumerate enforcement points from code.** Middleware, per-route role checks, scoping helpers, row-level filters, ownership predicates.
4. **Record one row per resource path.** Path, method, enforcement point file and line, claimed subject set.
5. **Mark intent as unproven.** A guard described in comments, docs, or UI is `unchecked` until located in the running code path.

Record the layer each point sits at:

| Layer | Examples | What its absence costs |
|---|---|---|
| Edge | Auth middleware, tenant resolution | Anonymous or wrong-tenant requests reach handlers |
| Route | Per-route role check, admin gate | Entitled-shape requests succeed for the wrong subject |
| Data | Scoping helper, row filter, ownership predicate in the query | Handler runs scoped to the wrong tenant or none at all |

A path with no point at any layer stays `unchecked` — the matrix records the gap, never a guess.

## Method

1. **Fix subjects and objects.** Freeze the subject list and the object list above before probing. Add service-to-service callers and cron identities explicitly.
2. **Map enforcement points.** For each route and data path, record what actually guards it — middleware chain, role check, scope helper, row filter, ownership predicate. Cite file and line. Never derive this from intent or from a UI that hides a control.
3. **Build the matrix.** One row per resource path, one column per subject. Mark each cell **allowed**, **refused**, or **unchecked**. Unchecked means no enforcement point was located, and unchecked is the finding.
4. **Probe at the boundary with a positive control.** For every unchecked or doubtful cell, send the request as the unentitled subject and confirm the refusal, **then send the same request shape as an entitled subject and confirm it succeeds**. A refusal without its passing twin proves nothing.
   - Cross-tenant reads and writes with a second tenant's records, files, and jobs.
   - Identifier substitution: another tenant's id in the path, body, and query of an otherwise entitled request.
   - Privilege escalation: member replaying owner-only and admin-only shapes unchanged.
   - Destructive admin routes: delete, ban, refund, and role-grant shapes as each subject.
   - Invite and membership edges: accept, revoke, re-use, and cross-workspace replay.
   - Service-to-service trust: unsigned, replayed, and wrong-scope caller credentials.
5. **Check the data path.** For each write and read path, record whether the ownership predicate sits in the query itself or is applied afterwards, and whether a missing predicate fails closed or returns data. Prefer predicates that scope the query over filters that discard rows after the fetch.

| Resource path | Anonymous | Member | Owner | Admin | Service |
|---|---|---|---|---|---|
| `GET /t/:id/records` | refused | refused cross-tenant | allowed own | allowed | refused |
| `DELETE /admin/users/:id` | refused | refused | refused | allowed | unchecked |

## Proof standards

- **Pairs only.** Request and response pairs, not code reading. Each cell cites both halves of the pair — unentitled refusal plus entitled success.
- **Label guard-read cells.** A cell proven only by reading the guard is labelled `guard-read` and can never be marked allowed.
- **State how each cell was proven.** Probe output, seeded subjects, exact request shape. No standing allows.
- **Record the refusal shape.** Status, body, and whether a 404 masks a forbidden — a mask is noted, never assumed to be a deny.
- **Fail closed or finding.** A missing predicate that returns data instead of nothing is an allow, not an unchecked.
- **Reproduce the refusal.** Exact command, observed status and body, expected status. Record negatives with the same care as allows.
- Proof-status labels and host-side confirmation follow the shared protocol in `audit-loop`.

## Ledger

`docs/authorization-audit-findings.md`, IDs `AUTH-001`… Columns follow the shared convention — location, evidence, impact, classification, proof status — plus subject, resource, and the probe that proved the cell.

## Repair rules

- **Fix at the guard, not the route.** A missing scope check repeated across siblings gets one shared guard plus a sweep of every sibling in the same change.
- **Ship the regression with the fix.** Every authorization repair lands with a test that fails before the fix and passes after — cross-tenant or wrong-role attempt denied.
- **Re-run the probe.** The probe that found the cell is re-run to prove the cell moved from unchecked or allowed to refused.
- **Call out breaking changes.** Stricter scoping that locks out current callers is recorded as breaking with the affected subjects named.

## Authorization completion criteria

- Every resource path has a matrix row with an enforcement point cited from code.
- Every cell is allowed, refused with its positive control, or unchecked with a finding.
- Every unchecked cell carries a probe pair and a ledger row.
- No refusal stands without its passing twin; no allow stands on a guard-read alone.
- Every repair has its failing-before and passing-after regression plus a re-run probe.
- `docs/audit-progress.md` and `docs/authorization-audit-findings.md` hold the complete dated run.

*Done when no unchecked cell lacks a finding, no refusal lacks its passing twin, and every repair proves its moved cell.*
