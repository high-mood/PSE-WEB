import pytest

from app import app
from app.utils import models


@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True

    yield client


@pytest.mark.integration_test
def test_something(client):
    pass
