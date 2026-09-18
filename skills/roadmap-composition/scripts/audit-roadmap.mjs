#!/usr/bin/env node
/**
 * audit-roadmap.mjs — composition-shape linter for ompo ROADMAP.md files.
 *
 * Complementary to `ompo lint` (which owns gate hygiene): checks overlap
 * (unordered → finding, ordered → note), missing `Files:`, read surface over
 * ~2000 lines, sweep-shaped bodies without a bounded `Files:` list, and prints
 * a file summary. Relative `Files:` resolve against the roadmap's directory;
 * missing/glob paths are reported, not counted.
 *
 * Usage:  node audit-roadmap.mjs <ROADMAP.md> [--strict]
 * Exit:   0 normally (findings are advisory), 1 with --strict on findings,
 *         1 on a parse failure (defer to `ompo lint` for the reason).
 *
 * Plain Node, no dependencies, deterministic, no ompo imports.
 */

import { readFileSync, statSync } from "node:fs";
import { dirname, isAbsolute, join, resolve } from "node:path";

const READ_SURFACE_LINES = 2000;
const TOP_REPEATED = 5;

const SWEEP_RE =
  /\b(audit|walk (?:every|all)|every page|all pages|sweep|verify[- ]existing|across (?:the )?(?:app|site|codebase|pages))\b/i;
const GLOB_RE = /[*?[\]{}]/;
const TRAILER_RE = /^(depends|files|effort|verify|skip)\s*:\s*(.*)$/i;
const HEADING_RE = /^##\s+(.*)$/;
const EXPLICIT_ID_RE = /^\[([A-Za-z0-9][A-Za-z0-9._-]*)\]\s*(.*)$/;

function slugify(title) {
  const slug = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
  return slug || "slice";
}

/** Split on `## ` headings exactly as src/parse.ts does (fences never hide one). */
function splitSections(markdown) {
  const sections = [];
  let current = null;
  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    const h = line.match(HEADING_RE);
    if (h && !line.startsWith("###")) {
      current = { heading: h[1].trim(), lines: [] };
      sections.push(current);
    } else if (current) {
      current.lines.push(line);
    }
  }
  return sections;
}

