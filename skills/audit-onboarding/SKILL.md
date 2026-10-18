---
name: audit-onboarding
description: Drive the deployed application through the new-user journey from first touch through first meaningful use, measuring time-to-value, drop-off, cognitive load, trust signals, and the promise-to-delivery gap. Use when the user wants an onboarding audit of the live signup-to-value path, in reviewed chunks — or when `audit-loop` selects this branch.
---

# Onboarding audit

Use this branch when the user selects **Onboarding audit**. It runs second (after `audit-live-flow`) because it narrows the live ground truth to the new-user journey specifically.

> Shared protocol — fix-mode repair contract, finding-ledger convention, order-of-effects assertion, repo-not-host fix statuses (`verified live` / `fixed, awaiting live verification`), and unproven/host-side confirmation — is stated once in `audit-loop`.

## Goal

Drive the application **as deployed** through the *new-user journey* from first touch (landing page, marketing, SEO entry points) through signup, verification, first login, first configuration, to first meaningful value moment (first booking made, first booking received, first payment, first dashboard insight). Measure:

- **Time-to-value** — wall-clock and step count from landing to first value.
- **Drop-off points** — where users stall, abandon, or need external help.
- **Cognitive load** — decisions required, fields filled, concepts explained vs assumed.
- **Trust signals** — security, social proof, guarantees visible at each step.
- **Promise-to-delivery gap** — what marketing/landing promises vs what the product actually delivers in the first session.

Executed in reviewed chunks, with the same browser+host pairing as `audit-live-flow`.

## Relationship to `audit-live-flow`

- Uses the same live surface, host access, identities, recipes, and data-safety contract established in `audit-live-flow` preflight.
- The onboarding flow inventory is a **subset** of the `audit-live-flow` inventory (the new-user entry path + first-value flows).
- Findings from `audit-live-flow` that affect onboarding (broken signup, broken email verification, broken first login) are imported as known constraints; they are not re-probed.
- This skill adds *onboarding-specific* measurements and lenses that `audit-live-flow` does not: step timers, hesitation points, copy clarity, empty-state quality for brand-new accounts, default/empty configurations, and the "what now?" moment after first value.

## Preflight (re-uses `audit-live-flow` preflight; add only)

1. **Onboarding entry points** — the exact URLs a brand-new user might land on (apex, `/`, `/landing`, campaign URLs, locale variants, referral links). Confirm each serves the expected build.
2. **Audit accounts** — fresh accounts created *for this run* (never real users). Use the reserved test range or a domain the user controls. **Never trigger a real outbound message** (SMS, email, push) to prove one works — mint server-side, seed verified state, stub outbound delivery. If the product requires a live OTP/SMS to proceed, the audit either (a) uses a seeded test phone with a known code, or (b) records `unproven` for that gate and proceeds with a pre-verified account.
3. **First-value definition** — agree with the user on what "first meaningful use" means for each role: customer (first booking confirmed), business owner (first booking received), employee (first shift seen), admin (first tenant configured). Record it in the state file.
4. **Persona scripts** — 2–4 representative new-user personas with different entry paths and goals (e.g., "mobile customer from Instagram ad", "desktop owner from search", "referred customer with invite link"). Each script names the entry URL, the expected steps, and the first-value target.

## Flow inventory (onboarding-specific)

Build a focused inventory **before** testing, derived from the `audit-live-flow` inventory plus marketing/landing routes. Give each flow a stable ID (`ONB-F01`, …) and record:

