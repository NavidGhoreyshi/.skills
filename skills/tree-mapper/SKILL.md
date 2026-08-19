---
name: tree-mapper
description: Build or refresh a project's frontend and backend integration tree for audit work. Use when an audit needs routes or SPA views, components, API wiring, backend endpoints, data dependencies, permissions, external integrations, or test coverage mapped before repair.
---

# Tree Mapper

Create or refresh `docs/ui-tree.md`. Do not modify application code, commit, or deploy.

Map stable work-unit IDs for server or SPA routes, views and flows; frontend pages, layouts, components, forms, state, API clients, loading and error states; backend routes, actions, validation, policies, services, models, migrations, jobs, storage, and response shapes; external APIs, environment variables, feature flags; dead or placeholder UI; and unit, feature, integration, and Playwright headless Chromium tests.

For SPAs, group by meaningful user-facing view or flow. Link each unit to files and dependencies. Mark uncertainty instead of guessing. When refreshing an existing tree, preserve stable IDs and audit history, add new nodes, and mark removed or moved nodes without silently deleting them.

For each unit, record a wiring inventory: every interactive control (button, link, toggle, form, filter, upload, rating, search) and every data-bearing element (list, card, KPI, chart, image, date, label) mapped to its backend endpoint and method, or marked `static` / `hardcoded` / `mock` / `dead` / `unknown`. A unit without this inventory is not audit-ready.

Report the path, work-unit count, changed sections, assumptions, unresolved mappings, and recommended next unit. Do not run deployment commands.
