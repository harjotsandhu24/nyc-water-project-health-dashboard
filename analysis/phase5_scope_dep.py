"""
Phase 5 — DEP scope isolation + PID/FMS ID relationship check.

DEP (the agency managing NYC's water infrastructure) was selected
because its 211-record review scope provided a manageable sample with
strong schedule-field completeness relative to the other eligible
agencies (see phase4). This script isolates those 211 records and
checks how FMS ID and PID relate to each other within that scope —
the check that surfaces the "9 funding IDs repeat" finding.

Run from the analysis/ directory: python phase5_scope_dep.py
"""
import pandas as pd

df = pd.read_csv('../data/raw_capital_projects_export.csv', dtype=str)
latest = df[df['Reporting Period'] == '202605'].copy()
latest['Current Phase'] = latest['Current Phase'].replace({'Construction procurement': 'Construction Procurement'})
STANDARD_PHASES = ['Pre-Design', 'Design', 'Construction Procurement', 'Construction', 'Close-out']
scoped = latest[latest['Current Phase'].isin(STANDARD_PHASES)].copy()

dep = scoped[scoped['Managing Agency'] == 'DEP'].copy()
print("DEP records in review scope:", len(dep))
print("Unique FMS ID:", dep['FMS ID'].nunique())
print("Duplicate FMS ID rows:", len(dep) - dep['FMS ID'].nunique())
print("Unique PID (non-null):", dep['PID'].dropna().nunique())
print("PID populated:", dep['PID'].notna().sum(), "/", len(dep))

# check FMS ID <-> PID relationship
grouped = dep.groupby('FMS ID')['PID'].nunique()
print("\nFMS IDs with >1 distinct PID:", (grouped > 1).sum())
grouped2 = dep.dropna(subset=['PID']).groupby('PID')['FMS ID'].nunique()
print("PIDs with >1 distinct FMS ID:", (grouped2 > 1).sum())

dep.to_csv('../data/dep_active_scope.csv', index=False)
