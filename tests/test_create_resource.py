import unittest

from exonetapi.create_resource import create_resource


class test_create_resource(unittest.TestCase):
    def test_create_resource(self):
        resource_data = {
            'type': 'test_resource'
        }

        resource = create_resource(resource_data)

        self.assertEqual(resource.__class__.__name__, 'TestResource')

if __name__ == '__main__':
    unittest.main()
