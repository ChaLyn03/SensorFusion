import requests
import pandas as pd

# AFL API URL
api_url = "https://api.afl.com.au/statspro/playersStats/seasons/CD_S2024014?includeBenchmarks=false"

# Insert your actual token here
headers = {
    "User-Agent": "Mozilla/5.0",
    "x-media-mis-token": "34cd01cc054c21d42cc01f736075f0c0"  # Insert your token
}

# Fetch the data
response = requests.get(api_url, headers=headers)
try:
    data = response.json()
except ValueError:
    print("Error: API did not return JSON data. Here is the response:")
    print(response.text)
    exit()

# Extract the list of players
players = data.get("players", [])

# Create a list to store structured data
player_data = []

# Iterate over each player
for player in players:
    player_id = player.get("playerId", "")
    details = player.get("playerDetails", {})
    team = player.get("team", {})
    totals = player.get("totals", {})
    averages = player.get("averages", {})

    # Player Details
    player_info = {
        "Player ID": player_id,
        "First Name": details.get("givenName", ""),
        "Last Name": details.get("surname", ""),
        "Full Name": f"{details.get('givenName', '')} {details.get('surname', '')}".strip(),
        "Age": details.get("age", ""),
        "Height (cm)": details.get("heightCm", ""),
        "Weight (kg)": details.get("weightKg", ""),
        "Jumper Number": details.get("jumperNumber", ""),
        "Kicking Foot": details.get("kickingFoot", ""),
        "State of Origin": details.get("stateOfOrigin", ""),
        "Draft Year": details.get("draftYear", ""),
        "Debut Year": details.get("debutYear", ""),
        "Draft Position": details.get("draftPosition", ""),
        "Draft Type": details.get("draftType", ""),
        "Position": details.get("position", ""),
        "Recruited From": details.get("recruitedFrom", ""),
        "Date of Birth": details.get("dateOfBirth", ""),
        "Photo URL": details.get("photoURL", ""),
        "Team": team.get("teamName", ""),
        "Team Abbreviation": team.get("teamAbbr", ""),
        "Games Played": player.get("gamesPlayed", ""),
    }

    # Add total stats
    for stat, value in totals.items():
        player_info[f"Total {stat}"] = value

    # Add average stats
    for stat, value in averages.items():
        player_info[f"Average {stat}"] = value

    # Append structured data
    player_data.append(player_info)

# Convert to DataFrame
df = pd.DataFrame(player_data)

# Save to CSV
csv_filename = "AFL_Player_Stats.csv"
df.to_csv(csv_filename, index=False)

print(f"✅ Successfully saved AFL stats to {csv_filename}")
