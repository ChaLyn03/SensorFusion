import pandas as pd
from datetime import datetime

# Load datasets
fantasy_df = pd.read_csv("AFL_Fantasy_Players.csv")
stats_df = pd.read_csv("AFL_Player_Stats.csv")

# Clean up Player ID format for merging
stats_df["Player ID"] = stats_df["Player ID"].str.replace("CD_I", "", regex=False)
fantasy_df["Player ID"] = fantasy_df["Player ID"].astype(str)
stats_df["Player ID"] = stats_df["Player ID"].astype(str)

# Merge datasets on Player ID
merged_df = pd.merge(fantasy_df, stats_df, on="Player ID", how="inner")

# Constants
magic_number = 10260  # Fantasy salary multiplier
current_year = 2025

# Fantasy Salary Metrics
merged_df["Fantasy Salary ($)"] = merged_df["Average Points"] * magic_number
merged_df["Value per Fantasy Point"] = merged_df["Fantasy Salary ($)"] / merged_df["Total Points"]

# Break Even and Price Change
merged_df["Break Even Score"] = merged_df["Fantasy Salary ($)"] / magic_number
merged_df["Projected Price Change"] = ((merged_df["Average dreamTeamPoints"] - merged_df["Break Even Score"]) * magic_number)

# Performance Efficiency Metrics
merged_df["Fantasy Points per Game"] = merged_df["Total Points"] / merged_df["Games Played_x"]
merged_df["Metres Gained per Possession"] = merged_df["Total metresGained"] / merged_df["Total disposals"]
merged_df["Score Involvement Rate (%)"] = (merged_df["Total scoreInvolvements"] / merged_df["Total disposals"]) * 100
merged_df["Clanger Rate (%)"] = (merged_df["Total clangers"] / merged_df["Total disposals"]) * 100
merged_df["Disposal Efficiency (%)"] = (merged_df["Total effectiveDisposals"] / merged_df["Total disposals"]) * 100
merged_df["Kick Efficiency (%)"] = (merged_df["Total effectiveKicks"] / merged_df["Total kicks"]) * 100
merged_df["Tackle Efficiency (%)"] = (merged_df["Total tackles"] / merged_df["Total pressureActs"]) * 100
merged_df["Hitout Win Rate (%)"] = (merged_df["Total hitoutsToAdvantage"] / merged_df["Total hitouts"]) * 100
merged_df["Goal Conversion Rate (%)"] = (merged_df["Total goals"] / merged_df["Total shotsAtGoal"]) * 100

# Career Experience Metrics
merged_df["Career Experience (Years)"] = current_year - merged_df["Debut Year"]
merged_df["Draft Age"] = merged_df["Draft Year"] - pd.to_datetime(merged_df["Date of Birth"], format="%d/%m/%Y", errors="coerce").dt.year
merged_df["Height-to-Weight Ratio"] = merged_df["Height (cm)"] / merged_df["Weight (kg)"]

# Fantasy Underpriced Flag
merged_df["Underpriced Flag"] = merged_df["Salary ($)"] < merged_df["Fantasy Salary ($)"]
merged_df["Draft Age"] = merged_df["Draft Year"] - pd.to_datetime(merged_df["Date of Birth"], format="%d/%m/%Y", errors="coerce").dt.year

# Save enhanced dataset
merged_df.to_csv("AFL_Players_Merged.csv", index=False)
print("Dataset enhanced and saved as AFL_Players_Merged.csv")

# Load the merged dataset
file_path = "AFL_Players_Merged.csv"  # Update with your local path
merged_df = pd.read_csv(file_path)

# Identify numerical columns (excluding IDs, years, etc.)
float_cols = merged_df.select_dtypes(include=['float64']).columns

# Round float columns to 2 decimal places
merged_df[float_cols] = merged_df[float_cols].round(2)

# Save the cleaned dataset
cleaned_file_path = "AFL_Players_Merged_Cleaned.csv"
merged_df.to_csv(cleaned_file_path, index=False)