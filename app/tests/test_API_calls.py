import pytest
import unittest

from app.tests.data.influx import multiple_users
from app.tests.data.sql import multiple_songs
from app.tests.presets import UseTestInfluxDB, UseTestSqlDB

from flask_restplus import Resource

from app.API.track_calls import History, TopSongs, Metric
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

    def test_get_top_song(self):
        expected_output = {
            'resource':
                {
                    'userid': 'snipper',
                    'songs': [
                        {
                            'songid': '0QXWfOuW9Nlk1DHuriQ47d',
                            'name': 'Solid As A Rock',
                            'excitedness': -0.298697,
                            'happiness': 0.429299
                        }
                    ]
                }
        }

        top = TopSongs(Resource)
        self.assertDictEqual(top.get('snipper', 1), expected_output)

    def test_get_metrics(self):
        expected_output = {
            'resource':
                {
                    'userid': 'bulk',
                    'metric_over_time': [
                        {
                            'songid': '2NyWdxhlqyrt91PE6Yzf9u',
                            'name': 'One Track Mind (feat. A$AP Rocky)',
                            'acousticness': 0.038,
                            'danceability': 0.364,
                            'duration_ms': 260609.0,
                            'energy': 0.46,
                            'instrumentalness': 0.00131,
                            'key': 0.0,
                            'liveness': 0.535,
                            'loudness': -8.298,
                            'mode': 1.0,
                            'speechiness': 0.0425,
                            'tempo': 93.129,
                            'valence': 0.068,
                            'excitedness': 2.05589,
                            'happiness': 0.735037
                        },
                        {
                            'songid': '69yfbpvmkIaB10msnKT7Q5',
                            'name': 'Radioactive',
                            'acousticness': 0.0386,
                            'danceability': 0.499,
                            'duration_ms': 276040.0,
                            'energy': 0.894,
                            'instrumentalness': 0.0,
                            'key': 9.0,
                            'liveness': 0.399,
                            'loudness': -3.887,
                            'mode': 1.0,
                            'speechiness': 0.267,
                            'tempo': 139.865,
                            'valence': 0.26,
                            'excitedness': -2.85417,
                            'happiness': 1.0746
                        }
                    ]
                }
        }

        metr = Metric(Resource)
        self.assertDictEqual(metr.get('bulk', 2), expected_output)
