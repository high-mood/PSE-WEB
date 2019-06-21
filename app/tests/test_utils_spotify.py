import pytest

from app import app
from app.utils import spotify


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


def test_timeout():
    refresh_token = "AQDMxiy5GuPy55xDpV60tzUpUu06GZKGLRZMKu8gIdORUoSPFPQJ1N-qwudJC_yoIeX_xLbK8iNb7rE3vy9T1DmFiAoaV_-5qLx5hzA1BmcJ0RNAW4WhgC-ROZs4CIe_15vWUA"
    access_token = spotify.get_access_token(refresh_token)
    spotify.get_recently_played(access_token)
