import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TOKEN_FILE = Path(__file__).resolve().parent / "yahoo_tokens.json"

LEAGUE_KEY = "470.l.84183"  # Mom and Pop Shop id # for 2026 season

LEAGUES_URL = (
    f"https://fantasysports.yahooapis.com/fantasy/v2/"
    f"league/{LEAGUE_KEY}/settings?format=json"
)                           #will only bring back mom and pop shop, not other leagues


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