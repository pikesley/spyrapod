import json
from pathlib import Path
from unittest import TestCase

import httpretty
from support.helpers import nuke
from tinydb import TinyDB

from lib.strava_client import StravaClient, StravaClientException


class TestStravaClient(TestCase):
    """Test the StravaClient."""

    def test_summary_fetcher(self):
        """Testing whether the client can parse some JSON but OK."""
        nuke("tmp/test-data.json")
        fake_db = TinyDB("tmp/test-data.json")

        fixture = Path("tests/fixtures/athlete/activities.json").read_text()
        client = StravaClient("FAKETOKEN", database=fake_db)
        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/athlete/activities",
            body=fixture,
        )

        summary = client.fetch_summary()
        self.assertEqual(summary, json.loads(fixture))

    def test_activity_fetcher(self):
        """Test it saves an activity."""
        nuke("tmp/test-data.json")
        fake_db = TinyDB("tmp/test-data.json")

        fixture = Path("tests/fixtures/activities/654321.json").read_text()
        client = StravaClient("PHONYTOKEN", database=fake_db)

        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/activities/654321",
            body=fixture,
        )

        client.fetch_activity(654321)

        self.assertEqual(len(fake_db.all()), 1)
        self.assertEqual(list(map(lambda x: x["id"], fake_db.all())), [654321])

    def test_activites_fetcher(self):
        """Test it finds all the activities."""
        nuke("tmp/test-data.json")
        fake_db = TinyDB("tmp/test-data.json")
        client = StravaClient("PHONYTOKEN", database=fake_db)

        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/athlete/activities",
            body=Path("tests/fixtures/athlete/activities.json").read_text(),
        )

        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/activities/654321",
            body=Path("tests/fixtures/activities/654321.json").read_text(),
        )

        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/activities/765432",
            body=Path("tests/fixtures/activities/765432.json").read_text(),
        )

        client.fetch_activities()

        self.assertEqual(len(fake_db.all()), 2)
        self.assertEqual(list(map(lambda x: x["id"], fake_db.all())), [654321, 765432])

    def test_populate(self):
        """Test it backfills correctly."""
        database = TinyDB("tests/fixtures/dbs/dates-data.json")
        client = StravaClient("PHONYTOKEN", database=database)

        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99"
            "&before=1577836800",
            body="{}",
        )

        client.populate()

        self.assertEqual(len(httpretty.latest_requests()), 1)
        self.assertEqual(
            httpretty.last_request().url,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99"
            "&before=1577836800",
        )

    def test_populate_from_scratch(self):
        """Test it backfills correctly with no initial data."""
        nuke("tmp/test-data.json")
        database = TinyDB("tmp/test-data.json")
        client = StravaClient("PHONYTOKEN", database=database)

        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99",
            body="{}",
        )

        client.populate()

        self.assertEqual(len(httpretty.latest_requests()), 1)
        self.assertEqual(
            httpretty.last_request().url,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99",
        )

    def test_refresh(self):
        """Test it tops-up the newest data."""
        database = TinyDB("tests/fixtures/dbs/dates-data.json")
        client = StravaClient("PHONYTOKEN", database=database)

        httpretty.enable(verbose=True, allow_net_connect=False)
        httpretty.reset()
        httpretty.register_uri(
            httpretty.GET,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99"
            "&after=1609459200",
            body="{}",
        )

        client.refresh()

        self.assertEqual(len(httpretty.latest_requests()), 1)
        self.assertEqual(
            httpretty.last_request().url,
            "https://www.strava.com/api/v3/athlete/activities?per_page=99"
            "&after=1609459200",
        )

    def test_bad_refresh(self):
        """Test it rejects an attempt to refresh when there's no data."""
        nuke("tmp/test-data.json")
        database = TinyDB("tmp/test-data.json")
        client = StravaClient("PHONYTOKEN", database=database)

        with self.assertRaises(StravaClientException) as sce:
            client.refresh()

        self.assertEqual(
            str(sce.exception), "Cannot refresh on an empty DB, try `populate` instead"
        )
