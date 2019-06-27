import unittest

from app.tests.presets import UseTestInfluxDB
from app.utils import influx

# some dummy points
k3_album = [
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:47:35Z",
        "fields": {
            "songid": "035czDmDakmsSlElgid5d9"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:51:23Z",
        "fields": {
            "songid": "6obJhxyLxEFlNOiqPKVR8i"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:52:19Z",
        "fields": {
            "songid": "2qJ5tIxB6mWfpo4M5DVvL6"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:55:25Z",
        "fields": {
            "songid": "19rmEKeQCsaYGI1g25i31N"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:57:48Z",
        "fields": {
            "songid": "37xPKDIqDyEbA0H0WSJkG0"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T10:59:03Z",
        "fields": {
            "songid": "25fL1tT0LaVABsNZhEln3Y"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:01:38Z",
        "fields": {
            "songid": "75NnpgZNv1iB2TMdklmUd1"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:01:59Z",
        "fields": {
            "songid": "035czDmDakmsSlElgid5d9"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:02:58Z",
        "fields": {
            "songid": "3lXERsaFCXB7dOLvwchzYh"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:05:03Z",
        "fields": {
            "songid": "2xtnke3OyEf3fzUVeEQ8nK"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:06:53Z",
        "fields": {
            "songid": "7i7DXixL0LFTiT4kWyBwuQ"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:09:43Z",
        "fields": {
            "songid": "77I3MCqxMx4IbMwiVhiH9T"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:12:23Z",
        "fields": {
            "songid": "588LZ5fQ4PW4BVyILiNpFN"
        }
    },
    {
        "measurement": "test_user",
        "time": "2019-03-12T11:15:42",
        "fields": {
            "songid": "7A6cA4hdbjj7OERuUWdZw4"
        }
    }
]


class TestSongs(UseTestInfluxDB, unittest.TestCase):
    populate_influx_with = k3_album

    def test_get_top_songs(self):
        self.assertEqual(influx.get_top_songs(self.cli, 'test_user', 1), [("035czDmDakmsSlElgid5d9", 2)])
