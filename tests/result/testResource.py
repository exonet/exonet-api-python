import unittest
from unittest.mock import MagicMock
from unittest import mock

from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.auth.Authenticator import Authenticator
from exonetapi.result.Resource import Resource
from exonetapi.exceptions.ValidationException import ValidationException
from exonetapi.create_resource import create_resource

import json


class testResource(unittest.TestCase):
    # authenticator = Authenticator('https://test.url', '/auth/token')
    # authenticator.get_token = MagicMock(return_value='test_token')
    #
    # request_builder = RequestBuilder('https://test.url', authenticator)
    #
    # class MockResponse:
    #     def __init__(self, content, status_code=200):
    #         self.content = content
    #         self.status_code = status_code
    #
    #     def raise_for_status(self):
    #         return None

    def test_init(self):
        resource = create_resource.create_resource(
            'fake',
            attributes={
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )

        self.assertEqual(resource.attribute('first_name'), 'John')
        self.assertEqual(resource.type(), 'fake')
        self.assertIsNone(resource.id())
        self.assertEqual(resource.attributes(), {'first_name': 'John', 'last_name': 'Doe', })

    def test_init_relationship(self):
        resource = create_resource.create_resource(
            'fake',
            attributes={
                'first_name': 'John',
                'last_name': 'Doe',
            },
            relationships={
                'account': create_resource.create_resource('account', id='someAccountID')
            }
        )

        self.assertEqual(resource.get_json_relationships(), {
            'account': {'data': {'type': 'account', 'id': 'someAccountID'}}
        })

    def test_set_relationship(self):
        resource = create_resource.create_resource(
            'fake',
            attributes={
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )

        resource.relationship('messages', [
            create_resource.create_resource('message', id='messageOne'),
            create_resource.create_resource('message', id='messageTwo')
        ])

        self.assertEqual(resource.get_json_relationships(), {
            'messages': {'data': [
                {'id': 'messageOne', 'type': 'message'},
                {'id': 'messageTwo', 'type': 'message'}
            ]}
        })

    def test_to_json(self):
        resource = create_resource.create_resource(
            'fake',
            id='FakeID',
            attributes={
                'first_name': 'John'
            },
            relationships={
                'thing': create_resource.create_resource('things', id='thingID')
            }
        )

        self.assertEqual(
            json.dumps(resource.to_json()),
            json.dumps({
                'type': 'fake',
                'attributes': {
                    'first_name': 'John'
                },
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

    def test_get_json_relationships(self):
        resource = create_resource.create_resource(
            'fake',
            relationships={
                'thing': {
                    'data' : {
                        'type': 'things',
                        'id' : 'thingID'
                    }
                }
            }
        )

        self.assertEqual(
            json.dumps(resource.get_json_relationships()),
            json.dumps(
                {
                    'thing': {
                        'data': {
                            'type': 'things',
                            'id': 'thingID'
                        }
                    }
                }
            )
        )


if __name__ == '__main__':
    unittest.main()
