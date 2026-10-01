import json
from pathlib import Path

SCORING_FILE = Path("config/scoring.json")
INPUT_FILE = Path("data/processed/players.json")
OUTPUT_FILE = Path("data/processed/scored_players.json")


def calculate_fantasy_points(player, scoring):
    stats = player["stats"]

    points = 0

    for stat_name, stat_value in stats.items():
        points += stat_value * scoring.get(stat_name, 0)

    return round(points, 2)

def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        players = json.load(file)

    with SCORING_FILE.open("r", encoding="utf-8") as file:
        scoring = json.load(file)

    scored_players = []

    for player in players:
        player["fantasy_points"] = calculate_fantasy_points(player,scoring)
        scored_players.append(player)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(scored_players, file, indent=2)

    print(f"Saved scored data to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()