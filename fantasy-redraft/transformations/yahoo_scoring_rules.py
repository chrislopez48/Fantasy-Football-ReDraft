import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/raw/yahoo_league_settings_2026.json"


def load_yahoo_settings():
    with open(INPUT_FILE, "r") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":
    settings = load_yahoo_settings()
    print("Yahoo settings loaded successfully!")