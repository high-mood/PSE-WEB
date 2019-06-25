import pytest

from app import app
from app.utils import models


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


@pytest.mark.integration_test
def test_main_page(client):
    rv = client.get('/')
    assert b"Welcome to Highmood" in rv.data


@pytest.mark.integration_test
def test_user_page(client):
    with client.session_transaction() as sess:
        sess['json_info'] = {'id': "1115081075",
                             'refresh_token': models.User.get_refresh_token('1115081075'),
                             'display_name': "Test Mood"}
    rv = client.get('/')

    assert b"Welcome Test Mood (1115081075), Here's your mood" in rv.data