- **Persona and entry point** — which persona, which URL, which campaign/referrer if any.
- **Preconditions** — brand-new account (no prior data), or specific seeded state (invite token, referral code).
- **Steps** — the interaction sequence, in order, including all decisions and inputs.
- **Time budget** — expected max minutes/steps for a motivated user (from user research or heuristic).
- **Expected result** — including the *order* of effects (same standard as `audit-live-flow`): UI acknowledgement → API success → DB write → job enqueued → job processed → cache invalidated → next page reflects it.
- **Server-side assertion** — what must be visible on the host afterwards.
- **Drop-off risk** — which step is most likely to lose the user (heuristic or data-backed).
- **Cleanup** — none, or exact reversal (delete audit account, purge audit bookings).
- **Verdict** — `pass` / `fail` / `partial` / `blocked` / `unproven` / `not applicable`.
- **Measurements captured** — actual time, actual steps, hesitations (pauses >10s on a field), errors, help clicks, back-button uses.

Order: anonymous landing → signup/verification → first login → first config/wizard → first value → "what now" screen.

## Chunking

Same rules as `audit-live-flow`: chunks are coherent slices (e.g., "landing → verified account", "first login → first booking"), each fits one context window, dependent flows stay together, go sign per chunk, re-ask deployment authority before any fix that deploys.

### State file

`docs/onboarding-audit.md` (new file, same pattern as `live-flow-audit.md`):

```markdown
# Onboarding Audit

- Run ID / started / last updated:
- Live URL(s):            https://app.example.com  (apex/www/locale/campaign variants)
- SSH host:               user@host   (topology: <what runs where>)
- Deployed revision:      <sha>   (local tree: <branch @ sha, dirty?>)
- Browser harness / viewport:
- Fix mode:               manual | automatic  (chunked, go sign per chunk)
- Deployment authority:   push+deploy allowed? YES/NO  (re-asked every run and chunk)
- Baseline health:        services up / public pages load / log state

## Identities (audit accounts, pre-seeded)
| Role | Account | Authenticates live via | Data owned | Flows allowed |
|---|---|---|---|---|

## First-value definitions
| Role | First-value moment | Success criteria |
|---|---|---|

## Persona scripts
| Persona | Entry URL | Expected steps | First-value target | Time budget |
|---|---|---|---|---|

## Data-safety contract
- Read-only: ...
- Creates data: ... (cleanup: ...)
- Forbidden without explicit approval: ...

## Server-side recipes (validated)
- containers: <cmd>   - logs: <cmd>   - db: <cmd>   - queue/cache/migrations: <cmd>

## Onboarding flow inventory
| ID | Flow | Persona | Entry | Preconditions | Expected (incl. ordering) | Server assertion | Drop-off risk | Cleanup | Verdict | Chunk |
|---|---|---|---|---|---|---|---|---|---|---|

## Chunk plan
| Chunk | Goal | Flows | Status |
|---|---|---|---|
| 1 | Landing → verified account | ONB-F01..ONB-F04 | pending |

## Defect ledger
| ID | Flow | Severity | Symptom | Host proof | Root cause | Fix | Live verification | Status |
|---|---|---|---|---|---|---|---|---|

## Measurements ledger
| Flow | Persona | Actual time | Actual steps | Hesitations | Errors | Help clicks | Back uses | Drop-off step |
|---|---|---|---|---|---|---|---|---|

## Chunk reports
### Chunk 1 — <goal>   (go sign: <yes/no, date>)
<verdicts, evidence, fixes, unproven, data left, next chunk>

## Next up
- Chunk: N — <goal>
- First flow: ONB-Fxx (<what to do first>)
- Open questions for the user:
```

### Per-flow protocol (adds onboarding lens to `audit-live-flow`)

1. State persona, entry, preconditions; verify preconditions hold (fresh account, no prior data).
2. Start step timer. Perform steps live, in order. Capture:
   - **Hesitation**: pause >10s on a field/decision (record field, duration).
   - **Error**: validation, 4xx, 5xx, timeout, toast, inline message (record exact text).
   - **Help click**: "?", tooltip, docs link, support button (record target).
   - **Back use**: browser back or in-app back from a step (record from→to).
3. Classify. `fail` needs a reproduction. `blocked` names the environment blocker. `unproven` names the settling check.
4. Record measurements in the measurements ledger.

## Cross-cutting onboarding checks

Fold into relevant chunks:

