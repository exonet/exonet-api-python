import unittest

from exonetapi.Client import Singleton


class BaseTestCase(unittest.TestCase):
    """Base test case that resets the Client singleton before every test."""

    def setUp(self) -> None:
        # Reset Client singleton.
        Singleton._instances = {}
