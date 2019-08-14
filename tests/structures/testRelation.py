import unittest
from unittest import mock

from tests.testCase import testCase

from exonetapi.structures.Relation import Relation


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
    def test_getattr(self, mock_request_builder):
        """Call a method on the relation and expect it to be passed to the RequestBuilder."""
        relation = Relation('author', 'posts', 'postID')

        self.assertEqual('get_response', relation.get())
        mock_request_builder.assert_called()


if __name__ == '__main__':
    unittest.main()
