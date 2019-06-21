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

        self.assertEqual(len(User.get_all_users()), 1)

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
                 'excitedness': 10,
                 'happiness': 10}

    def test_add_song(self):
        Song.create_if_not_exist(self.song_info)
        self.assertEqual(Song.get_song_name(self.song_info['songid']), self.song_info['name'])

        Artist.create_if_not_exist(self.artist_info)

        Songmood.create_if_not_exist(self.mood_info)
        self.assertEqual(Songmood.get_moods(self.song_info['songid']), None)

        song_artist = {'songid': self.song_info['songid'],
                       'artistid': self.artist_info['artistid']}
        SongArtist.create_if_not_exist(song_artist)
