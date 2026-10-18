# Onboarding HTML report

Onboarding-specific sections, filenames, data source, and integration notes. The generic rules — document shell, section order, severity table, per-finding evidence links, inline CSS, and the offline single-file constraint — live in `skill://audit-loop/references/html-report` and are not restated here.

## Filenames

- Per chunk: `docs/onboarding-report-chunk-<N>.html` — only that chunk's flows plus the cumulative defect ledger.
- Final: `docs/onboarding-report-final.html` — all chunks, all personas, complete measurements ledger, and a summary row per persona (total time, total steps, drop-off step, pass/fail).

## Data source

`docs/onboarding-audit.md` (state file, including the measurements ledger) and `docs/onboarding-findings.md` (or the defect ledger section within the state file).

## Onboarding sections

Slot these into the parent spec's section order:

1. **Time-to-value funnel** — one card per persona tracing entry → verified → first login → first value, with actual time against the time budget and the drop-off step named. Example card: Mobile Customer (Instagram) — Landing 0:00, Signup 0:38, OTP Verify 1:12 (22s hesitation), First Login 1:45, First Booking 3:42; drop-off: OTP Verify.
2. **Hesitation heatmap** — pauses over 10 seconds, one row per hesitation: flow, persona, field or decision, duration, context. Rows come from the measurements ledger. Example: ONB-F03, Mobile Customer, phone input (OTP), 22s, Persian digits not auto-normalized.
3. **Trust-signal checklist** — one gate group per gate (signup, verify, payment, first booking) listing each signal as present or missing. Example: signup shows SSL badge and testimonial, money-back guarantee missing.
4. **Defect ledger** — every `ONB-###` finding with persona, flow, status text, and a foldable reproduction (steps, observed vs expected, host proof). Statuses use the same wording as the ledger: `fixed, awaiting live verification` stays explicit, never shown as closed.
5. **Measurements ledger** — the full table: flow, persona, actual time, actual steps, hesitations, errors, help clicks, back uses, drop-off step. Tables support Persian/Farsi RTL content.

## Integration

Add this step to the **Chunk loop** (onboarding pass):
> 7. **Generate chunk HTML report** — write `docs/onboarding-report-chunk-<N>.html` from the current state file. Commit it alongside the chunk's changes if the user wants history.

Add this step to the **onboarding pass completion**:
> - `docs/onboarding-report-final.html` generated and committed (or offered as artifact).
