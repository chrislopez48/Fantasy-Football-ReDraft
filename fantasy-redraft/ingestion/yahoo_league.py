import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TOKEN_FILE = Path(__file__).resolve().parent / "yahoo_tokens.json"

LEAGUES_URL = (
    "https://fantasysports.yahooapis.com/fantasy/v2/"
    "users;use_login=1/games;game_codes=nfl/leagues?format=json"
)


def main():
    with TOKEN_FILE.open() as file:
        tokens = json.load(file)

    request = Request(
        LEAGUES_URL,
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=30) as response:
            league_data = json.load(response)
    except HTTPError as error:
        print(f"Yahoo request failed: HTTP {error.code}")
        print(error.read().decode("utf-8", errors="replace"))
        return
    except URLError as error:
        print(f"Connection failed: {error.reason}")
        return

    print(json.dumps(league_data, indent=2))


if __name__ == "__main__":
    main()