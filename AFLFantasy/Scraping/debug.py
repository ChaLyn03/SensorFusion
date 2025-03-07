import pandas as pd

# Load the full dataset
df = pd.read_csv("AFL_Players_Merged.csv")

# Normalize text formatting
df["Position_x"] = df["Position_x"].str.upper().str.strip()

# Extract primary and secondary positions
df["Primary Position"] = df["Position_x"].apply(lambda x: x.split(" / ")[0] if " / " in x else x)
df["Secondary Position"] = df["Position_x"].apply(lambda x: x.split(" / ")[1] if " / " in x else "")

# Standardize position names
position_map = {
    "DEFENDER": "DEF",
    "MIDFIELDER": "MID",
    "RUCK": "RUC",
    "FORWARD": "FWD"
}

df["Primary Position"] = df["Primary Position"].replace(position_map)
df["Secondary Position"] = df["Secondary Position"].replace(position_map)

# Select only necessary columns
columns_needed = [
    "Player ID", "First Name_x", "Last Name_x", 
    "Primary Position", "Secondary Position", 
    "Salary ($)", "Total Points", "Average Points"
]
df_cleaned = df[columns_needed]

# Rename columns for clarity
df_cleaned = df_cleaned.rename(columns={
    "First Name_x": "First Name",
    "Last Name_x": "Last Name"
})

# Save the streamlined dataset
df_cleaned.to_csv("AFL_Players_Optimized.csv", index=False)

# Debug output
print("✅ Streamlined dataset saved as 'AFL_Players_Optimized.csv'")
print(df_cleaned.head())
