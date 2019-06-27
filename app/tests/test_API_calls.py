import pytest
import unittest

from app.tests.data.influx import multiple_users
from app.tests.data.sql import multiple_songs
from app.tests.presets import UseTestInfluxDB, UseTestSqlDB

from flask_restplus import Resource

from app.API.track_calls import History, Metric
# from app.API.user_calls import


@pytest.mark.api_calls
class TestTracks(UseTestInfluxDB, UseTestSqlDB, unittest.TestCase):
    populate_influx_with = multiple_users
    populate_sql_with = multiple_songs

    def test_get_history(self):
        expected_output = {
            'resource':
                {
                    'userid': 'snipper',
                    'mean_excitedness': -0.30965299999999996,
                    'mean_happiness': 2.281719,
                    'songs': [
                        {
                            'songid': '0QXWfOuW9Nlk1DHuriQ47d',
                            'name': 'Solid As A Rock',
                            'time': '2019-06-24T10:57:20.282000128Z',
                            'excitedness': -0.298697,
                            'happiness': 0.429299
                        },
                        {
                            'songid': '3m7oq6mI87137pdj4MUS9i',
                            'name': 'Stay Bless',
                            'time': '2019-06-24T10:53:52.470000128Z',
                            'excitedness': 0.373746,
                            'happiness': 0.60425
                        },
                        {
                            'songid': '62aAUYl8nqio3kgth3sMzT',
                            'name': 'Not Because',
                            'time': '2019-06-24T10:49:15.564999936Z',
                            'excitedness': -0.384702,
                            'happiness': 1.24817
                        }
                    ]
                }
        }

        hist = History(Resource)
        self.assertDictEqual(hist.get('snipper', 3), expected_output)

    def test_get_metrics(self):
        expected_output = {}

        metr = Metric(Resource)

        print(metr.get('bulk', 3))

        self.assertDictEqual(metr.get('snipper', 3), expected_output)
