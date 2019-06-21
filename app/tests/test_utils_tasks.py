import pytest
import unittest

from app import app, db
from app.utils import tasks


@pytest.fixture(autouse=True, scope="module")
def db_setup(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True

    db.create_all()

    request.addfinalizer(db_teardown)


def db_teardown():
    db.session.remove()
    db.drop_all()


class MoodsTest(unittest.TestCase):
    def test_get_features_moods(self):
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

        tasks.get_features_moods(tracks)
