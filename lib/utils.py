from datetime import datetime

import numpy as np


def timestamp_to_seconds(timestamp):
    """Convert an ISO-ish timestamp to seconds-since-epoch."""
    return int(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z").strftime("%s"))


def find_oldest_timestamp(database):
    """Find the oldest-dated record in some TinyDB data."""
    if not database:
        return None

    return timestamp_to_seconds(
        sorted(database.all(), key=lambda x: x["start_date"])[0]["start_date"]
    )


def find_newest_timestamp(database):
    """Find the oldest-dated record in some TinyDB data."""
    if not database:
        return None

    return timestamp_to_seconds(
        sorted(database.all(), key=lambda x: x["start_date"])[-1]["start_date"]
    )


def centre_finder(points):
    """Find the centre of some points."""
    eastings = list(map(lambda x: x[0], points))
    northings = list(map(lambda x: x[1], points))

    return [np.median(northings), np.median(eastings)]
