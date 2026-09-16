---
name: deep-research
description: Research anything on the internet with platform breadth and extraction depth. MUST USE when the user says research, search, look up, investigate, find out, survey, compare options, what people think/say, or shares a URL to read/summarize/monitor — including Twitter/X, Reddit, YouTube, GitHub, Bilibili, Xiaohongshu, V2EX, Facebook, Instagram, LinkedIn/jobs, RSS, stocks, or any webpage, especially WAF-blocked or JS-heavy pages where plain fetch fails.
---

# Deep Research

Three tools, in order. Stop at the first one that yields content.

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

## 2. Depth — scrapling (extract any URL)

Escalate `get` → `fetch` → `stealthy-fetch`. ALWAYS pass `--ai-targeted`,
prefer `.md` output to /tmp, narrow with `-s "<css>"`, delete temp files after reading.

```bash
scrapling extract get "<URL>" /tmp/x.md --ai-targeted -s "article"
scrapling extract fetch "<URL>" /tmp/x.md --ai-targeted --network-idle --wait-selector ".content"
scrapling extract stealthy-fetch "<URL>" /tmp/x.md --ai-targeted --solve-cloudflare
```

## 3. Last resort — patchright-enhanced (WAF / login / interaction)

Only when step 2 `stealthy-fetch` fails (Cloudflare/Kasada/DataDome, login wall,
multi-step interaction). Stealth comes from patchright itself — no spoofing code.

```bash
cd ~/patchright-enhanced && npm run build && npm start   # opens clean Chrome, stays until closed
```

Point it at the URL via `START_PAGE_URL` in `.env`; drive via its session runner.

## 4. Report

Primary sources only (docs, code, specs — not write-ups of them). Every claim
cited with its URL. Lead with the answer, then evidence. Scratch in `/tmp/`;
persist a findings file only if the repo has a convention for one.
