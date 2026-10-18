---
name: audit-secrets
description: Audit every credential a project depends on across code, stores, logs, and hosts with inventory, placement, echo, liveness, and separation probes. Use when the user wants a secrets audit — or when audit-loop selects this branch.
---

# Secrets audit

Use this branch when the user selects **Secrets audit**.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses, and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Prove every credential the system depends on is known, minimally placed, unexposed, live only where intended, and separated across environments. Scope is the **whole project**, not a sample — every environment, every store, every holder.

What this audit proves: no credential the system needs is unknown, no holder keeps one it does not need, no value is echoed where it can be replayed, no revoked or previous-account credential is still live, and every leak path names its cost and its operator fix.

## Rules of engagement

- **Read-only by default.** Never print, copy, or transmit a credential value — in the ledger, in messages, in logs, or in tool output.
- **Operator owns rotation.** Revocation, rotation, and panel changes are the operator's actions; the audit names the exact panel and command, never performs them silently.
- **Least proof settles it.** Prove liveness with a read-only call or panel state; stop at the minimum that answers the question.
- **Stale access is a finding.** A credential reachable by a service, checkout, snapshot, or person that no longer needs it is recorded, not excused.
- **Unknown owner is a finding.** A credential whose owner, purpose, or environment cannot be identified is recorded as such.
- **Authority boundaries.** The audit may read stores, panels, and history; it never rotates, revokes, reissues, or shares a credential. Anything that would change access needs the operator's call first.
- **Scope is holders, not just code.** A clean source tree proves nothing about panels, snapshots, mirrors, or vault grants — check every holder named in the inventory.

## Credential inventory

Enumerate before judging. One row per credential — named, never valued:

| Column | Record |
|---|---|
| Name | Credential name as the code and store refer to it |
| Authorises | What the credential grants — service, account, and capability |
| Environment | Which environment it belongs to — dev, staging, prod, CI |
| Holder | Which service or store holds it |

Sources to sweep:

- **Code reads.** Every environment read in the source — process environment access, config loaders, secret-manager clients, connection-string builders.
- **Outside-code use.** Vendor panels, payment providers, SMS and mail senders, object storage, database users, CI variables, SSH deploy keys, webhook signing secrets.
- **Forgotten holders.** Previous panels and accounts, stale checkout mirrors, host snapshots and backups, departed-member access, shared team vaults.

Close the phase only when every read in code maps to a row and every external service the project depends on maps to a row.

Record per row the store path and holder identity as precisely as the panel or mount shows them — vault path, environment-variable name, file path with mode, CI variable scope, panel account name. Vague holders ("somewhere in prod") fail the inventory.

## Probe set

Run each probe against every inventory row. Each probe ends as `confirmed defect`, `intentional` (with rationale), `unproven` (with the check that would settle it), or `not applicable` (with a reason).

1. **Placement** — for each credential, define the smallest set of services that must hold it, then list which services hold it anyway. A credential reachable by the web process that only the worker needs is a finding, not a note. Check config mounts, environment inheritance, shared vault paths, base-image layers, and CI variables injected into jobs that never use them.
2. **Echo surface** — trace where a value could be printed or persisted: application logs and error messages, tool output pasted into sessions, shell history, committed files and `git log`, checkouts holding environment mirrors, support pastes and screenshots, CI logs, database rows, backups, and snapshots on hosts. Pair every negative with a positive control: a clean log proves nothing until the same request shape shows the log does capture comparable fields.
3. **Liveness and rotation** — determine whether the credential is still valid, when it was last rotated, whether it is shared across environments, and what its blast radius is on leak. Prefer a read-only call where safe — a list-keys, describe, or permissions-check call that cannot mutate state; otherwise use the issuing panel's key list or last-used timestamp. Record how liveness was proven per row: which call or panel view, and what it showed with values redacted.
4. **Separation** — flag the same value across dev and prod, one value shared by several services, and credentials from a previous account or environment that were never revoked. Compare fingerprints, not values, across environments. The recurring incidents are the old vendor key left alive in a previous panel, the stale checkout mirror, the snapshot holding live production credentials, and the token placed where it was never needed.

## Proof standards

- **Never print a value.** Record a fingerprint per credential — store path, file mode, length, and prefix shape — plus how liveness was proven.
- **A claim is not a write.** Read the running configuration, not the documented one; the store that serves the process decides.
- **Unverified stays unverified.** A credential that could not be checked is recorded as unverified with the reason — never assumed safe.
- **Reproducible rows.** Each finding carries the exact command or panel path a reviewer can repeat, plus the observed output with values redacted.

Proof-status labels, unproven handling and host-side confirmation: the shared protocol in `audit-loop`.

## Ledger

`docs/secrets-audit-findings.md`, IDs `SCR-001…`: credential name, location, evidence (redacted citation plus probe output), impact, blast radius, classification, proof status, remediation, re-probe. No row carries a value, pasted output containing a value, or personal data.

Ledger columns follow the shared convention — stable ID, location, evidence, impact, classification, proof status — plus the secrets columns: credential name, holder location, and blast radius per row. Blast radius states what a leak would cost: which data, which accounts, which spend.

## Repair rules

- **Name the operator action.** Rotation and revocation entries state the exact panel and the exact command or click path — nothing vaguer.
- **Remove, never relocate.** Delete the stale holder, mirror, or snapshot grant; do not copy the credential to a second location to work around it.
- **Never demonstrate with a value.** No writing a value into a repository, message, log, or ticket to prove handling works — use the fingerprint and a redacted success signal.
- **Scope the blast radius first.** Before naming a rotation order, state what a leak would cost — which data, which accounts, which spend — so the operator sequences correctly.

- **Verify the fix without the value.** Re-probe the same holder with the same instrument after rotation and record before/after: old fingerprint dead, new fingerprint live, stale holders empty.
- **Sequence by blast radius.** Order operator actions by cost of leak — widest blast radius first — and say what stays unverified until the operator acts.

## Secrets completion criteria

The secrets branch is complete only when:

- Every credential read in code and every external service maps to an inventory row with no value recorded.
- Every row carries placement, echo-surface, liveness, and separation verdicts with evidence or an unproven reason.
- Every confirmed defect names the exact operator rotation or revocation step plus its blast radius.
- The ledger holds no value, pasted credential output, or personal data.
- `docs/audit-progress.md` and `docs/secrets-audit-findings.md` contain the complete dated run.

*Done when every credential is inventoried, every probe has evidence or an unproven reason, every leak path names its operator fix, and the ledger proves it without holding a single value.*
