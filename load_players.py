import csv

FILE_PATH = "data/weekly/players_2025.csv"

players = []


def calculate_fantasy_points(player):
    points = 0.0

    # Passing
    points += player["pass_yd"] / 25
    points += player["pass_td"] * 4
    points -= player["interceptions"] * 2

    # Rushing
    points += player["rush_yd"] / 10
    points += player["rush_td"] * 6

    # Receiving
    points += player["receptions"] * 1
    points += player["rec_yd"] / 10
    points += player["rec_td"] * 6

    # Turnovers
    points -= player["fumbles"] * 2

    return round(points, 2)


with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        player = {
            "name": row["name"],
            "position": row["position"],
            "team": row["team"],
            "adp": int(row["adp"]),
            "points": float(row["points"]),
            "games_played": int(row["games_played"]),
            "pass_yd": float(row["pass_yd"]),
            "pass_td": int(row["pass_td"]),
            "interceptions": int(row["interceptions"]),
            "rush_yd": float(row["rush_yd"]),
            "rush_td": int(row["rush_td"]),
            "receptions": int(row["receptions"]),
            "rec_yd": float(row["rec_yd"]),
            "rec_td": int(row["rec_td"]),
            "fumbles": int(row["fumbles"])
        }

        player["calculated_points"] = calculate_fantasy_points(player)
        players.append(player)

players.sort(key=lambda p: p["calculated_points"], reverse=True)

print("REDRAFT RANKINGS")
print()

for i, player in enumerate(players, start=1):
    redraft_rank = i
    value_diff = player["adp"] - redraft_rank

    if value_diff > 0:
        label = "STEAL"
    elif value_diff < 0:
        label = "BUST"
    else:
        label = "EVEN"

    print(
        f"{redraft_rank}. {player['name']} | {player['position']} | {player['team']} "
        f"| ADP: {player['adp']} | Points: {player['calculated_points']} "
        f"| Value Diff: {value_diff} | {label}"
    )