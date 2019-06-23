import pytest

from app import app
from app.utils import spotify, models


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


def test_timeout():
    refresh_token = models.User.get_all_tokes()[0]
    access_token = spotify.get_access_token(refresh_token)
    spotify.get_recently_played(access_token)
