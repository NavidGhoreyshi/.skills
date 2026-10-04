#!/usr/bin/env python3
"""Surface candidate what-went-wrong turns from an omp session transcript.

Reads both transcript stores — omp sessions (`~/.omp/agent/sessions/**/*.jsonl`,
JSON Lines) and the opencode sqlite store (`~/.local/share/opencode/opencode.db`,
tables `session_v2` + `session_message`) — and prints the turns that most
plausibly record a mistake, a near miss, a self-repair, or a request for a retro.
Judgement is still the caller's: this ranks candidates, it does not decide that a
turn was an incident.

Usage:
  incidents.py                       # newest session transcript
  incidents.py PATH [PATH...]        # explicit .jsonl files
  incidents.py --session ID          # newest transcript whose name contains ID
  incidents.py --day 2026-10-03      # every transcript touched that UTC day
  incidents.py --days 14            # trailing fortnight, both stores
  incidents.py --project rata       # only sessions under a matching directory
  incidents.py --list                # transcripts with timestamps, newest first
  incidents.py ... --kind retro      # only these kinds (retro, correction, repair, error)
  incidents.py ... --min-score 4     # raise the bar; default 3
  incidents.py ... --chars 4000      # per-turn truncation, default 1200
  incidents.py ... --json            # machine-readable output

Exit: 0 if candidates were found, 1 if none, 2 on bad input.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

SESSION_ROOT = os.path.expanduser("~/.omp/agent/sessions")
OPENCODE_DB = os.path.expanduser("~/.local/share/opencode/opencode.db")

# Weights are rough priors, not truth. Raise a pattern's weight when it is a
# near-unambiguous signal of a correction; leave generic ones near zero so they
# only surface in combination with something else.
PATTERNS = {
    "retro": [
        (r"\bwhat (?:went wrong|happened wrong)\b", 6),
        (r"\bnear[- ]mistakes?\b", 6),
        (r"\bpost[- ]?mortem\b|\bretrospective\b|\bretro\b", 5),
        (r"\bwhat would you add to\b", 5),
        (r"\bprevent (?:your|the) (?:near )?mistakes?\b", 6),
        (r"\bwhat mistakes?\b.{0,40}\bhappened\b", 5),
        (r"\bgoing forward\b", 3),
        (r"\bfor next time\b|\bnext time you\b", 3),
        (r"\bdon'?t (?:do|let) (?:that|this) happen again\b", 5),
        (r"\blessons?\b.{0,30}\b(?:learn|extract|file)\b", 4),
        (r"\bwhat went wrong\b", 6),
    ],
    "correction": [
        (r"\bthat(?:'|’)s (?:not|wrong)\b", 5),
        (r"\bnot what i (?:asked|said|meant)\b", 6),
        (r"\byou (?:ignored|missed|assumed|didn'?t|failed to)\b", 4),
        (r"\bi (?:already )?(?:told|said|asked|mentioned)\b", 5),
        (r"\bi meant\b", 4),
        (r"\bwhy (?:did|didn'?t|do|does|are|is|were|was) you\b", 5),
        (r"\byou got (?:it )?wrong\b", 5),
        (r"\bthat(?:'|’)s (?:a )?mistake\b", 5),
        (r"\bstop\b.{0,40}\b(?:doing|changing|editing|touching)\b", 5),
        (r"\b(?:undo|revert|roll ?back)\b", 4),
        (r"\bdon'?t (?:touch|change|edit|delete|commit|push)\b", 5),
        (r"\bwithout (?:asking|checking|reading|being asked)\b", 5),
        (r"\bhow many times\b", 5),
        (r"\byou (?:should|could) have\b", 3),
        (r"\bagain\b", 2),
        (r"\bno\b[,.]", 1),
        (r"\bwrong\b", 3),
        (r"\bmistake\b", 3),
    ],
    "repair": [
        (r"\bmy (?:mistake|error|fault)\b", 5),
        (r"\bi was wrong\b", 6),
        (r"\bi mis(?:read|took|judged|assumed)\b", 5),
        (r"\bcorrection\b", 4),
        (r"\bscrap that\b|\bscratch that\b", 4),
        (r"\bi (?:should|shouldn'?t) have\b", 4),
        (r"\bthat(?:'|’)s (?:not|wasn'?t) what i\b", 5),
        (r"\bgood catch\b", 4),
        (r"\bmy (?:earlier|previous|prior)\b", 3),
        (r"\bactually,? (?:it|i|the)\b", 2),
        (r"\brolled? back\b|\breverted\b", 3),
        (r"\bfixed in place\b|\bself-?correct", 4),
        (r"\bfalse (?:pass|positive|read)\b", 5),
        (r"\bnear miss\b", 6),
    ],
    "error": [
        (r"\bTraceback \(most recent call last\)", 3),
        (r"\bcommand failed\b|\bexited with (?:code|status)\b", 2),
        (r"\bENOENT\b|\bEACCES\b|\bSIGSEGV\b", 2),
        (r"\bsyntaxerror\b|\bparseerror\b", 3),
        (r"\bno such file or directory\b", 2),
    ],
}

COMPILED = {
    kind: [(re.compile(p, re.I), w) for p, w in pats] for kind, pats in PATTERNS.items()
}

# Turns this short are acknowledgements ("ok", "do it", "go ahead"), not evidence.
MIN_CHARS = 24


def iter_records(path):
    """Yield parsed records, skipping the unparsable lines a live session leaves behind."""
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def turn_text(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(
        b.get("text", "")
        for b in content
        if isinstance(b, dict) and b.get("type") == "text" and b.get("text")
    )


def score(text, kind):
    return sum(w for rx, w in COMPILED[kind] if rx.search(text))


def classify(role, text):
    """Map a role plus its text onto (kind, score), or (None, 0) if it is not a lead."""
    if role == "toolResult":
        kinds = ["error"]
    elif role == "user":
        kinds = ["retro", "correction"]
    elif role == "assistant":
        kinds = ["repair"]
    else:
        return None, 0
    best_kind, best_score = None, 0
    for kind in kinds:
        hit = score(text, kind)
        if hit > best_score:
            best_kind, best_score = kind, hit
    return best_kind, best_score


def row_for(kind, score, role, timestamp, text, session):
    return {
        "kind": kind,
        "role": role,
        "timestamp": timestamp,
        "score": score,
        "text": text,
        "session": session,
    }


def collect(path):
    """Return scored candidate turns from one omp transcript."""
    out = []
    for rec in iter_records(path):
        if rec.get("type") != "message":
            continue
        msg = rec.get("message") or {}
        role = msg.get("role")
        text = turn_text(msg.get("content"))
        if not text or len(text) < MIN_CHARS:
            continue
        kind, hit = classify(role, text)
        if not kind:
            continue
        out.append(row_for(kind, hit, role, rec.get("timestamp", ""), text, os.path.basename(path)))
    return out


def collect_opencode(db_path, since, until, project):
    """Return scored candidate turns from the opencode sqlite store.

    opencode keeps history in `session_v2` + `session_message`, not in the
    legacy `session`/`message`/`part` tables, which are near-empty in current
    builds. Role lives in the `type` column; the payload is JSON in `data`, with
    `text` for user turns and a `content` block list for assistant turns.
    """
    if not os.path.isfile(db_path):
        return []
    import sqlite3

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT m.session_id, m.type, m.time_created, m.data, s.directory, s.title"
            " FROM session_message m LEFT JOIN session_v2 s ON s.id = m.session_id"
        ).fetchall()
    except sqlite3.Error as exc:
        print(f"opencode store unreadable ({exc}); continuing with omp transcripts", file=sys.stderr)
        return []
    finally:
        con.close()

    out = []
    for session_id, mtype, created, raw, directory, title in rows:
        if since and created and created < since:
            continue
        if until and created and created >= until:
            continue
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        if mtype in ("user", "assistant"):
            text = data.get("text") if mtype == "user" else opencode_assistant_text(data)
            role = mtype
        elif mtype == "tool":
            text = data.get("text", "")
            role = "toolResult"
        else:
            continue
        if not text or len(text) < MIN_CHARS:
            continue
        if project and project not in (directory or ""):
            continue
        kind, hit = classify(role, text)
        if not kind:
            continue
        stamp = ""
        if created:
            stamp = dt.datetime.fromtimestamp(created / 1000, dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        label = f"opencode:{os.path.basename(directory or 'unknown')}/{session_id}"
        if title:
            label += f" ({title})"
        out.append(row_for(kind, hit, role, stamp, text, label))
    return out


def opencode_assistant_text(data):
    blocks = data.get("content")
    if not isinstance(blocks, list):
        return ""
    return "\n".join(
        b.get("text", "")
        for b in blocks
        if isinstance(b, dict) and b.get("type") == "text" and b.get("text")
    )


def resolve(args):
    if args.paths:
        found = []
        for p in args.paths:
            if os.path.isfile(p):
                found.append(p)
            else:
                hits = glob.glob(os.path.join(SESSION_ROOT, "**", f"*{p}*.jsonl"), recursive=True)
                if not hits:
                    print(f"no transcript matching {p!r}", file=sys.stderr)
                found.extend(hits)
        return sorted(set(found))
    if args.session:
        hits = sorted(
            glob.glob(os.path.join(SESSION_ROOT, "**", f"*{args.session}*.jsonl"), recursive=True),
            key=os.path.getmtime,
        )
        return hits[-1:]
    if args.day:
        start = dt.datetime.fromisoformat(args.day).replace(tzinfo=dt.timezone.utc)
        stop = start + dt.timedelta(days=1)
        out = []
        for path in glob.glob(os.path.join(SESSION_ROOT, "**", "*.jsonl"), recursive=True):
            mtime = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc)
            if start <= mtime < stop:
                out.append(path)
        return sorted(out)
    all_sessions = sorted(
        glob.glob(os.path.join(SESSION_ROOT, "*", "*.jsonl")),
        key=os.path.getmtime,
    )
    return all_sessions[-1:]


def omp_window(args):
    """Return (start, stop) datetimes for the requested window, or (None, None)."""
    if args.day:
        start = dt.datetime.fromisoformat(args.day).replace(tzinfo=dt.timezone.utc)
        return start, start + dt.timedelta(days=1)
    if args.days:
        start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)
        return start, start + dt.timedelta(days=args.days + 1)
    return None, None


def glob_omp(args):
    """Every omp transcript in the requested window, or just the newest one."""
    start, stop = omp_window(args)
    if start is None:
        return sorted(
            glob.glob(os.path.join(SESSION_ROOT, "*", "*.jsonl")), key=os.path.getmtime
        )[-1:]
    out = []
    for path in glob.glob(os.path.join(SESSION_ROOT, "**", "*.jsonl"), recursive=True):
        mtime = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc)
        if start <= mtime < stop:
            out.append(path)
    return sorted(out)


def list_sessions():
    rows = []
    for path in glob.glob(os.path.join(SESSION_ROOT, "*", "*.jsonl"), recursive=True):
        rows.append((os.path.getmtime(path), path))
    for mtime, path in sorted(rows, reverse=True):
        stamp = dt.datetime.fromtimestamp(mtime, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        title = ""
        for rec in iter_records(path):
            if rec.get("type") == "title":
                title = rec.get("title", "")
                break
        size = os.path.getsize(path)
        print(f"{stamp}  {size / 1e6:6.1f}MB  {path}")
        if title:
            print(f"{'':16}  \u2190 {title}")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", help="transcript paths or session id fragments")
    ap.add_argument("--session", help="newest transcript whose name contains this id")
    ap.add_argument("--day", help="UTC day, YYYY-MM-DD, to scan wholesale")
    ap.add_argument(
        "--days",
        type=int,
        help="scan the trailing N days across both stores",
    )
    ap.add_argument(
        "--source",
        default="all",
        choices=["all", "omp", "opencode"],
        help="which transcript stores to read; default both",
    )
    ap.add_argument("--project", help="substring match on the session's working directory")
    ap.add_argument("--list", action="store_true", help="list transcripts and exit")
    ap.add_argument("--min-score", type=int, default=3)
    ap.add_argument("--chars", type=int, default=1200)
    ap.add_argument(
        "--kind",
        action="append",
        choices=sorted(PATTERNS),
        help="restrict to these kinds; repeatable",
    )
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)

    if args.list:
        return list_sessions()

    targets = resolve(args) if (args.paths or args.session) else glob_omp(args)
    if not targets and args.source == "omp":
        print("no transcripts resolved; try --list, --day or --days", file=sys.stderr)
        return 2

    def keep(row):
        if row["score"] < args.min_score:
            return False
        return not args.kind or row["kind"] in args.kind

    rows = []
    if args.source in ("all", "omp"):
        for path in targets:
            rows.extend(row for row in collect(path) if keep(row))
    if args.source in ("all", "opencode"):
        start, stop = omp_window(args)
        since = int(start.timestamp() * 1000) if start else None
        until = int(stop.timestamp() * 1000) if stop else None
        rows.extend(
            row for row in collect_opencode(OPENCODE_DB, since, until, args.project) if keep(row)
        )
    rows.sort(key=lambda r: (r["timestamp"], -r["score"]))

    if args.as_json:
        json.dump(rows, sys.stdout, indent=1)
        print()
        return 0 if rows else 1

    if not rows:
        print(f"no candidates at score >= {args.min_score} in {len(targets)} transcript(s)")
        return 1

    for i, row in enumerate(rows, 1):
        body = row["text"]
        if len(body) > args.chars:
            body = body[: args.chars].rstrip() + f"\n... [{len(row['text']) - args.chars} more chars]"
        print(f"\n{'=' * 78}")
        print(f"#{i} [{row['kind']}] score={row['score']} {row['role']} {row['timestamp']}")
        print(f"session: {row['session']}")
        print("-" * 78)
        print(body)

    by_kind = {}
    for row in rows:
        by_kind[row["kind"]] = by_kind.get(row["kind"], 0) + 1
    print(f"\n{'=' * 78}")
    print(f"{len(rows)} candidate(s): " + ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items())))
    print("Candidates are ranked leads, not verdicts. Confirm each against its tool output before filing a rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))