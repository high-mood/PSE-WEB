import pytest
import unittest

from app.utils.influx import *

from influxdb.tests.server_tests.base import ManyTestCasesWithServerMixin
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

dummy_point = [  # some dummy points
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]


# TODO test this on linux
class TestSongs(ManyTestCasesWithServerMixin, unittest.TestCase):
    influxdb_template_conf = os.path.join(THIS_DIR, 'influxdb.conf.template')

    def test_write(self):
        """ Test write to the server. """
        self.assertIs(True, self.cli.write(
            {'points': dummy_point},
            params={'db': 'db'},
        ))

    def test_get_genres(self):
        pass
