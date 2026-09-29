"""
Phase 4 — Review-scope rule + full-population agency comparison.

Per the official data dictionary, Current Phase has five standard
values (Pre-Design, Design, Construction Procurement, Construction,
Close-out); parentheses indicate "the rationale for deviations," not
an official active/inactive status. This script applies that as an
analytical scope decision (not an NYC classification), then compares
every agency to pick which one to focus the review on.

Run from the analysis/ directory: python phase4_review_scope.py
"""
import pandas as pd

df = pd.read_csv('../data/raw_capital_projects_export.csv', dtype=str)
latest = df[df['Reporting Period'] == '202605'].copy()
latest['Current Phase'] = latest['Current Phase'].replace({'Construction procurement': 'Construction Procurement'})

# Per the official data dictionary: Current Phase has five standard
# values. Parentheses indicate "the rationale for deviations," NOT an
# official active/inactive status. This scope rule is an analytical
# decision for this project, not an NYC classification.
STANDARD_PHASES = ['Pre-Design', 'Design', 'Construction Procurement', 'Construction', 'Close-out']

scoped = latest[latest['Current Phase'].isin(STANDARD_PHASES)].copy()
print("Total latest-period records:", len(latest))
print("Records matching one of the five standard phases:", len(scoped))
print("Excluded (parenthesized deviation codes):", len(latest) - len(scoped))

print("\nRecords in scope by agency (all 13):")
print(scoped['Managing Agency'].value_counts())

# Reproducible eligibility rule, applied to the full agency population
counts = scoped['Managing Agency'].value_counts()
eligible = counts[(counts >= 100) & (counts <= 300)]
print("\nEligible agencies (100-300 records in scope):")
print(eligible)

for agency in eligible.index:
    sub = scoped[scoped['Managing Agency'] == agency]
    missing_forecast = sub['Forecast Completion'].isna().sum()
    print(f"{agency}: n={len(sub)}, missing Forecast Completion={missing_forecast} ({missing_forecast/len(sub)*100:.1f}%)")
