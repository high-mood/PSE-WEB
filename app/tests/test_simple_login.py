import pytest

from app import app


class ConfigException(Exception):
    pass


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


def test_debug_mode(client):
    if app.config['DEBUG']:
        raise ConfigException("Build should not be in DEBUG mode.")


def test_main_page(client):
    rv = client.get('/')
    assert b"LOGGED OUT" in rv.data


def test_user_page(client):
    with client.session_transaction() as sess:
        sess['json_info'] = {'id': "1115081075", 'refresh_token': "AQDMxiy5GuPy55xDpV60tzUpUu06GZKGLRZMKu8gIdORUoSPFPQJ1N-qwudJC_yoIeX_xLbK8iNb7rE3vy9T1DmFiAoaV_-5qLx5hzA1BmcJ0RNAW4WhgC-ROZs4CIe_15vWUA",
                             'display_name': "Stan van den Broek"}
    rv = client.get('/')

    assert b"Welcome Stan van den Broek, Here's your mood" in rv.data