- **Landing promise vs delivery** — does the landing page/CTA promise match the first screen after signup?
- **Empty-state quality** — brand-new account sees helpful empty states with CTAs, not blank tables.
- **Default configuration** — sensible defaults pre-filled; user can reach value without a settings detour.
- **Progress visibility** — user knows where they are in the journey (steps left, what's next).
- **Recovery from interruption** — session expiry mid-flow, tab close, back-button, refresh — does the user resume or restart?
- **Trust signals at each gate** — security badges, testimonials, guarantees visible at signup, payment, first booking.
- **Mobile-first** — the primary onboarding path must work at 375px without horizontal scroll or truncated text.
- **RTL/Locale** — Persian/Farsi copy, digit input, calendar, date formats at every step.
- **Accessibility** — labels, focus order, announcements for dynamic steps, keyboard reach of primary CTA.
- **Referral/invite handling** — invite link lands on the right page with pre-filled context; no "invalid token" for valid links.

## Completion criteria

- Every onboarding entry point and first-value flow has a verdict; out-of-scope listed with reason.
- Every chunk executed and reviewed, go sign recorded for each transition.
- Every `fail`/`partial` fixed and re-verified live, or explicitly deferred with reason.
- Every defect confirmed host-side, or recorded `unproven` with settling check named.
- Measurements ledger complete for every persona × flow.
- Cleanup accurate: audit accounts, bookings, data created, removed, remaining.
- Data-safety contract held.
- `docs/onboarding-audit.md` holds the full run, measurements ledger, and final summary.
- `docs/onboarding-findings.md` (optional, if split) holds the defect ledger with terminal statuses.

## Visual HTML report (onboarding audit)

At the end of each chunk and at the final summary, generate a standalone **HTML report** at `docs/onboarding-report-<chunk-id>.html` (per chunk) and `docs/onboarding-report-final.html` (cumulative). The report must be a single file with embedded CSS/JS (no external dependencies) so it can be opened directly in a browser or shared as an artifact.

### Report structure

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <title>Onboarding Audit Report — <project> — Chunk <N> / Final</title>
  <style>
    /* Embedded: CSS custom properties for theming, responsive grid, print styles */
    :root { --bg:#0b1020; --fg:#e8eefc; --muted:#7a8bb8; --accent:#f0b800; --accent-ink:#0b1020; --card:#121830; --border:#223058; --ok:#22c55e; --warn:#f59e0b; --fail:#ef4444; }
    @media (prefers-color-scheme: light) { :root { --bg:#ffffff; --fg:#0b1b3a; --muted:#5a6d8a; --card:#f8faff; --border:#d5ddec; } }
    /* ... rest of embedded styles ... */
  </style>
</head>
<body>
  <header class="report-header">
    <h1>Onboarding Audit — <Project> — <Chunk N / Final></h1>
    <div class="meta">Run ID: <id> | Deployed: <sha> | Live: <url> | Personas: <N> | Flows: <M> | Generated: <ISO timestamp></div>
  </header>

  <!-- 1. EXECUTIVE FUNNEL -->
  <section id="funnel" class="section">
    <h2>Time-to-Value Funnel</h2>
    <div class="funnel-grid">
      <!-- One card per persona: entry → verified → first login → first value -->
      <article class="persona-funnel" data-persona="mobile-customer">
        <header><h3>Mobile Customer (Instagram)</h3><span class="badge">3:42 min</span></header>
        <div class="steps">
          <div class="step ok" data-step="landing" data-time="0:00">Landing</div>
          <div class="step ok" data-step="signup" data-time="0:38">Signup</div>
          <div class="step warn" data-step="verify" data-time="1:12">OTP Verify</div>
          <div class="step ok" data-step="first-login" data-time="1:45">First Login</div>
          <div class="step ok" data-step="first-booking" data-time="3:42">First Booking ✓</div>
        </div>
        <div class="drop-off">Drop-off: OTP Verify (22s hesitation)</div>
      </article>
      <!-- repeat per persona -->
    </div>
  </section>

  <!-- 2. HESITATION HEATMAP -->
  <section id="hesitation" class="section">
    <h2>Hesitation Heatmap (pauses >10s)</h2>
    <table class="heatmap">
      <thead><tr><th>Flow</th><th>Persona</th><th>Field / Decision</th><th>Duration</th><th>Context</th></tr></thead>
      <tbody>
        <tr><td>ONB-F03</td><td>Mobile Customer</td><td>Phone input (OTP)</td><td>22s</td><td>Persian digits not auto-normalized</td></tr>
        <!-- rows from measurements ledger -->
      </tbody>
    </table>
  </section>

  <!-- 3. TRUST SIGNAL CHECKLIST -->
  <section id="trust" class="section">
    <h2>Trust Signals by Gate</h2>
    <div class="gate-grid">
      <article class="gate"><h4>Signup</h4><ul><li class="ok">SSL badge</li><li class="ok">Testimonial</li><li class="fail">Money-back guarantee</li></ul></article>
      <!-- per gate: signup, verify, payment, first booking -->
    </div>
  </section>

  <!-- 4. DEFECT LEDGER -->
  <section id="defects" class="section">
    <h2>Defects (ONB-###)</h2>
    <ul class="defect-list">
      <li class="defect fail" data-id="ONB-003">
        <strong>ONB-003</strong> — OTP verify fails on Persian digits
        <span class="persona">Mobile Customer</span>
        <span class="flow">ONB-F03</span>
        <span class="status">fixed, awaiting live verification</span>
        <details><summary>Reproduction</summary><pre>...</pre></details>
      </li>
    </ul>
  </section>

  <!-- 5. MEASUREMENTS TABLE -->
  <section id="measurements" class="section">
    <h2>Measurements Ledger</h2>
    <table class="measurements">
      <thead><tr><th>Flow</th><th>Persona</th><th>Time</th><th>Steps</th><th>Hesitations</th><th>Errors</th><th>Help clicks</th><th>Back uses</th><th>Drop-off step</th></tr></thead>
      <tbody>
        <tr><td>ONB-F03</td><td>Mobile Customer</td><td>3:42</td><td>7</td><td>2</td><td>1</td><td>0</td><td>1</td><td>OTP Verify</td></tr>
      </tbody>
    </table>
  </section>

  <footer class="report-footer">
    <p>Generated by `audit-loop`. <a href="#funnel">Back to funnel</a></p>
  </footer>

  <script>
    /* Embedded: tiny interactions — foldable defect details, persona filter, print-to-PDF hint */
  </script>
</body>
</html>
```

### Generation rules

- **Per chunk**: After each chunk's go sign, write `docs/onboarding-report-chunk-<N>.html` with only that chunk's flows + cumulative defect ledger.
- **Final**: After the last chunk, write `docs/onboarding-report-final.html` with all chunks, all personas, complete measurements ledger, and a summary row per persona (total time, total steps, drop-off step, pass/fail).
- **Data source**: Read `docs/onboarding-audit.md` (state file) and `docs/onboarding-findings.md` (or the defect ledger section within the state file) to populate the report. Do not re-run flows.
- **Styling**: Dark-first (matches the app's dark mode), high contrast, Persian/Farsi RTL support in tables, print stylesheet for PDF export.
- **No external assets**: All CSS/JS inlined. No CDN, no images (use inline SVG for icons/checkmarks).
- **Accessibility**: Semantic HTML, ARIA labels on interactive elements, focus-visible outlines, color-blind safe palette.

### Integration

Add this step to the **Chunk loop** (this skill):
> 7. **Generate chunk HTML report** — write `docs/onboarding-report-chunk-<N>.html` from the current state file. Commit it alongside the chunk's changes if the user wants history.

Add this step to **this skill's completion**:
> - `docs/onboarding-report-final.html` generated and committed (or offered as artifact).
