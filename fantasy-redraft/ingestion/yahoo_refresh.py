#throwing this file up to deal with refresh token issues
import os
import json
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TOKEN_FILE = Path(__file__).resolve().parent / "yahoo_tokens.json"
CLIENT_ID = os.environ["YAHOO_CLIENT_ID"]


def refresh_access_token():
    tokens = json.loads(TOKEN_FILE.read_text())

    refresh_token = tokens["refresh_token"]

    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.login.yahoo.com/oauth2/get_token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            new_tokens = json.load(response)

    except HTTPError as error:
        print(f"Yahoo returned HTTP {error.code}")

        error_body = error.read().decode("utf-8")
        print(error_body)

        return

    tokens.update(new_tokens)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    TOKEN_FILE.chmod(0o600)

    print("Yahoo access token refreshed successfully!")


if __name__ == "__main__":
    refresh_access_token()