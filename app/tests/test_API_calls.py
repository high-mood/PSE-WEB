import unittest

from app.utils import models
from app.tests.presets import UseTestSqlDB


class TestPlaylistAPI(UseTestSqlDB, unittest.TestCase):
    def test_pass(self):
        pass


class TestSongAPI(UseTestSqlDB, unittest.TestCase):
    def test_pass(self):
        pass


class TestTrackAPI(UseTestSqlDB, unittest.TestCase):
    def test_pass(self):
        pass


class TestUserAPI(UseTestSqlDB, unittest.TestCase):
    def test_pass(self):
        pass