function parseRoadmap(markdown) {
  const slices = [];
  const seen = new Set();
  for (const sec of splitSections(markdown)) {
    const m = sec.heading.match(EXPLICIT_ID_RE);
    const id = m ? m[1] : slugify(sec.heading);
    if (seen.has(id)) throw new Error(`duplicate slice id "${id}"`);
    seen.add(id);
    const slice = { id, title: m ? (m[2] || id).trim() || id : sec.heading, deps: [], files: [], skip: false, body: [] };
    let inFence = false;
    for (const line of sec.lines) {
      if (/^\s*```/.test(line)) inFence = !inFence;
      const t = !inFence ? line.match(TRAILER_RE) : null;
      if (!t) {
        slice.body.push(line);
        continue;
      }
      const key = t[1].toLowerCase();
      const value = t[2] ?? "";
      if (key === "depends") slice.deps = value.split(/[,\s]+/).map((s) => s.trim()).filter(Boolean);
      else if (key === "files") slice.files = value.split(/[,\s]+/).map((s) => s.trim()).filter(Boolean);
      else if (key === "skip") slice.skip = /^(true|yes|1|skip)$/i.test(value.trim());
    }
    slice.body = slice.body.join("\n").trim();
    slices.push(slice);
  }
  return slices;
}

function main(argv) {
  const args = argv.filter((a) => a !== "--strict");
  const strict = argv.includes("--strict");
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log("usage: node audit-roadmap.mjs <ROADMAP.md> [--strict]");
    return args.length === 0 ? 1 : 0;
  }
  const roadmapPath = args[0];
  let text;
  try {
    text = readFileSync(roadmapPath, "utf8");
  } catch (err) {
    console.error(`roadmap-audit: cannot read ${roadmapPath}: ${err.message}`);
    return 1;
  }

  let slices;
  try {
    slices = parseRoadmap(text);
  } catch (err) {
    console.error(`roadmap-audit: cannot parse ${roadmapPath}: ${err.message}`);
    console.error(`roadmap-audit: run \`ompo lint --roadmap ${roadmapPath}\` for the parser's verdict, fix that first`);
    return 1;
  }
  if (slices.length === 0) {
    console.error(`roadmap-audit: no \`## \` slices found in ${roadmapPath}`);
    console.error(`roadmap-audit: run \`ompo lint --roadmap ${roadmapPath}\` for the parser's verdict, fix that first`);
    return 1;
  }

  const active = slices.filter((s) => !s.skip);
  const byId = new Map(slices.map((s) => [s.id, s]));
  const reaches = (from, to, seen = new Set()) => {
    if (from === to) return true;
    if (seen.has(from)) return false;
    seen.add(from);
    const s = byId.get(from);
    return s ? s.deps.some((d) => byId.has(d) && reaches(d, to, seen)) : false;
  };

  const findings = [];
  const notes = [];

  // 1. Overlap: one writer per file (R1/R9).
  const owners = new Map();
  for (const s of active) {
    for (const f of s.files) {
      if (!owners.has(f)) owners.set(f, []);
      owners.get(f).push(s.id);
    }
  }
  for (const [file, ids] of owners) {
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const [a, b] = [ids[i], ids[j]];
        const aToB = reaches(a, b);
        const ordered = aToB || reaches(b, a);
        if (ordered) {
          // `a reaches b` means a depends on b, so b runs first.
          const [from, to] = aToB ? [b, a] : [a, b];
          notes.push(`[overlap-ordered] ${file} — ${from} → ${to} (ordered; the later body must state what it inherits)`);
        } else {
          findings.push(`[overlap] ${file} — ${a} & ${b} share it with no dependency path between them`);
        }
      }
    }
  }

  // 2 + 3. Scope: every non-skip slice declares Files; its surface fits.
  const base = dirname(resolve(roadmapPath));
  for (const s of active) {
    if (s.files.length === 0) {
      findings.push(`[missing-files] ${s.id} — no Files: trailer (unbounded read scope; the worker discovers paths itself)`);
    }
    let lines = 0;
    const unresolved = [];
    for (const f of s.files) {
      if (GLOB_RE.test(f) || isAbsolute(f)) {
        unresolved.push(f);
        continue;
      }
      try {
        const abs = join(base, f);
        if (!statSync(abs).isFile()) throw new Error("not a file");
        lines += readFileSync(abs, "utf8").split("\n").length;
      } catch {
        unresolved.push(f);
      }
    }
    s.lines = lines;
    s.unresolved = unresolved;
    if (lines > READ_SURFACE_LINES) {
      findings.push(`[read-surface] ${s.id} — ~${lines} lines across Files: (threshold ${READ_SURFACE_LINES}); split by file cluster or script it`);
    }
  }

  // 4. Sweep smell: unbounded body scope pretending to be a slice (R3).
  for (const s of active) {
    const unbounded = s.files.length === 0 || s.files.every((f) => GLOB_RE.test(f));
    if (unbounded && SWEEP_RE.test(s.body)) {
      const why = s.files.length === 0 ? "no Files: trailer" : "only glob Files:";
      findings.push(`[sweep-smell] ${s.id} — sweep-shaped body with ${why} (write a codemod against a committed manifest instead)`);
    }
  }

  // 5. Summary.
  const refs = active.flatMap((s) => s.files);
  const distinct = new Set(refs);
  const counts = new Map();
  for (const f of refs) counts.set(f, (counts.get(f) ?? 0) + 1);
  const repeated = [...counts.entries()]
    .filter(([, n]) => n > 1)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, TOP_REPEATED);

  const w = Math.max(12, ...slices.map((s) => s.id.length));
  console.log(`roadmap-audit: ${roadmapPath}`);
  console.log(`base: ${base}`);
  console.log(`slices: ${slices.length} (${slices.length - active.length} skipped) · files: ${distinct.size} distinct, ${refs.length} refs`);
  console.log("");
  console.log("read surface (non-skipped slices):");
  for (const s of active) {
    const missing = s.unresolved.length > 0 ? `  (${s.unresolved.length} unresolved)` : "";
    console.log(`  ${s.id.padEnd(w)}  files=${s.files.length}  lines=${s.lines}${missing}`);
  }
  console.log("");
  if (findings.length === 0) {
    console.log("findings: none");
  } else {
    console.log(`findings (${findings.length}):`);
    for (const f of findings) console.log(`  warn ${f}`);
  }
  for (const n of notes) console.log(`  note ${n}`);
  const top = repeated.length > 0 ? repeated.map(([f, n]) => `${f} (${n})`).join(", ") : "none";
  console.log("");
  console.log(`totals: ${findings.length} finding(s), ${notes.length} note(s) · top repeated: ${top}`);
  return strict && findings.length > 0 ? 1 : 0;
}

process.exit(main(process.argv.slice(2)));
