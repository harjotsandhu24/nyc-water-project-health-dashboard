"""
Phase 6 — Forecast Date Review rule + overlap analysis.

Defines the second review signal (a populated Forecast Completion
date earlier than May 1, 2026 — the start of the latest reporting
month) and combines it with the missing-start-date signal from
phase5b to produce the dashboard's headline numbers: 29 missing start
date, 22 forecast predates the reporting month, 14 meeting both, and
37 as the union (not the sum) of the two rules.

Run from the analysis/ directory: python phase6_forecast_rule.py
"""
import pandas as pd

dep = pd.read_csv('../data/dep_with_flags.csv', dtype=str)
dep['flag_missing_forecast'] = dep['flag_missing_forecast'].map({'True': True, 'False': False})
dep['flag_missing_phase_start'] = dep['flag_missing_phase_start'].map({'True': True, 'False': False})
dep['Forecast Completion_dt'] = pd.to_datetime(dep['Forecast Completion'], errors='coerce')

# Rule: Forecast Completion populated AND earlier than 2026-05-01
flag_forecast_predates = dep['Forecast Completion_dt'].notna() & (dep['Forecast Completion_dt'] < '2026-05-01')
print("Forecast Predates Reporting Month (May 1, 2026):", flag_forecast_predates.sum())

flag_missing_start = dep['flag_missing_phase_start']
print("Missing Schedule Anchor (missing start date):", flag_missing_start.sum())

overlap = flag_forecast_predates & flag_missing_start
print("Overlap (both rules):", overlap.sum())

union = flag_forecast_predates | flag_missing_start
print("Unique records triggering at least one rule (union, not sum):", union.sum())

only_forecast = flag_forecast_predates & ~flag_missing_start
only_missing = flag_missing_start & ~flag_forecast_predates
print("Forecast-only (no overlap):", only_forecast.sum())
print("Missing-anchor-only (no overlap):", only_missing.sum())

dep['flag_forecast_predates'] = flag_forecast_predates
dep.to_csv('../data/dep_with_flags_v2.csv', index=False)

print("\n=== Example: forecast-only record ===")
print(dep[only_forecast][['FMS Project Name', 'Current Phase', 'Current Phase Start', 'Forecast Completion']].head(3).to_string())
print("\n=== Example: both-rules record ===")
print(dep[overlap][['FMS Project Name', 'Current Phase', 'Current Phase Start', 'Forecast Completion']].head(3).to_string())
print("\n=== Example: missing-anchor-only record ===")
print(dep[only_missing][['FMS Project Name', 'Current Phase', 'Current Phase Start', 'Forecast Completion']].head(3).to_string())
