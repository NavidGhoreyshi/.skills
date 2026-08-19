---
name: context-pack
description: Package the source files relevant to a prompt into a portable context pack for another LLM. Use when the user wants to hand off a question, feature, or bug to another model with full file context, without solving the request.
---

# Context Pack

Prepare context only. Never solve the request.

## Workflow

1. Read the prompt. **Scope the change first**:
   - **Contained** — one component, file, or element (replace an element, tweak styles, fix one component). Include only the files being directly modified; reference swapped-in assets by path only. Stop — no following imports or parents.
   - **Broad** — a feature change, refactor, or new feature touching multiple layers (auth flow, new page, data-model change). Include the primary files, then follow imports, references, dependencies, routing, shared utilities, schemas, types, configs, middleware, services, stores, hooks, and contexts until nothing relevant remains.
2. Read the selected files completely.
3. Generate, in the project root: `context_manifest.txt`, `context_01.txt`, `context_02.txt`, … Overwrite any previous exports — never append.
4. Stop. Report stats only. Do not answer the prompt.

## Context file format (XML)

```xml
<context version="1">

<prompt>
<![CDATA[{{USER_PROMPT}}]]>
</prompt>

<project_root>
<![CDATA[{{ABSOLUTE_PROJECT_ROOT}}]]>
</project_root>

<part index="1" total="N"/>

<files>

<file
    path="app/page.tsx"
    language="tsx">

<![CDATA[
...exact file contents...
]]>

</file>

</files>

</context>
```

Each context file carries the prompt, project root, part number, and the files it contains.

## Output rules

- **Complete files, verbatim.** Never summarize, truncate, abbreviate, omit sections, rewrite formatting, normalize whitespace, strip comments, or change line endings. Preserve the file exactly as on disk. UTF-8.
- **Media / binary** (SVG, PNG, JPG, GIF, WEBP, ICO, fonts, PDF, video, audio, binaries): no contents in context files. Path in the manifest + path-only reference in the XML: `<file path="public/logo.svg" media="true" size="3954 bytes" />`.
- **Splitting.** When output nears the model limit: finish the current source file, start the next context file. Never split one source file across context files. Name sequentially: `context_01.txt`, `context_02.txt`, …

## Manifest

`context_manifest.txt`: header, generated timestamp, prompt, project root, generated context files, statistics (source files included, media referenced, context files, total size), included source files, referenced media files, excluded categories.

## Ignore

Never include: `node_modules/`, `.next/`, `dist/`, `build/`, `coverage/`, `.cache/`, `.git/`, `.vercel/`, `out/`, `tmp/`; `*.lock`, `*.log`; media (`*.png *.jpg *.jpeg *.gif *.bmp *.webp *.ico *.svg`); video/audio (`*.mp4 *.avi *.mov *.mkv`); archives (`*.zip *.rar *.7z *.tar *.gz`); `*.pdf`; fonts (`*.woff *.woff2 *.ttf`); binaries (`*.exe *.dll *.so`).

If the request specifically concerns one of these, reference its path in the manifest + XML — never its raw contents.

## File selection

Scope first (see Workflow step 2). Within the scoped boundary, prefer slightly more context over omitting something useful. Always include when relevant: pages, routes, components, layouts, hooks, context providers, stores, API routes, services, utilities, types, interfaces, schemas, validation, database/ORM models, middleware, config files, env examples, directly related tests, shared libraries. Only files that help understand or modify the requested feature; avoid unrelated areas.

## Ordering

Most-important files first — core feature files before supporting utilities — so a receiver gains useful context even from the first file alone.

## Completion

Report only: source files exported, media files referenced (path only), context files generated, total size, location of the generated files. Do not answer the user's original request.
