import pytest

from app import app


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


def test_main_page(client):
    rv = client.get('/')
    assert b'LOGGED OUT' in rv.data
