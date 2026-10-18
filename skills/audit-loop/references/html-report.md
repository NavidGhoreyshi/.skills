# HTML report

Generic spec for any branch HTML report. Branch references add only their own sections, filenames, and data sources — never restate these rules.

## Document shell

- **One file.** `<!DOCTYPE html>`, `<head>` with charset, title, and one `<style>` block, `<body>` with header, sections, footer, and one small `<script>` for foldable details or filters.
- **Header.** Report title, project, run ID, deployed revision, live URL, scope counts, generated timestamp.
- **Footer.** Generator credit and a back-to-top link.

## Section order

1. Executive summary (funnel, verdict counts, or equivalent top-down view).
2. Breakdowns (per-group heatmaps, checklists, or tables).
3. Defect ledger (every finding with severity, status, and evidence link).
4. Measurements or inventory tables backing the verdicts.
5. Footer.

Branches keep this order and slot their own sections into it.

## Severity table

| Badge | Meaning | Color |
|---|---|---|
| `ok` | pass / in place | green |
| `warn` | partial / at risk | amber |
| `fail` | fail / missing | red |

- **Text plus color.** Never encode a verdict by color alone — every badge carries text.
- **Color-blind-safe palette.** Passes a grayscale check; `ok`/`warn`/`fail` stay distinguishable without hue.
- **Dark-first.** CSS custom properties with a `prefers-color-scheme: light` override.

## Evidence links

- **Per-finding anchors.** Each finding has an `id`, a one-line summary, and a `<details>` block with reproduction, observed vs expected, and probe output.
- **Linkable.** Section `id`s and finding `id`s so the ledger and the report cross-reference.

## Inline CSS

- **All CSS inlined.** Custom properties, responsive grid, print stylesheet. No external stylesheets.
- **No external assets.** No CDN, no remote images or fonts — inline SVG for icons and checkmarks.

## Offline single-file constraint

- **Opens from disk.** The report works opened directly in a browser with no server and no network — one `.html` file, zero dependencies.

## Where it is written

- **Beside the ledger.** Next to the branch state file and findings ledger, under the filenames the branch reference names.

## How it is generated

- **Read, never re-run.** Populate from the branch state file and findings ledger after the chunk lands — do not re-run flows to build the report.
- **Commit or artifact.** Commit alongside the chunk's changes when the user wants history, otherwise offer as an artifact.

*Done when the report opens offline as one file, every finding links to its evidence, and every verdict carries text plus color.*
