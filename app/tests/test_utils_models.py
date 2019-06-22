import pytest
import unittest

from app import app, db
from app.utils.models import User, Song, Artist, Songmood, SongArtist

from datetime import datetime


@pytest.fixture(autouse=True, scope="module")
def db_setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True

    db.create_all()

    request.addfinalizer(db_teardown)


def db_teardown():
    db.session.remove()
    db.drop_all()


class TestUsers(unittest.TestCase):
    user_info = {'id': '112',
                 'email': "such_email@email.com",
                 'display_name': "Test user",
                 'image_url': None,
                 'birthdate': datetime.now().strftime("%Y-%m-%d"),
                 'country': "Earth",
                 'product': True,
                 'refresh_token': "refresh_token",
                 'user_is_active': True}

    def test_add_user(self):
        User.create_if_not_exist(self.user_info, self.user_info['refresh_token'])

        self.assertIn(self.user_info['id'], User.get_all_users())

    def test_add_user_again(self):
        User.create_if_not_exist(self.user_info, self.user_info['refresh_token'])

        self.assertEqual(User.get_all_tokes(), [self.user_info['refresh_token']])
        self.assertEqual(User.get_all_users(), [self.user_info['id']])

    def test_refresh_token(self):
        self.assertEqual(User.get_refresh_token(self.user_info['id']), self.user_info['refresh_token'])


class TestSongs(unittest.TestCase):
    song_info = {'songid': "6obJhxyLxEFlNOiqPKVR8i",
                 'name': "Oya lélé",
                 'duration_ms': 224946,
                 'key': 2,
                 'mode': 1,
                 'time_signature': 4,
                 'acousticness': 0.00479,
                 'danceability': 0.669,
                 'energy': 0.903,
                 'instrumentalness': 0.0,
                 'liveness': 0.32,
                 'loudness': -6.012,
                 'speechiness': 0.0564,
                 'valence': 0.882,
                 'tempo': 135.041}

    artist_info = {'artistid': "1eZrOVQ8ady3sDTNdG9E4D",
                   'name': "K3",
                   'genres': "belgian pop, dutch pop, dutch rock",
                   'popularity': 60}

    mood_info = {'songid': "6obJhxyLxEFlNOiqPKVR8i",
                 'excitedness': 10.0,
                 'happiness': 10.0,
                 'response_excitedness': 10.0,
                 'response_happiness': 10.0,
                 'response_count': 20}

    @staticmethod
    def _row_to_dict(row):
        sql_dict = dict(row.__dict__)
        sql_dict.pop('_sa_instance_state', None)

        return sql_dict

    def test_add_song(self):
        Song.create_if_not_exist(self.song_info)
        self.assertEqual(Song.get_song_name(self.song_info['songid']), self.song_info['name'])

        Artist.create_if_not_exist(self.artist_info)

        Songmood.create_if_not_exist(self.mood_info)
        moods = filter(lambda row: row.songid == self.song_info['songid'],
                       Songmood.get_moods([self.mood_info['songid']]))
        self.assertDictEqual(self._row_to_dict(next(moods)), self.mood_info)

        song_artist = {'songid': self.song_info['songid'],
                       'artistid': self.artist_info['artistid']}
        SongArtist.create_if_not_exist(song_artist)

    def test_update_mood(self):
        Songmood.update_response_mood(self.song_info['songid'], 5.0, 5.0)
        self.assertAlmostEqual(Songmood.get_moods([self.mood_info['songid']])[0].response_excitedness, 9.7, delta=0.1)
        self.assertAlmostEqual(Songmood.get_moods([self.mood_info['songid']])[0].response_happiness, 9.7, delta=0.1)
