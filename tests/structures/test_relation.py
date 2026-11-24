import unittest
from unittest import mock

from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures.Relation import Relation
from tests.base import BaseTestCase


class TestRelation(BaseTestCase):
    """Tests for the Relation."""

    def test_len_empty(self) -> None:
        relation = Relation("author", "posts", "postID")

        assert len(relation) == 0

    def test_len_filled(self) -> None:
        relation = Relation("author", "posts", "postID")
        relation.set_resource_identifiers(["a", "b", "c"])

        assert len(relation) == 3

    @mock.patch.object(RequestBuilder, "get", return_value="get_response")
    def test_getattr(self, mock_request_builder) -> None:
        """Pass a method call on the relation on to the RequestBuilder."""
        relation = Relation("author", "posts", "postID")

        assert relation.get() == "get_response"
        mock_request_builder.assert_called()


if __name__ == "__main__":
    unittest.main()
