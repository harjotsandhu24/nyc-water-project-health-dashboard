# Methodology & findings

Full detail behind the numbers shown in the dashboard and summarized in the
top-level README. Every number below was recomputed directly from the CSV
using the scripts in `analysis/`, and cross-checked against the publisher's
own data dictionary — none of it is assumed or estimated.

## Grain, per the official data dictionary

- **PID**: "Unique identifier that represent a set of schedule managed
  by agency" (foreign key).
- **FMS ID**: "Unique identifier in the Financial Management System
  (FMS)" (foreign key) — a separate identifier system from PID.
- **Total Budget / Spend to Date** reflect FMS "Commitments" /
  "Liquidations."
- The dictionary does not establish a one-to-one PID↔FMS ID
  relationship, consistent with what the data itself shows (below).

## Scope definition

1. **Latest Reporting Period**, identified directly from the data:
   `202605` (May 2026), 5,801 records — not assumed.
2. **One managing agency**, chosen using a reproducible eligibility
   rule applied to all 13 agencies with records in the review scope:
   agencies with between 100 and 300 records. This produced 5 eligible
   agencies:

   | Agency | Records in scope | Missing Forecast Completion |
   |---|---|---|
   | DEP | 211 | 10 (4.7%) |
   | NYPD | 151 | 81 (53.6%) |
   | EDC | 144 | 15 (10.4%) |
   | DCAS | 129 | 20 (15.5%) |
   | DOT | 104 | 28 (26.9%) |

   DEP (NYC's water/environmental-protection agency, referred to as
   "water projects" in the dashboard) was selected because its
   211-record review scope provided a manageable sample with strong
   schedule-field completeness relative to the other eligible
   agencies.

3. **Review-scope definition**, corrected against the data dictionary:
   the dictionary states Current Phase has five standard values
   (Pre-Design, Design, Construction Procurement, Construction,
   Close-out), and that "the use of parentheses indicates the
   rationale for deviations, providing an explanation as to why the
   project does not conform to the standard phase." Parentheses are
   therefore **not** documented as an active/inactive indicator — the
   analysis limits its review to records whose Current Phase exactly
   matches one of the five standard values. This is an analytical
   scope decision made for this project, not an official NYC
   active/inactive classification. Result: 3,162 of 5,801 latest-period
   citywide records match one of the five standard phases; 211 of
   those belong to DEP.

## Data quality findings

| Issue | Affected records | Treatment | Reason |
|---|---|---|---|
| 9 FMS IDs shared across multiple PIDs within DEP's 211-record scope | 9 | Total Budget not summed into a portfolio total; shown at the record level | Summing would double-count shared funding lines |
| Missing Current Phase Start | 29 of 211 | Flagged (missing start date), not deleted | A genuine gap in the public record, not established evidence of a data error |
| Populated Forecast Completion earlier than May 1, 2026 (the start of this reporting month) | 22 of 211 | Flagged (finish date already passed), not deleted | A published date worth a closer look on its face, not a confirmed delay |
| Both rules together | 14 | Counted once, not twice | The two rules overlap — union (unique flagged records) is 37, not 29 + 22 = 51 |
| Spend to Date > Total Budget | 0 | Checked and clear | Documented as checked, not silently omitted |

## Review signals (211 DEP records in review scope)

- **Missing start date**: Current Phase Start unavailable — 29 records
- **Finish date already passed**: Forecast Completion populated and
  earlier than May 1, 2026 — 22 records
- **Both**: 14 records
- **Worth reviewing (union of the two signals)**: 37 records

These are analytical review labels created for this portfolio project,
not official NYC project classifications. They identify records worth
a closer look based on the two defined signals above — they are not a
claim that any flagged record is failing, delayed, or over budget.

## Three records shown as examples

Chosen to show each rule combination once:

- **Conversion of Kensico Lab to EOH Operations HQ** — Construction —
  finish date already passed only (has a Current Phase Start; forecast
  12/19/2025 predates the reporting month)
- **Delaware–Rondout Aqueduct (Parallel Tunnel to RWBT)** — Close-out —
  both signals (missing Current Phase Start; forecast 12/05/2025
  predates)
- **Completion of CT3 Stage 2 B/Q Leg & Bklyn Downtake Interconnection**
  (shown on the dashboard as "City Water Tunnel 3 — Stage 2
  connection") — Pre-Design — missing start date only (no forecast
  date exists to evaluate against the second signal)

## What this does and doesn't claim

No project failure, delay, cost overrun, schedule-change cause,
savings, or performance improvement is claimed anywhere in this
project. No claim is made that DEP performs better than another
agency, or that this 211-record scope represents the complete set of
DEP's projects. Every displayed number traces to the scripts in
`analysis/`, run directly against the supplied CSV and verified
against the official data dictionary.
