---
name: audit-seo
description: Audit crawlability, indexation, technical foundations, on-page elements, structured data, content quality, authority signals, and AI answer-engine visibility, with the installed `seo-audit` and `ai-seo` skills supplying the domain detail. Use when the user wants an SEO audit of a site the user owns — or when `audit-loop` selects this branch.
---

# SEO audit

Use this branch when the user selects **SEO audit**. In a mixed run it executes seventh — after `audit-security`, before `audit-code-quality` — because its remediations change served markup and copy, and code quality freezes behavior.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Find what suppresses organic and AI-search visibility: crawl and indexation faults, technical and on-page gaps, schema and content problems, weak authority, and absence from AI answers. `skill://seo-audit` owns classic-search detail, `skill://ai-seo` owns AI answer-engine detail; this branch owns the inventory, the probes, the classification, and the ledger. Both disclose references (`skill://seo-audit/references/…`, `skill://ai-seo/references/…`) — open the one the owning skill names for the question in front of you.

## Rules of engagement

- Audit only the site the user owns or authorized; probe it without mutating anything, and never crawl a third party's site.
- Record the URL, the status code, and the instrument behind every observation — a finding without its instrument is a rumor.
- Probe at a human pace, within the site's own crawl directives.
- Implement only guideline-satisfying remediations; refuse and record a request that needs cloaking, doorway pages, link schemes, or keyword stuffing.

## Inventory phase

1. Take the URL set from `docs/ui-tree.md` when the wiring branch built it; otherwise enumerate routes from the router, sitemap, and rendered navigation. The probe unit is a URL **class** (template + render mode).
2. Record the crawl surface: `robots.txt`, sitemaps, canonicals, `hreflang`, redirect chains, filtered and paginated URLs, `noindex`, and every host or locale variant.
3. Classify the site type (SaaS, e-commerce, content, local) — `skill://seo-audit` weights the checklist per type — and each class's render mode, which picks the probe instrument.

## Probe set

Coverage skeleton; the depth of each item comes from the owning skill.

1. **Crawlability and indexation** — reachability without JavaScript, robots directives, sitemap coverage, canonicals, duplicates, redirect chains, soft 404s, orphans, index bloat.
2. **Technical foundations** — status codes, HTTPS and host consistency, mobile rendering, Core Web Vitals, URL patterns, internationalization.
3. **On-page elements** — titles and descriptions against intent, headings, image alt text, internal links and anchors, breadcrumbs, social cards.
4. **Structured data** — per `skill://seo-audit`'s schema-detection rule; type coverage against page types.
5. **Content quality** — depth against intent, thin or duplicate content, E-E-A-T, freshness, cannibalization.
6. **Authority signals** — internal link distribution, broken outbound links, off-site evidence the user supplies.
7. **AI answer-engine visibility** — the recorded prompt set through `skill://ai-seo`'s visibility measurement.
8. **Metrics baseline** — the analytics or log access the project has, so remediation is measurable later; absent access is `unproven`, naming what would settle it.

Each probe ends as `confirmed defect`, `missing coverage`, `intentional`, `unproven` (with the precondition that would settle it), or `not applicable` (with the reason).

## Proof standards

- Crawlability: what a plain HTTP client receives — status, headers, body, no script execution.
- Rendered content or structured data: the browser DOM, never view-source or a partial fetch.
- AI visibility: a dated observation per platform, with the exact prompt and the quoted answer or its absence — never a standing rank.
- Negatives are recorded too: URL, response, and why the class passes.

## Ledger

`docs/seo-audit-findings.md`, IDs `SEO-001`…: URL class, URL, status, probe, instrument, observation, classification, impact, remediation, re-probe. AI-visibility rows carry platform, prompt, and date.

## Repair rules

- Name the URL class and expected effect before touching markup; re-probe the same class with the same instrument and record the before/after.
- Keep redirects one hop.
- Keep every legitimate `noindex`, authentication wall, and crawl rule in place; visibility is earned inside those boundaries.

## SEO completion criteria

The SEO branch is complete only when:

- Every URL class carries a crawlability and indexation verdict, or an out-of-scope reason.
- Every probe has a classification with its URL, instrument, and observation.
- Every confirmed defect has a fix, a re-probe, and the recorded before/after.
- AI-visibility results are recorded per platform and prompt with the date taken, and unproven entries name what would settle them.
- `docs/audit-progress.md` and `docs/seo-audit-findings.md` contain the complete dated run.
