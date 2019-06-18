import pytest

from app import app


class ConfigException(Exception):
    pass


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


def test_get_features_moods():
    tracks = {
        '7zx0r1pcEiX92UwJ3MuNbV': {
            'name': 'The Concept of Love'
        },
        '7zmwcmjK7NIIiJXIkc072A': {
            'name': 'Keyboard Partita No. 4 in D Major, BWV 828: V. Sarabande'
        },
        '7yQYuDWHOcEwngp2cYmQkC': {
            'name': 'Seamonkey'
        }
    }
    print('works / 10')
