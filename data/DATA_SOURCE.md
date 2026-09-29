# Data source

**Dataset:** NYC Capital Projects Dashboard — Citywide Budget and Schedule
**Publisher:** NYC Office of Management and Budget / Mayor's Office of
Operations (Capital Projects Dashboard)

## What's in this folder

| File | What it is |
|---|---|
| `raw_capital_projects_export.csv` | The citywide export as downloaded, covering 10 reporting periods across all managing agencies. 56,525 rows. |
| `dep_active_scope.csv` | Output of `analysis/phase5_scope_dep.py` — the latest reporting period (May 2026), narrowed to records in the five standard `Current Phase` values, narrowed to DEP (NYC's water/environmental-protection agency). 211 rows. |
| `dep_with_flags.csv` | Output of `analysis/phase5b_attention.py` — the same 211 records with several candidate review-signal columns added. |
| `dep_with_flags_v2.csv` | Output of `analysis/phase6_forecast_rule.py` — the final 211-record dataset with both review-signal flags and the union/overlap logic applied. This is the dataset the dashboard's 37-record review count is drawn from. |

Field definitions (PID, FMS ID, Total Budget, Spend to Date, Current
Phase, etc.) are documented in the publisher's own data dictionary,
included at `docs/Capital_Projects_Dashboard_Data_Dictionary.xlsx`
("Column Information" sheet).

## Scope, step by step

1. **56,525 → 5,801** — the raw export spans 10 reporting periods; the
   analysis uses only the latest one (`202605`, May 2026), identified
   directly from the data.
2. **5,801 → 211** — of the 5,801 latest-period records, 3,162 have a
   `Current Phase` matching one of the five standard values the
   publisher's data dictionary defines (Pre-Design, Design,
   Construction Procurement, Construction, Close-out). Every agency
   with between 100 and 300 records in that 3,162 was compared, and
   DEP (211 records, only 4.7% missing a Forecast Completion date) was
   selected as the review scope.
3. **211 → 37** — two review signals were defined and checked against
   DEP's 211 records: a missing `Current Phase Start` date (29
   records), and a populated `Forecast Completion` date earlier than
   May 1, 2026, the start of the reporting month (22 records). 14
   records meet both. The **37** reported by the dashboard is the
   union of the two signals (29 + 22 − 14 = 37), not their sum.

## Regenerating the data

`dep_active_scope.csv`, `dep_with_flags.csv`, and `dep_with_flags_v2.csv`
are all regenerated automatically by the scripts in `analysis/` — see
the main README for run instructions. They're committed here so the
dashboard numbers can be checked without having to run the pipeline
first.
