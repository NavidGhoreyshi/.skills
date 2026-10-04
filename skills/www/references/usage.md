# Using `scripts/incidents.py`

The scanner is a lead generator. It ranks turns by how strongly they match the
shape of a correction, a self-repair, a tool error, or an explicit request for a
retro. It does not know which of those were real, and it will not find a mistake
nobody wrote down.

Zero dependencies, python3 only.

## Transcript stores

Both hold history; neither is complete alone. `--source` picks; `all` is default.

**omp** — one JSONL per session:

```
~/.omp/agent/sessions/<project-slug>/<session-id>.jsonl
```

Sibling directories hold per-tool output (`*.bash.log`, `*.read.log`). A
`*.bash-original.log` next to a `*.bash.log` means that command was re-run after
being corrected — a cheap signal that a tool call was repaired in flight.

Record shape, if you parse these yourself:

```json
{"type":"message","message":{"role":"user","content":[{"type":"text","text":"..."}]}}
```

The role and content sit under the **nested** `message` key; a naive
`record["role"]` returns `None` on every line. Assistant records also carry
`toolCall` blocks — ignore those when reading prose.

**opencode** — sqlite, and the table choice matters:

```sh
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT m.type, m.data FROM session_message m LIMIT 5"
```

History lives in `session_v2` (id, directory, title, times) and `session_message`
(session_id, type, time_created, data). The legacy `session`, `message` and
`part` tables are near-empty in current builds — querying `session` returns one
row and will convince you the history is gone. It is not. Role is the `type`
column (`user`, `assistant`, `tool`, `idle`); the payload is JSON in `data`, with
`text` for user turns and a `content` block list for assistant turns whose blocks
are `text`, `reasoning` or `tool`. Timestamps are ms epoch in `data.time.created`.

## Commands

```sh
scripts/incidents.py --list                    # omp transcripts, newest first
scripts/incidents.py                           # newest omp session
scripts/incidents.py --session 01a0f7ed        # newest matching id fragment
scripts/incidents.py --day 2026-10-03          # one UTC day, both stores
scripts/incidents.py --days 14 --project rata  # trailing fortnight, one project
scripts/incidents.py --source opencode         # opencode store only
scripts/incidents.py --kind retro --kind correction
scripts/incidents.py --min-score 6 --chars 400 # raise the bar, less text
scripts/incidents.py --json > leads.json
```

Exit codes: `0` candidates found, `1` none, `2` bad input. A missing or
unreadable opencode store prints a warning and continues with omp; a missing omp
root plus `--source opencode` is still a valid run.

Roughly 40 seconds for a 14-day window across both stores, returning a few
hundred leads at the default threshold.

## Reading the output

Each block is one turn: kind, score, role, timestamp, transcript name, text.

| Kind | Means | Usually becomes |
|---|---|---|
| `retro` | the user explicitly asked what went wrong | the whole session's lesson set |
| `correction` | the user pushed back | a rule about the specific mistake |
| `repair` | the agent admitted an error | a rule about the failure shape |
| `error` | a tool result carrying an error signature | context for the turn above it |

Four calibration notes, learned from the first two real runs:

- `retro` is unambiguous and rare. When it fires it is the highest-value turn in the session and it should anchor the report.
- `error` is mostly noise alone — a failed `grep` teaches nothing. An error only matters next to the correction or repair it caused. Read it with its neighbours.
- **Long turns accumulate score.** Weights sum across patterns, so a 2000-word prompt matching six weak phrasings outranks a short, precise correction. Read the text, not the number.
- Subagent transcripts are included and often the most honest source, because a scout has no stake in how the parent's work was reported.

## What the scanner cannot see

- Mistakes the agent never acknowledged and nobody corrected.
- State that leaked between calls — a stale cookie, a cached fixture, an env var — where every turn reads clean.
- Tests that passed for the wrong reason. Those surface only when a human reads the assertion closely.
- Sessions predating a store's current layout.

When the leads come back thin, read the session's own end-of-task reports instead:
agents list what they fixed far more often than what they got wrong twice.
