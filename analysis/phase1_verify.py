"""
Phase 1 — Raw file inspection.

Loads the raw citywide export as-downloaded and prints the shape,
reporting periods, and agency counts so the scope (latest reporting
period, one agency) can be defined from what's actually in the file.

Run from the analysis/ directory: python phase1_verify.py
"""
import pandas as pd
pd.set_option('display.max_rows', 50)

df = pd.read_csv('../data/raw_capital_projects_export.csv', dtype=str)

print("Total rows:", len(df))
print("\nReporting Period values:")
print(df['Reporting Period'].value_counts().sort_index())
print("\nLatest Reporting Period:", df['Reporting Period'].max())

print("\nManaging Agency counts (all periods):")
print(df['Managing Agency'].value_counts().head(20))

print("\nFMS ID uniqueness:")
print("total FMS ID (non-null):", df['FMS ID'].notna().sum())
print("unique FMS ID:", df['FMS ID'].nunique())

print("\nPID uniqueness:")
print("total PID (non-null):", df['PID'].notna().sum())
print("unique PID:", df['PID'].nunique())

print("\nCurrent Phase values:")
print(df['Current Phase'].value_counts())
