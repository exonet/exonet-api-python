import unittest
from unittest.mock import MagicMock
from unittest import mock

from tests.testCase import testCase

from exonetapi.structures.ApiResource import ApiResource
from exonetapi import create_resource

import json


class testApiResource(testCase):

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

    def test_init_string(self):
        resource = ApiResource('fake', 'abc')
        resource.attribute('first_name', 'John')
        resource.attribute('last_name', 'Doe')

        self.assertEqual(resource.attribute('first_name'), 'John')
        self.assertEqual(resource.type(), 'fake')
        self.assertEqual(resource.id(), 'abc')
        self.assertEqual(resource.attributes(), {'first_name': 'John', 'last_name': 'Doe', })

    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            ApiResource(1234)

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
        resource = ApiResource({
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
                'attributes': {},
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

    def test_to_json_changed_attributes(self):
        resource = ApiResource({
            'type': 'fake',
            'id': 'FakeID',
        })
        self.assertEqual({}, resource.to_json_changed_attributes())

        resource.attribute('test', 'Hello World')
        resource.set_relationship(
            'thing',
            create_resource({
                'type': 'things',
                'id': 'thingID',
            })
        )

        self.assertEqual(
            json.dumps({"type": "fake", "attributes": {"test": "Hello World"}, "id": "FakeID"}),
            json.dumps(resource.to_json_changed_attributes())
        )

    @mock.patch('exonetapi.RequestBuilder.__init__', return_value=None)
    @mock.patch('exonetapi.RequestBuilder.patch')
    def test_patch(self, mock_requestbuilder_patch, mock_requestbuilder_init):
        mock_requestbuilder_patch.patch = MagicMock(return_value=None)
        ApiResource({'type': 'fake', 'id': 'FakeID'}).patch()
        mock_requestbuilder_init.assert_called_with('fake')

    @mock.patch('exonetapi.RequestBuilder.__init__', return_value=None)
    @mock.patch('exonetapi.RequestBuilder.delete')
    def test_delete(self, mock_requestbuilder_delete, mock_requestbuilder_init):
        mock_requestbuilder_delete.delete = MagicMock(return_value=None)
        ApiResource({'type': 'fake', 'id': 'FakeID'}).delete()
        mock_requestbuilder_init.assert_called_with('fake')

    @mock.patch('exonetapi.RequestBuilder.__init__', return_value=None)
    @mock.patch('exonetapi.RequestBuilder.post')
    def test_post(self, mock_requestbuilder_post, mock_requestbuilder_init):
        mock_requestbuilder_post.post = MagicMock(return_value=None)
        ApiResource({'type': 'fake', 'id': 'FakeID'}).post()
        mock_requestbuilder_init.assert_called_with('fake')

    def test_reset_changed_attributes(self):
        resource = ApiResource({
            'type': 'fake',
            'id': 'FakeID',
        })
        resource.attribute('test', 'Hello World')

        self.assertEqual(
            {'attributes': {'test': 'Hello World'}, 'id': 'FakeID', 'type': 'fake'},
            resource.to_json_changed_attributes()
        )

        resource.reset_changed_attributes()
        self.assertEqual({}, resource.to_json_changed_attributes())


if __name__ == '__main__':
    unittest.main()
