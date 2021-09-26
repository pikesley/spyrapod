import json
from pathlib import Path
from unittest.case import TestCase

from support.helpers import nuke
from tinydb import Query, TinyDB

from lib.ride_enhancer import RideEnhancer, polyline_to_geojson


class TestRideEnhancer(TestCase):
    """Test the RideEnhancer."""

    def test_processing(self):
        """Test it updates the DB records."""
        nuke("tmp/test-data.json")
        database = TinyDB("tmp/test-data.json")
        database.insert(
            {
                "name": "With GeoJSON",
                "id": 1,
                "map": {"polyline": "abc123xyz"},
                "GeoJSON": {"type": "LineString", "coordinates": [[0, 0]]},
            }
        )
        database.insert(
            {
                "name": "Without GeoJSON",
                "id": 2,
                "map": {
                    "polyline": Path("tests/fixtures/polylines/vicky-park")
                    .read_text()
                    .strip()
                },
            }
        )
        fixture = json.loads(Path("tests/fixtures/GeoJSON/vicky-park.json").read_text())

        processor = RideEnhancer(database)
        processor.process()

        self.assertEqual(database.search(Query().id == 2)[0]["GeoJSON"], fixture)
        self.assertEqual(
            database.search(Query().id == 2)[0]["centre"],
            [51.53752, -0.039459999999999995],
        )


def test_polyline_to_geojson():
    """Test it converts a polyline to GeoJSON."""
    polyline = Path("tests/fixtures/polylines/vicky-park").read_text().strip()
    fixture = json.loads(Path("tests/fixtures/GeoJSON/vicky-park.json").read_text())
    assert polyline_to_geojson(polyline) == fixture
