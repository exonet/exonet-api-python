import unittest
from unittest.mock import MagicMock
from unittest import mock

from tests.testCase import testCase

from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.auth.Authenticator import Authenticator
from exonetapi.structures.Relation import Relation
from exonetapi.exceptions.ValidationException import ValidationException
from exonetapi import create_resource

import json


class testRelation(testCase):

    def test_len_empty(self):
        relation = Relation('author', 'posts', 'postID')

        self.assertEqual(0, len(relation))

    def test_len_filled(self):
        relation = Relation('author', 'posts', 'postID')
        relation.set_resource_identifiers([
            'a', 'b', 'c'
        ])

        self.assertEqual(3, len(relation))

    @mock.patch('exonetapi.RequestBuilder.get', return_value='get_response')
    def test_getattr(self, mock_requestBuilder):
        """Call a method on the relation and expect it to be passed to the RequestBuilder."""
        relation = Relation('author', 'posts', 'postID')

        self.assertEqual('get_response', relation.get())
        mock_requestBuilder.assert_called()


if __name__ == '__main__':
    unittest.main()
