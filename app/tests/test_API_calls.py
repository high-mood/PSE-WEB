"""
    test_API_calls.py
    ~~~~~~~~~~~~
    This file contains test for the API calls.

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

import pytest
import unittest

from app.tests.data.influx import multiple_users
from app.tests.data.sql import multiple_songs
from app.tests.presets import UseTestInfluxDB, UseTestSqlDB

from flask_restplus import Resource

from app.API.track_calls import History, TopSongs, Metric
from app.API.user_calls import HourlyMood, DailyMood


@pytest.mark.api_calls
class TestAPICalls(UseTestInfluxDB, UseTestSqlDB, unittest.TestCase):
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

    def test_get_hourly_mood(self):
        expected_output = {
            'resource':
                {
                    'userid': 'snipper',
                    'hours': [
                        {
                            'hour': '14',
                            'excitedness': 0.04745772222222222,
                            'happiness': 0.6015380333333336,
                            'acousticness': 0.265185,
                            'danceability': 0.7126111111111111,
                            'duration_ms': 215871.38888888888,
                            'energy': 0.5402222222222224,
                            'instrumentalness': 0.1268772433333333,
                            'key': 5.722222222222222,
                            'liveness': 0.21075555555555556,
                            'loudness': 0.0,
                            'mode': 0.6111111111111112,
                            'speechiness': 0.16409444444444443,
                            'tempo': 125.36200000000001,
                            'valence': 0.5524777777777778
                        },
                        {
                            'hour': '13',
                            'excitedness': 0.0,
                            'happiness': 0.04739899999999999,
                            'acousticness': 0.12324,
                            'danceability': 0.7436,
                            'duration_ms': 239181.46666666667,
                            'energy': 0.6091333333333335,
                            'instrumentalness': 0.07230773,
                            'key': 5.733333333333333,
                            'liveness': 0.19531333333333337,
                            'loudness': 0.0,
                            'mode': 0.4666666666666667,
                            'speechiness': 0.16362666666666664,
                            'tempo': 110.53093333333332,
                            'valence': 0.7540666666666667
                        }
                    ]
                }
        }

        hour = HourlyMood(Resource)
        self.assertDictEqual(hour.get('snipper', start=13, end=14), expected_output)

    def test_get_daily_mood(self):
        expected_output = {
           'resource':
               {
                  'userid': 'bulk',
                  'dates': [
                     {
                        'date': '2019-06-20',
                        'excitedness': 0.1321179142857143,
                        'happiness': 0.37893217465714296,
                        'acousticness': 0.1732328571428572,
                        'danceability': 0.6541142857142855,
                        'duration_ms': 195919.22857142857,
                        'energy': 0.7373999999999999,
                        'instrumentalness': 0.0681925857142857,
                        'key': 5.228571428571429,
                        'liveness': 0.17476857142857144,
                        'loudness': 0.0,
                        'mode': 0.5428571428571428,
                        'speechiness': 0.09494571428571429,
                        'tempo': 115.08668571428574,
                        'valence': 0.5423714285714285
                     }
                  ]
               }
        }

        day = DailyMood(Resource)
        self.assertDictEqual(day.get('bulk', day_count=1), expected_output)
