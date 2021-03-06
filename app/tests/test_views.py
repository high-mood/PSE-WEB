"""
    test_views.py
    ~~~~~~~~~~~~
    This file contains test for loading the web page.

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
    assert b"Your Spotify usage analysed and visualised" in rv.data


@pytest.mark.integration_test
def test_user_page(client):
    with client.session_transaction() as sess:
        sess['json_info'] = {'id': "1115081075",
                             'refresh_token': models.User.get_refresh_token('1115081075'),
                             'display_name': "Test Mood"}
    rv = client.get('/')

    assert b"1115081075" in rv.data
