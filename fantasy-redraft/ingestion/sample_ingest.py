import json
from pathlib import Path


RAW_DATA_DIR = Path("data/raw")


def save_raw_data(data: dict, filename: str) -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = RAW_DATA_DIR / filename

    with open(output_path, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Saved raw data to {output_path}")


if __name__ == "__main__":
    sample_data = {
        "source": "sample",
        "players": [
            {
                "name": "Test QB",
                "position": "QB",
                "pass_yd": 300,
                "pass_td": 3,
                "interception": 1
            },
            {
                "name": "Test RB",
                "position": "RB",
                "rush_yd": 110,
                "rush_td": 1,
                "receptions": 4
            }
        ]
    }

    save_raw_data(sample_data, "sample_players.json")