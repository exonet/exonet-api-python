import unittest

from tests.testCase import testCase

from exonetapi.structures.Resource import Resource
from exonetapi import create_resource

import json


class testResource(testCase):

    def test_init(self):
        resource = create_resource({
            'type': 'fake',
        })
        resource.attribute('first_name', 'John')
        resource.attribute('last_name', 'Doe')

        self.assertEqual(resource.attribute('first_name'), 'John')
        self.assertEqual(resource.type(), 'fake')
        self.assertIsNone(resource.id())
        self.assertEqual(resource.attributes(), {'first_name': 'John', 'last_name': 'Doe', })

    def test_init_relationship(self):
        resource = create_resource({
            'type': 'fake',
        })

        resource.set_relationship(
            'account',
            create_resource({
                'type': 'account',
                'id': 'someAccountID',
            })
        )

        self.assertEqual(resource.get_json_relationships(), {
            'account': {'data': {'type': 'account', 'id': 'someAccountID'}}
        })

    def test_set_relationship(self):
        resource = create_resource({
            'type': 'fake'
        })

        resource.relationship('messages', [
            create_resource({
                'type': 'message',
                'id': 'messageOne'
            }),
            create_resource({
                'type': 'message',
                'id': 'messageTwo'
            })
        ])

        self.assertEqual(resource.get_json_relationships(), {
            'messages': {'data': [
                {'id': 'messageOne', 'type': 'message'},
                {'id': 'messageTwo', 'type': 'message'}
            ]}
        })

    def test_to_json(self):
        resource = Resource({
            'type': 'fake',
            'id': 'FakeID',
        })
        resource.set_relationship(
            'thing',
            create_resource({
                'type': 'things',
                'id': 'thingID',
            })
        )

        self.assertEqual(
            json.dumps(resource.to_json()),
            json.dumps({
                'type': 'fake',
                'attributes': { },
                'id': 'FakeID',
                'relationships': {
                    'thing': {
                        'data': {
                            'type': 'things',
                            'id': 'thingID'
                        }
                    }
                }
            })
        )


if __name__ == '__main__':
    unittest.main()
