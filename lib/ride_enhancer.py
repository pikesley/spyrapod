import json
import logging
import subprocess
import sys

from tinydb import Query

from lib.utils import centre_finder

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class RideEnhancer:
    """Add some additional metadata."""

    def __init__(self, database):
        """Construct."""
        self.database = database

    def process(self):
        """Process the data."""
        self.generate_geojson()
        self.add_centres()

    def generate_geojson(self):
        """Convert polylines to GeoJSON points."""
        for item in self.database.all():
            if "GeoJSON" not in item.keys():
                logging.info("Generating GeoJSON for %s...", item["id"])
                self.database.upsert(
                    {"GeoJSON": polyline_to_geojson(item["map"]["polyline"])},
                    Query().id == item["id"],
                )

    def add_centres(self):
        """Add a median centre to each ride."""
        for item in self.database.all():
            if "centre" not in item.keys():
                logging.info("Adding `centre` to %s...", item["id"])
                self.database.upsert(
                    {"centre": centre_finder(item["GeoJSON"]["coordinates"])},
                    Query().id == item["id"],
                )


def polyline_to_geojson(polyline):
    """Convert Strava polyline to GeoJSON points."""
    command = "polyline --toGeoJSON".split(" ")
    child_process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    stdout = child_process.communicate(polyline.encode(encoding="UTF-8"))
    pairs = json.loads(stdout[0].decode())
    inverted_pairs = list(map(lambda x: [x[1], x[0]], pairs))

    return {"type": "LineString", "coordinates": inverted_pairs}
