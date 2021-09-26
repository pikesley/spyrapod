import json
import os
from urllib.parse import parse_qs, urlparse

import requests


class OauthDancer:
    """Class that does the tedious Oauth dance."""

    def __init__(self):
        """Construct."""
        self.client_id = os.environ["CLIENT_ID"]
        self.client_secret = os.environ["CLIENT_SECRET"]

    def dance(self):
        """Do the work."""
        self.get_auth_code()
        self.get_token()

    @property
    def url(self):
        """Construct the initial URL."""
        url = "http://www.strava.com/oauth/authorize?"
        url += f"client_id={self.client_id}&"
        url += "response_type=code&"
        url += "redirect_uri=http://localhost/exchange_token&"
        url += "approval_prompt=force&scope=activity:read_all"

        return url

    def get_auth_code(self):
        """Get the intermediate auth code."""
        print("Open this in a browser, where you're logged-in to Strava")
        print()
        print(f"  {self.url}")
        print()

        self.redirect_url = input(
            "capture the URL to which you're redirected, and paste it here: "
        )

        self.authorisation_code = parse_qs(urlparse(self.redirect_url).query)["code"][0]

    def get_token(self):
        """Get the actually-useful access-token."""
        headers = {"Accept": "application/json"}

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.authorisation_code,
            "grant_type": "authorization_code",
        }

        response = requests.post(
            "https://www.strava.com/oauth/token", headers=headers, params=params
        )

        self.token = json.loads(response.text)["access_token"]

    @property
    def headers(self):
        """Assemble the request headers."""
        return {"Accept": "application/json", "Authorization": f"Bearer {self.token}"}
