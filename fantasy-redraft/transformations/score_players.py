import json
from pathlib import Path

from backend.lambda_ranker.scoring import compute_fantasy_points


INPUT_FILE = Path("data/processed/players.json")
OUTPUT_FILE = Path("data/processed/scored_players.json")


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        players = json.load(file)

    scored_players = []

    for player in players:
        fantasy_points, breakdown = compute_fantasy_points(player)

        scored_player = {
            **player,
            "fantasy_points": round(fantasy_points, 2),
            "breakdown": breakdown,
        }

        scored_players.append(scored_player)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(scored_players, file, indent=2)

    print(f"Saved scored data to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()