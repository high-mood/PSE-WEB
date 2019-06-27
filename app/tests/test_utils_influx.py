"""
    test_utils_influx.py
    ~~~~~~~~~~~~
    This file contains test for the influx database data flow.

    :copyright: 2019 Moodify (High-Mood)
    :authors:
           "Stan van den Broek",
           "Mitchell van den Bulk",
           "Mo Diallo",
           "Arthur van Eeden",
           "Elijah Erven",
           "Henok Ghebrenigus",
           "Jonas van der Ham",
           "Mounir El Kirafi",
           "Esmeralda Knaap",
           "Youri Reijne",
           "Siwa Sardjoemissier",
           "Barry de Vries",
           "Jelle Witsen Elias"
"""

import unittest

from app.tests.data.influx import k3_album
from app.tests.presets import UseTestInfluxDB
from app.utils import influx


class TestSongs(UseTestInfluxDB, unittest.TestCase):
    populate_influx_with = k3_album

    def test_get_top_songs(self):
        self.assertEqual(influx.get_top_songs(self.cli, 'test_user', 1), [("035czDmDakmsSlElgid5d9", 2)])
