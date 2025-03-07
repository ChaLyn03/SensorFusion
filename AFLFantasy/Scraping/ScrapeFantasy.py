import requests
import csv

# Define the API URL
api_url = "https://fantasy.afl.com.au/data/afl/players.json"

# Set headers to mimic a real browser request (optional but recommended)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Fetch the data from the API
response = requests.get(api_url, headers=headers)

# Parse the JSON response
players_data = response.json()

# Define the CSV file name
csv_filename = "AFL_Fantasy_Players.csv"

# Open CSV file for writing
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the CSV headers
    writer.writerow(["Player ID", "First Name", "Last Name", "Position", "Salary ($)", "Games Played", "Total Points", "Average Points"])

    # Loop through each player in the data
    for player in players_data:
        player_id = player.get("id", "N/A")
        first_name = player.get("first_name", "N/A")
        last_name = player.get("last_name", "N/A")
        salary = player.get("cost", "N/A")
        games_played = player.get("stats", {}).get("games_played", "N/A")
        total_points = player.get("stats", {}).get("total_points", "N/A")
        avg_points = player.get("stats", {}).get("avg_points", "N/A")

        # Convert position numbers to readable names
        position_map = {
            1: "Defender",
            2: "Midfielder",
            3: "Ruck",
            4: "Forward"
        }
        positions = [position_map.get(pos, "Unknown") for pos in player.get("positions", [])]
        positions_str = " / ".join(positions) if positions else "N/A"

        # Write player data to CSV
        writer.writerow([player_id, first_name, last_name, positions_str, salary, games_played, total_points, avg_points])

print(f"✅ Data successfully saved to {csv_filename}")
