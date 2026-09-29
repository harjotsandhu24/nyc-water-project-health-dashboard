"""
Phase 5b — Review-signal rule testing (DEP scope).

Tests several candidate data-quality rules against the 211-record DEP
scope. The two rules that became the dashboard's review signals are
"missing Current Phase Start" and (in phase6) "Forecast Completion
predates the reporting month" — this script is where the missing
Current Phase Start rule (29 records) is established, alongside a few
other checks run and documented as checked-and-clear.

Run from the analysis/ directory: python phase5b_attention.py
"""
import pandas as pd

dep = pd.read_csv('../data/dep_active_scope.csv', dtype=str)


def parse_money(s):
    if pd.isna(s):
        return None
    return float(s.replace('$', '').replace(',', ''))


dep['Total Budget Num'] = dep['Total Budget'].apply(parse_money)
dep['Spend to Date Num'] = dep['Spend to Date'].apply(parse_money)

for col in ['Current Phase Start', 'Forecast Current Phase End', 'Forecast Completion']:
    dep[col + '_dt'] = pd.to_datetime(dep[col], errors='coerce')

# Rule 1: missing forecast completion
flag_missing_forecast = dep['Forecast Completion'].isna()
print("Rule 1 - Missing Forecast Completion:", flag_missing_forecast.sum())

# Rule 2: Spend to Date > Total Budget
flag_overspend = (dep['Spend to Date Num'] > dep['Total Budget Num'])
print("Rule 2 - Spend to Date > Total Budget:", flag_overspend.sum())
if flag_overspend.sum() > 0:
    print(dep[flag_overspend][['FMS Project Name', 'Total Budget', 'Spend to Date']])

# Rule 3: Forecast Completion earlier than Current Phase Start (impossible ordering)
valid_both = dep.dropna(subset=['Current Phase Start_dt', 'Forecast Completion_dt'])
flag_impossible = valid_both['Forecast Completion_dt'] < valid_both['Current Phase Start_dt']
print("\nRule 3 - Forecast Completion before Current Phase Start:", flag_impossible.sum())

# Rule 4: missing Current Phase Start (basic schedule anchor missing)
# -> this is the "missing start date" review signal used in the dashboard
flag_missing_phase_start = dep['Current Phase Start'].isna()
print("Rule 4 - Missing Current Phase Start:", flag_missing_phase_start.sum())

# Rule 5: missing Spend to Date
flag_missing_spend = dep['Spend to Date'].isna()
print("Rule 5 - Missing Spend to Date:", flag_missing_spend.sum())

dep['flag_missing_forecast'] = flag_missing_forecast
dep['flag_overspend'] = flag_overspend
dep['flag_missing_phase_start'] = flag_missing_phase_start
dep['flag_missing_spend'] = flag_missing_spend

any_flag = flag_missing_forecast | flag_overspend | flag_missing_phase_start | flag_missing_spend
print("\nTotal records with >=1 attention flag (all 5 candidate rules):", any_flag.sum())
dep['any_flag'] = any_flag

dep.to_csv('../data/dep_with_flags.csv', index=False)
