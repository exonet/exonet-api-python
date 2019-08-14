import unittest

from tests.testCase import testCase

from exonetapi.structures.Resource import Resource
from exonetapi.structures.Relationship import Relationship
from exonetapi.structures.Relation import Relation
from exonetapi import create_resource

import json


class testResourceIdentifier(testCase):

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

    def test_get_relationship_create(self):
        resource = create_resource({
            'type': 'fake',
        })

        relationship = resource.get_relationship('something')
        self.assertIsInstance(relationship, Relationship)

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

    def test_get_json_relationships(self):
        resource = create_resource({
            'type': 'fake'
        })

        resource.relationship('messages', {
            'data' : {
                'type': 'this',
                'id': 'that',
            }
        })

        self.assertEqual(
            resource.get_json_relationships(),
            {
                'messages': {
                    'data': {
                        'id': 'that',
                        'type': 'this'
                    }
                }
            }
        )

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

    def test_related(self):
        resource = create_resource({
            'type': 'fake',
        })

        relation = resource.related('something')
        self.assertIsInstance(relation, Relation)


if __name__ == '__main__':
    unittest.main()
