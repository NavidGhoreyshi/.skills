---
name: deep-research
description: Research anything on the internet with platform breadth and extraction depth. MUST USE when the user says research, search, look up, investigate, find out, survey, compare options, what people think/say, or shares a URL to read/summarize/monitor — including Twitter/X, Reddit, YouTube, GitHub, Bilibili, Xiaohongshu, V2EX, Facebook, Instagram, LinkedIn/jobs, RSS, stocks, or any webpage, especially WAF-blocked or JS-heavy pages where plain fetch fails.
---

# Deep Research

Run all three lanes on every task, then compare outputs and keep the best evidence per claim. NEVER stop at the first lane that yields content.

## 0. Setup (once per machine, skip if present)

```bash
which agent-reach || pip install git+https://github.com/Panniantong/Agent-Reach
which scrapling || pip install "scrapling[all]" && scrapling install --force
# patchright-enhanced: clone once to ~/patchright-enhanced, then:
# npm install && npx patchright install chrome
```

## 1. Breadth — agent-reach (platforms + search)

Login-state platforms first: `agent-reach doctor --json`, follow its
`active_backend`. State which backend you use. Parallelize multi-platform sweeps.

```bash
mcporter call exa.web_search_exa query="<q>" numResults=5   # web search
curl -s "https://r.jina.ai/<URL>"                           # plain article
gh search repos "<q>" --sort stars --limit 10               # github
yt-dlp --write-sub --write-auto-sub --skip-download "URL"   # youtube subs
bili search "<q>" --type video -n 5                         # bilibili
twitter search "<q>" -n 10                                  # needs TWITTER_AUTH_TOKEN + TWITTER_CT0 in env
opencli reddit search "<q>" -f yaml                         # or: rdt search "<q>"
opencli xiaohongshu search "<q>" -f yaml                    # desktop, existing Chrome session only
```

Never log in as the user, never read/inject browser cookies yourself.
Query every platform relevant to the question, not just one. Parallelize multi-platform sweeps. Log which backend you used and what each platform returned or missed.

## 2. Depth — scrapling (extract any URL)

Escalate `get` → `fetch` → `stealthy-fetch`. ALWAYS pass `--ai-targeted`,
prefer `.md` output to /tmp, narrow with `-s "<css>"`, delete temp files after reading.
Run this lane even when breadth returned snippets — snippets are leads, not evidence. Extract the top candidate URLs. Log which level (`get` / `fetch` / `stealthy-fetch`) succeeded per URL.

```bash
scrapling extract get "<URL>" /tmp/x.md --ai-targeted -s "article"
scrapling extract fetch "<URL>" /tmp/x.md --ai-targeted --network-idle --wait-selector ".content"
scrapling extract stealthy-fetch "<URL>" /tmp/x.md --ai-targeted --solve-cloudflare
```

## 3. Verify — patchright-enhanced (interaction / JS-heavy / WAF check)

Always run on the top 1-2 URLs, even when scrapling succeeded: verify JS-heavy content, WAF-blocked pages, or multi-step interaction, and cross-check the scrapling extract against the live rendered page. Stealth comes from patchright itself — no spoofing code. Scope to 1-2 URLs, never a full re-sweep: breadth and depth do the sweeping, this lane verifies. If no URL exists to drive (pure API aggregation with nothing to render), log a one-line skip reason instead of running.

```bash
cd ~/patchright-enhanced && npm run build && npm start   # opens clean Chrome, stays until closed
```

Point it at the URL via `START_PAGE_URL` in `.env`; drive via its session runner.

## 4. Compare and select (mandatory)

Compare the three lanes per key claim and keep the best evidence; never default to the first result. Prefer primary sources (docs, code, specs, the posts themselves) over write-ups; direct observation over quoted numbers; complete extracts over snippets; newer over older for changing data. On conflict prefer the lane showing the raw source and name the disagreement explicitly. Log per key claim which lane won and with which URL.

## 5. Report

Primary sources only (docs, code, specs — not write-ups of them). Every claim
cited with its URL. Lead with the answer, then evidence. State which backends and lanes ran and which lane won each key claim. Scratch in `/tmp/` and delete temp files after reading;
persist a findings file only if the repo has a convention for one.
