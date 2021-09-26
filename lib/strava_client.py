import json
import logging
import sys

import requests
from tinydb import TinyDB

from lib.utils import find_newest_timestamp, find_oldest_timestamp

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class StravaClient:
    """Talks to Strava."""

    def __init__(self, token, database=None):
        """Construct."""
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.params = {"per_page": 99}

        self.database_path = "/data/tiny-data/rides.json"
        self.database = TinyDB(self.database_path)

        if database is not None:
            self.database = database

    def fetch_activities(self):
        """Fetch all the activities from the `summary`."""
        summary = self.fetch_summary()
        if not summary:
            logging.info("Nothing to do")
        for item in summary:
            self.fetch_activity(item["id"])

    def fetch_summary(self):
        """Fetch a list of activities."""
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=self.headers,
            params=self.params,
        )

        validate_response(response)
        return json.loads(response.text)

    def fetch_activity(self, activity_id):
        """Fetch an individual activity."""
        logging.info("Getting activity %s... ", activity_id)
        url = f"https://www.strava.com/api/v3/activities/{activity_id}"
        response = requests.get(url, headers=self.headers)
        validate_response(response)

        self.database.insert(json.loads(response.text))

    def populate(self):
        """Backfill historical data."""
        self.params["before"] = find_oldest_timestamp(self.database)

        self.fetch_activities()

        del self.params["before"]

    def refresh(self):
        """Collect the latest data."""
        if not self.database.all():
            raise StravaClientException(
                "Cannot refresh on an empty DB, try `populate` instead"
            )
        self.params["after"] = find_newest_timestamp(self.database)

        self.fetch_activities()

        del self.params["after"]


def validate_response(response):  # nocov
    """Check we get a 200."""
    if not response.status_code == 200:
        logging.error("Error %s... ", response.status_code)
        logging.error(response.text)
        sys.exit()


class StravaClientException(Exception):
    """Custom exception."""
