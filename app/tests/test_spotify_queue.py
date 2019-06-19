import pytest

from app import app
from app.API import spotify as api


@pytest.fixture
def client():
    client = app.test_client()
    app.config['testing'] = True

    yield client


def test_timeout():
    refresh_token = "AQDMxiy5GuPy55xDpV60tzUpUu06GZKGLRZMKu8gIdORUoSPFPQJ1N-qwudJC_yoIeX_xLbK8iNb7rE3vy9T1DmFiAoaV_-5qLx5hzA1BmcJ0RNAW4WhgC-ROZs4CIe_15vWUA"
    access_token = api.get_access_token(refresh_token)
    for i in range(100):
        api.get_recently_played(access_token)
