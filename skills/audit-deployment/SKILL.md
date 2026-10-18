---
name: audit-deployment
description: "Prove the serving artifact matches the repo and the project can be deployed, reverted and restored on purpose. Use when the user wants a deployment, release, or parity audit — or when `audit-loop` selects this branch."
---

# Deployment audit

Use this branch when the user selects **Deployment audit**.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Prove the thing serving users is the thing in the repository, and the project can be deployed, reverted, and restored on purpose. Cover the **whole project** — every environment, surface, queue, schedule, and flag — not a sample. Written because the failure is almost never a bug in the code: it is a stale artifact, a push that never deployed, a local-only env value, a one-environment migration, or a backup nobody restored.

## Rules of engagement

- **Read live, change nothing.** Reading live config, schema, certs, and artifact identity is in scope; changing them is not.
- **Deploying, rotating, or changing platform env is the operator's call.** Record the finding and the exact command; do not execute it.
- **Never trigger deploys, rollbacks, restores, or migrations.** Propose the one command; let the operator run it.
- **Never print a secret value.** Record store path, mode, length, and prefix fingerprint only.
- **Probe production read-only.** No writes, no restores into live databases, no load against live endpoints.

## Surface inventory

Enumerate every environment and what runs it before probing anything.

- **List every environment:** production, staging, preview, local — plus anything else serving traffic.
- **Identify each surface:** host, service, container, edge function, static host, worker, queue consumer, scheduler.
- **Record the running artifact:** commit sha, image tag, build time, release id — from the running process, not the dashboard.
- **Record the deploy path:** webhook, CI pipeline, manual push, platform auto-deploy — plus who can trigger it.
- **Record domains and TLS:** every domain per environment with certificate expiry read from the live endpoint.
- **Record scheduled work and supervision:** cron entries, schedulers, retry policy, and what restarts them.
- **Record workers and queues:** queue names, consumers, dead-letter handling, and backlog source.

| Environment | Surface | Running artifact | Deploy path | Evidence |
|---|---|---|---|---|
| prod | app host + worker | commit sha / image tag / build time | CI pipeline + trigger | version endpoint output, deploy log id |
| staging | preview service | commit sha / image tag / build time | branch auto-deploy | version endpoint output, deploy log id |
| prod | scheduler + queues | job ids / consumer count / backlog | platform schedule config | scheduler listing, queue depth output |

## Parity

Prove the running system matches the repo, the schema, the env, and the flags.

- **Artifact parity:** compare running commit and build time against the repo HEAD and the CI build that produced it; a push with no deploy is a finding.
- **Schema parity:** compare applied migrations read from the live database against the migrations directory; list applied vs pending per environment.
- **Env parity:** compare every variable the code reads against what the platform injects per environment; flag values that exist only in a local `.env` no deploy reads.
- **Flag parity:** list every feature flag, its live value per environment, its default in code, and where the override lives.
- **Stale-artifact check:** confirm the newest merged commit is the running one; anything newer in the repo than on the host is drift, not history.

## Recovery drill

Prove the project can be reverted and restored on purpose — without performing the revert.

- **Rollback:** name the one rollback command, the artifact it restores, and whether it was dry-run or operator-confirmed; a rollback that needs invention is a finding.
- **Restore:** restore the latest backup into a scratch database and report success or the exact failure; never restore into live.
- **Migrations:** state per migration whether it is reversible or forward-only, and confirm that direction is stated in the repo, not assumed.
- **Recovery docs:** confirm the runbook names backup location, retention, restore command, and expected duration — or record its absence.

## Probe set

One probe per claim, against the live thing — each producing evidence a reviewer can re-run.

- **Artifact probe:** read commit/build identity from the running process or version endpoint; pair with the repo HEAD and CI record.
- **Schema probe:** read the applied migration set from the database itself, never the migrations directory.
- **Env probe:** read injected env from the running process or platform inspection command, never a config file or `.env`.
- **Cert probe:** read expiry dates from the live TLS handshake per domain, never the dashboard.
- **Queue probe:** read backlog, consumer count, and dead-letter depth from the queue, not the deploy log.
- **Restore probe:** run the backup restore into scratch storage and keep the command plus its output.

## Proof standards

- **A claim is not a write:** read the code that is actually running, not the build on disk; read applied schema from the database, not the directory.
- **Pair every negative with a positive control:** a missing deploy, missing var, or clean cert proves nothing until the same request shape succeeds for something entitled and current.
- **Never print a secret value:** record fingerprint (store path, mode, length, prefix) and prove liveness by a call that uses it, not by displaying it.
- **A finding needs a reproduction:** exact command, live output, expected state, and the code or platform path that permits it — repeatable by someone else.
- **Unproven stays unproven:** proof-status labels, re-run rule, and host-side confirmation live in the shared protocol in `audit-loop`.

## Ledger

`docs/deployment-audit-findings.md`, IDs `DEP-001`…: environment, surface, probe, observation, evidence (command plus output), impact, classification, remediation (exact operator command), status. Columns follow the shared convention in `audit-loop`, plus environment and surface per row.

## Repair rules

- **May fix automatically:** version endpoint or build-stamping gaps, missing runbook statements, forward-only migration labels, `.env.example` drift — repo-only changes, no live effect.
- **Needs the operator:** deploys, rollbacks, restores, migration runs, env or secret rotation, cert renewal, queue or scheduler changes — record the exact command and stop.
- **Fixes live in the repo, never on the host:** no hand-editing a running container, no live database edits to force a pass; a fix is `verified live` only after a deploy plus a re-run.

## Deployment completion criteria

The deployment branch is complete only when:

- Every environment and surface has a row with running artifact, deploy path, and evidence.
- Every parity check (artifact, schema, env, flags) has a verdict per environment.
- Rollback, restore-into-scratch, and migration reversibility each have a proven or explicitly unproven result.
- Every probe names its live source, command, and output; no config-file or dashboard claim stands alone.
- `docs/audit-progress.md` and `docs/deployment-audit-findings.md` contain the complete dated run.

*Done when the serving artifact is identified per environment, parity and recovery each have evidence, and the next operator command is named.*
