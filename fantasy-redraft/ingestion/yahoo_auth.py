import base64
import hashlib
import json
import os
import secrets
from pathlib import Path
from urllib.error import HTTPError                  #help us decode terminal line issues
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
REDIRECT_URI = "https://github.com/chrislopez48/Fantasy-Football-ReDraft"

TOKEN_FILE = Path(__file__).resolve().parent / "yahoo_tokens.json" #resolve makes path absolute


def main():
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)               #this is the PKCE verifier

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("ascii")).digest() #hashlib converts sting into bytes
    ).decode("ascii").rstrip("=")

    parameters = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": "fspt-r",
    }

    authorization_url = (
        "https://api.login.yahoo.com/oauth2/request_auth?"
        + urlencode(parameters)
    )

    print("Open this URL and approve Yahoo access:")
    print(authorization_url)

    redirected_url = input(
        "\nPaste the complete URL from your browser after approval: "
    ).strip()

    callback = urlsplit(redirected_url)
    expected = urlsplit(REDIRECT_URI)

    if (callback.scheme, callback.netloc, callback.path) != (
        expected.scheme, expected.netloc, expected.path
    ):
        print("The redirect address does not match. Start again.")
        return

    query = parse_qs(callback.query)

    returned_state = query.get("state", [""])[0]
    if not secrets.compare_digest(returned_state, state):
        print("State verification failed. Start again.")
        return

    if "error" in query:
        print("Yahoo did not grant access. Start again.")
        return

    code = query.get("code", [""])[0]
    if not code:
        print("No authorization code found in that URL.")
        return

    token_parameters = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }

    request = Request(
        "https://api.login.yahoo.com/oauth2/get_token",
        data=urlencode(token_parameters).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            tokens = json.load(response)
    except HTTPError as error:
        print(f"Token exchange failed: HTTP {error.code}.")
        return

    if not tokens.get("access_token"):
        print("Yahoo did not return an access token.")
        return

    descriptor = os.open(
        TOKEN_FILE,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )
    with os.fdopen(descriptor, "w") as file:
        json.dump(tokens, file, indent=2)

    print("Success! Yahoo tokens saved to yahoo_tokens.json.")


if __name__ == "__main__":
    main()