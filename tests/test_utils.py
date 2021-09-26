from tinydb import TinyDB

from lib.utils import (
    centre_finder,
    find_newest_timestamp,
    find_oldest_timestamp,
    timestamp_to_seconds,
)


def test_timestamp_to_seconds():
    """Test it converts times correctly."""
    assert timestamp_to_seconds("1970-01-01T00:00:00Z") == 0
    assert timestamp_to_seconds("2020-10-18T11:12:54Z") == 1603019574
    assert timestamp_to_seconds("2038-01-19T03:14:07Z") == 2147483647


def test_find_oldest_timestamp():
    """Test it finds the oldest data."""
    database = TinyDB("tests/fixtures/dbs/dates-data.json")
    assert find_oldest_timestamp(database) == 1577836800


def test_find_newest_timestamp():
    """Test it finds the newest data."""
    database = TinyDB("tests/fixtures/dbs/dates-data.json")
    assert find_newest_timestamp(database) == 1609459200

    assert find_newest_timestamp(None) is None


def test_center_finder():
    """Test it finds the centre of a single ride."""
    ride = [-19.0, 51.0], [-1.0, 48.0], [-1.0, 45.0], [-1.5, 48.0]
    assert centre_finder(ride) == [48.0, -1.25]
