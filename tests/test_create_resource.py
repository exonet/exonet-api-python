import unittest

from exonetapi.create_resource import create_resource


class testClient(unittest.TestCase):
    def test_create_resource(self):
        resource = create_resource.create_resource('test_resource')

        self.assertEqual(resource.__class__.__name__, 'TestResource')

if __name__ == '__main__':
    unittest.main()
