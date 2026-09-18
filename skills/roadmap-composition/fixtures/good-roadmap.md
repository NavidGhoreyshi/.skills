# Roadmap — taskboard (calibration: a clean composition)

> Every non-skipped slice owns a disjoint `Files:` set, bodies carry the
> interfaces dependencies established, and each slice has a real gate.
> `ompo lint` and `scripts/audit-roadmap.mjs` must both report clean.

## [t1-scaffold] Scaffold the app

Vite + React entry, a glob-based route table, and the base stylesheet. No
feature code.

Work:
1. `src/main.jsx` mounts `App`; `index.html` loads it.
2. `src/app/routes.js` exports a route table built from
   `import.meta.glob("../pages/*.jsx")` — `src/pages/Foo.jsx` maps to `/foo`.
   Later slices add pages by adding files, never by editing this table.
3. `src/App.jsx` renders the matching route or a `data-testid="not-found"` fallback.
4. `src/index.css` defines `--color-accent`, `--color-border`, `--radius-md`,
   `--font-sans`. No other file may define them.
5. `package.json` scripts: `dev`, `build`, `test`.

Acceptance: `bun run build` exits 0. Do not add a component library, state
manager, or router dependency.
Verify: bun run build
Files: src/main.jsx, src/App.jsx, src/app/routes.js, src/index.css, index.html, package.json
Effort: med

## [t2-primitives] Form primitives

Depends: t1-scaffold

1. `src/components/ui/Button.jsx`: `{ variant: "primary" | "ghost", size: "sm" | "md", disabled }`,
   renders `<button data-testid="button" data-variant={variant}>`; uses t1's
   `--color-accent` / `--radius-md`.
2. `src/components/ui/Field.jsx`: `{ label, error, children }`; visible label,
   `aria-invalid` + `role="alert"` on error, `data-testid="field"`.
3. `src/styles/forms.css` imported by both: 36px controls, focus ring from `--color-accent`.
4. `src/components/ui/primitives.test.jsx`: variant attribute renders;
   `aria-invalid` wires when `error` is set.

Acceptance: `bun test src/components/ui/primitives.test.jsx` exits 0; no inline
hex colors in `src/components/ui/`.
Verify: bun test src/components/ui/primitives.test.jsx
Files: src/components/ui/Button.jsx, src/components/ui/Field.jsx, src/styles/forms.css, src/components/ui/primitives.test.jsx
Effort: med

## [t3-task-store] Task store

Depends: t1-scaffold

1. `src/store/tasks.js`: `createTaskStore()` → `{ list(), add({ title }), toggle(id), subscribe(fn) }`;
   ids from `crypto.randomUUID()`; persists to `localStorage` key `taskboard.tasks`.
2. `src/store/tasks.test.js`: add → list round-trip, toggle flips `done`, state
   survives a fresh store against the same storage.

Acceptance: `bun test src/store/tasks.test.js` exits 0.
Verify: bun test src/store/tasks.test.js
Files: src/store/tasks.js, src/store/tasks.test.js
Effort: med

## [t4-task-page] Task page

Depends: t2-primitives, t3-task-store

1. `src/pages/TasksPage.jsx` (auto-routed by t1's glob table): a `Field` for the
   title, a `Button variant="primary"` to add, one row per task
   (`data-testid="task-row"`), toggle `Button variant="ghost"` with
   `data-testid="task-toggle"` and `aria-pressed`.
2. Subscribe to the t3 store in a `useEffect`; never reimplement store logic or
   keep a second copy of the list.
3. `src/pages/TasksPage.test.jsx`: adding renders a row; toggling sets
   `aria-pressed="true"`.

Acceptance: `bun test src/pages/TasksPage.test.jsx` exits 0. Do not edit
`src/app/routes.js` — the glob table already routes this file.
Verify: bun test src/pages/TasksPage.test.jsx
Files: src/pages/TasksPage.jsx, src/pages/TasksPage.test.jsx
Effort: med

## [t5-legacy-shim] Remove the legacy shim (parked)

Delete `src/legacy/` and its import once the new pages have shipped a release.
Skip: true
Effort: lo
