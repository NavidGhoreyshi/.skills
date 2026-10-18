---
name: checkpoint
description: Save a session to a durable checkpoint and reload it later — the plan, locked decisions, in-flight jobs and the next action. Use when the user stops for the day, shuts the machine down or asks to save state, or on the other branch when a resumed session says keep going or asks where we left off.
---

# Checkpoint

One directory per session under `~/.agents/state/` — never the OS temp dir (reboots clear it) or the repo (`git status` noise). `STATE.md` beside `log.txt`, `status.txt`, `worktree.patch` taken as the tree stood, so a fresh session given only the project path reaches it and names the next action.

Refresh on every settled decision, and **always before dispatching a long job** — the brief dies with the session that wrote it. Shutdowns are not announced, so a checkpoint written at the end is missing exactly when it is needed. `Updated:` heads the file, `fsync`ed to disk, so a stale one cannot pass for the current one.

## Save

Stop or question every live job (`read proc://`, then `write agent://<id>`) rather than snapshotting a moving tree. In every repo touched, snapshot `git log --oneline -5`, `git status --porcelain`, `git diff HEAD`.

Write `STATE.md`: *Work / Why*, pointing at the plan file rather than restating it · *Locked decisions*, each with the reason the user gave · *In flight*, naming the job, when it was last checked, the files it was writing, that its edits are partial, and **its brief quoted verbatim** · *Proven vs assumed* · *Open questions* · *Next action* · *Credentials*, paths only · *Transcripts*.

Then point this session's line in `INDEX.md` at it and refresh `latest`.

Done when the index reaches `STATE.md`, and `STATE.md` names the next action, the in-flight files and every locked decision.

## Resume

Read the newest `ls -td ~/.agents/state/*/ | head -3`, and `latest`. What they record is settled.

Age it against the tree: an in-flight job is unknown until its own record (`proc://`, `agent://`, `history://`) and its files are read — it may have landed nothing, or been cut mid-edit. Correct the file before doing the work.

Resume with a fresh agent whose brief opens on the partial state just found, never on the original brief.

Done when the next action is underway and no heading describes finished work.
