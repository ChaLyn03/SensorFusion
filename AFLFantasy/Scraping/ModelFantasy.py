import pandas as pd
import pulp

def main():
    # 1) Load your optimized dataset
    # Must contain columns: 
    # ["Player ID", "First Name", "Last Name", 
    #  "Primary Position", "Secondary Position", 
    #  "Salary ($)", "Total Points", "Average Points"]
    file_path = "AFL_Players_Optimized.csv"  # or whichever file has primary/secondary
    df = pd.read_csv(file_path)

    # 2) Define the ILP model
    model = pulp.LpProblem("AFL_Fantasy_Optimization", pulp.LpMaximize)

    # 3) Create decision variables for each player *only* in their allowed positions
    # (primary, secondary)
    player_vars = {}

    # Helper to normalize position strings
    def fix_pos(pos):
        p = str(pos).strip().upper()
        mapping = {
            "DEFENDER": "DEF",
            "MIDFIELDER": "MID",
            "FORWARD": "FWD",
            "RUCK": "RUC",
            "DEF": "DEF",
            "MID": "MID",
            "FWD": "FWD",
            "RUC": "RUC",
            ""
: ""
        }
        return mapping.get(p, "")

    for idx, row in df.iterrows():
        pid = row["Player ID"]
        primary = fix_pos(row["Primary Position"])
        secondary = fix_pos(row["Secondary Position"])

        allowed_positions = set()
        if primary:
            allowed_positions.add(primary)
        if secondary:
            allowed_positions.add(secondary)

        # Create a binary decision var for each allowed position
        for pos in allowed_positions:
            var_name = f"x_{pid}_{pos}"
            player_vars[(pid, pos)] = pulp.LpVariable(var_name, cat=pulp.LpBinary)

    # 4) Binary variables for the four valid formations
    # Each formation sums to 30 players in total
    formation_vars = {
        "f1": pulp.LpVariable("f1", cat=pulp.LpBinary),  # (9 DEF, 10 MID, 3 RUC, 8 FWD)
        "f2": pulp.LpVariable("f2", cat=pulp.LpBinary),  # (8 DEF, 11 MID, 3 RUC, 8 FWD)
        "f3": pulp.LpVariable("f3", cat=pulp.LpBinary),  # (8 DEF, 10 MID, 4 RUC, 8 FWD)
        "f4": pulp.LpVariable("f4", cat=pulp.LpBinary),  # (8 DEF, 10 MID, 3 RUC, 9 FWD)
    }

    # 5) Objective: maximize total points
    model += pulp.lpSum(
        row["Total Points"] * player_vars[(row["Player ID"], pos)]
        for _, row in df.iterrows()
        for pos in ["DEF", "MID", "FWD", "RUC"]
        if (row["Player ID"], pos) in player_vars
    ), "Maximize_Total_Points"

    # 6) Salary cap <= 17.8M
    model += pulp.lpSum(
        row["Salary ($)"] * player_vars[(row["Player ID"], pos)]
        for _, row in df.iterrows()
        for pos in ["DEF", "MID", "FWD", "RUC"]
        if (row["Player ID"], pos) in player_vars
    ) <= 17_800_000, "Salary_Cap"

    # 7) Each player can only occupy one position (among their allowed ones)
    for idx, row in df.iterrows():
        pid = row["Player ID"]
        allowed_sum = pulp.lpSum(
            player_vars[(pid, p)]
            for p in ["DEF", "MID", "FWD", "RUC"]
            if (pid, p) in player_vars
        )
        model += allowed_sum <= 1, f"One_Position_{pid}"

    # 8) Exactly one formation is chosen
    model += pulp.lpSum(formation_vars.values()) == 1, "One_Formation"

    # Helper: sum across all players assigned to a certain position
    def sum_pos(pos):
        return pulp.lpSum(
            player_vars[(row["Player ID"], pos)]
            for _, row in df.iterrows()
            if (row["Player ID"], pos) in player_vars
        )

    # 9) Formation-based constraints
    # f1 => 9 DEF, 10 MID, 3 RUC, 8 FWD
    model += sum_pos("DEF") == (9*formation_vars["f1"] + 8*formation_vars["f2"] + 8*formation_vars["f3"] + 8*formation_vars["f4"]), "DEF_Count"
    model += sum_pos("MID") == (10*formation_vars["f1"] + 11*formation_vars["f2"] + 10*formation_vars["f3"] + 10*formation_vars["f4"]), "MID_Count"
    model += sum_pos("RUC") == (3*formation_vars["f1"] + 3*formation_vars["f2"] + 4*formation_vars["f3"] + 3*formation_vars["f4"]), "RUC_Count"
    model += sum_pos("FWD") == (8*formation_vars["f1"] + 8*formation_vars["f2"] + 8*formation_vars["f3"] + 9*formation_vars["f4"]), "FWD_Count"

    # Because each formation sums to 30 exactly, we do NOT add a separate Utility spot.
    # The total is 30 automatically.

    # 10) Solve
    solver = pulp.PULP_CBC_CMD(msg=True)
    result_status = model.solve(solver)
    print(f"Solver status: {pulp.LpStatus[result_status]}")

    # 11) Extract chosen players
    selected_players = []
    for idx, row in df.iterrows():
        pid = row["Player ID"]
        fname = row.get("First Name", "")
        lname = row.get("Last Name", "")
        ppos = row.get("Primary Position", "")
        spos = row.get("Secondary Position", "")
        sal = row["Salary ($)"]
        tpoints = row["Total Points"]
        avg_pts = row["Average Points"]

        for pos in ["DEF", "MID", "FWD", "RUC"]:
            if (pid, pos) in player_vars and pulp.value(player_vars[(pid, pos)]) == 1:
                selected_players.append({
                    "Player ID": pid,
                    "First Name": fname,
                    "Last Name": lname,
                    "Assigned Position": pos,
                    "Primary Position": ppos,
                    "Secondary Position": spos,
                    "Salary ($)": sal,
                    "Total Points": tpoints,
                    "Average Points": avg_pts
                })

    selected_df = pd.DataFrame(selected_players)
    selected_df.to_csv("optimized_afl_fantasy_team.csv", index=False)
    print("Optimized AFL Fantasy Team saved to 'optimized_afl_fantasy_team.csv'")

    # 12) Print summary
    if not selected_df.empty:
        total_salary = selected_df["Salary ($)"].sum()
        total_points = selected_df["Total Points"].sum()
        print(f"Total Salary: ${total_salary:,.0f}")
        print(f"Total Points: {total_points}")

if __name__ == "__main__":
    main()
