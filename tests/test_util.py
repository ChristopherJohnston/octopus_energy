from octopus_energy_client import iso_format
import unittest
import mock
import responses
import requests
import datetime
import pytz

class TestClient(unittest.TestCase):
    def test_iso_format(self):
        dt = datetime.datetime(2022, 1, 1, 15, 23, 13, tzinfo=pytz.utc)
        self.assertEqual(iso_format(dt), "2022-01-01T15:23:13Z")