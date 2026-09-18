# Roadmap — dashboard redesign (calibration: the wedge shape)

> Reproduces the composition failures of run `20260916-va5e9b`: unordered file
> overlap, an unbounded sweep with no manifest, and slices with no `Files:`
> list — while still passing `ompo lint` (gate hygiene is fine, composition is
> not). `scripts/audit-roadmap.mjs` must flag every shape below.

## [b1-tokens] Design tokens

Replace `src/index.css` with the token set; restyle `Button.jsx` to consume it.
Verify: npm run build
Files: src/index.css, src/components/ui/Button.jsx
Effort: med

## [b2-shell] Application shell

Flat sidebar, one system top bar, new content frame — adjusting the tokens in
`src/index.css` where the shell needs new surfaces.
Verify: npm run build
Files: src/index.css, src/pages/TopDataBar.jsx, src/layout/MainLayout.jsx
Effort: med

## [b3-dialogs] Dialog shell

Depends: b1-tokens

Restyle the shared modal shell and the camera dialog on the new primitives.
Verify: npm run build
Files: src/components/ui/Modal.jsx, src/components/ui/Button.jsx, src/components/CameraModal.jsx
Effort: med

## [b4-members] Members workspace

Rebuild the members page around the new dialog shell.
Verify: npm run build
Files: src/components/ui/Modal.jsx, src/pages/MembersPage.jsx
Effort: hi

## [b5-language] Language and digits sweep

Walk every page and convert hard-coded digits to the Persian converter, then
check all pages for missing `dir="rtl"` attributes and fix what is wrong.
Verify: npm run build
Effort: med

## [b6-responsive] Responsive pass

Review all pages at 390 / 768 / 1280 and fix overflow and cramped controls
wherever they show up.
Verify: npm run build
Effort: med
