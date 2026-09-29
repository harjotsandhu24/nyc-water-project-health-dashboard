"""
Phase 1b — Isolate the latest reporting period.

The dashboard is scoped to the most recent citywide reporting period
(202605 / May 2026), identified directly from the data rather than
assumed. This is the step that produces the 56,525 -> 5,801 narrowing.

Run from the analysis/ directory: python phase1b_latest.py
"""
import pandas as pd

df = pd.read_csv('../data/raw_capital_projects_export.csv', dtype=str)

latest = df[df['Reporting Period'] == '202605'].copy()
print("Latest period rows:", len(latest))

print("\nUnique FMS ID in latest period:", latest['FMS ID'].nunique())
print("Duplicate FMS ID in latest period:", len(latest) - latest['FMS ID'].nunique())

print("\nManaging Agency counts (latest period only):")
print(latest['Managing Agency'].value_counts())

print("\nCurrent Phase values (latest period, all agencies):")
print(latest['Current Phase'].value_counts().head(20))
