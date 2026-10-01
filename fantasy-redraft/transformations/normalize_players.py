import json
from pathlib import Path

RAW_FILE = Path("data/raw/sample_players.json")
PROCESSED_FILE = Path("data/processed/players.json")


def normalize_player(player):
    return {
        "name": player["name"],
        "position": player["position"],

        "pass_yd": player.get("pass_yd", 0),
        "pass_td": player.get("pass_td", 0),
        "interceptions": player.get("interception", 0),

        "rush_yd": player.get("rush_yd", 0),
        "rush_td": player.get("rush_td", 0),

        "reception": player.get("receptions", 0),
        "rec_yd": player.get("rec_yd", 0),
        "rec_td": player.get("rec_td", 0),
    }


def main():
    with RAW_FILE.open("r", encoding="utf-8") as file:
        raw_players = json.load(file)

    normalized_players = [
        normalize_player(player)
        for player in raw_players["players"]
    ]

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    with PROCESSED_FILE.open("w", encoding="utf-8") as file:
        json.dump(normalized_players, file, indent=2)

    print(f"Saved processed data to {PROCESSED_FILE}")


if __name__ == "__main__":
    main()