import pytest
import unittest

from app.utils.influx import *

dummy_point = [  # some dummy points
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]

cli = None
@pytest.fixture(autouse=True, scope="module")
def influx_setup(request):
    app.config['TESTING'] = True

    global cli
    cli = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'],
                         username=app.config['INFLUX_USER'], password=app.config['INFLUX_PASSWORD'])
    cli.create_database('test_db')
    cli.switch_database('test_db')

    request.addfinalizer(influx_teardown)


def influx_teardown():
    cli.drop_database('test_db')


class TestDB(unittest.TestCase):
    def test_write(self):
        """Test write to the server."""
        __import__('time').sleep(10)
        self.assertTrue(cli.write_points(dummy_point))
