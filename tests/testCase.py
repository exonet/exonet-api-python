import unittest
from exonetapi.Client import Singleton

class testCase(unittest.TestCase):

    def setUp(self):
        # Reset Client singleton.
        Singleton._instances = {}
