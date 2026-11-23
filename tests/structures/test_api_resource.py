import json
import unittest
from unittest import mock
from unittest.mock import MagicMock

import pytest

from exonetapi import create_resource
from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures.ApiResource import ApiResource
from tests.base import BaseTestCase


class TestApiResource(BaseTestCase):
    """Tests for the ApiResource."""

    def test_init(self) -> None:
        resource = create_resource(
            {
                "type": "fake",
            }
        )
        resource.attribute("first_name", "John")
        resource.attribute("last_name", "Doe")

        assert resource.attribute("first_name") == "John"
        assert resource.type() == "fake"
        assert resource.id() is None
        assert resource.attributes() == {"first_name": "John", "last_name": "Doe"}

    def test_init_string(self) -> None:
        resource = ApiResource("fake", "abc")
        resource.attribute("first_name", "John")
        resource.attribute("last_name", "Doe")

        assert resource.attribute("first_name") == "John"
        assert resource.type() == "fake"
        assert resource.id() == "abc"
        assert resource.attributes() == {"first_name": "John", "last_name": "Doe"}

    def test_init_invalid(self) -> None:
        with pytest.raises(ValueError, match="First argument must be a string or dict"):
            ApiResource(1234)

    def test_init_relationship(self) -> None:
        resource = create_resource(
            {
                "type": "fake",
            }
        )

        resource.set_relationship(
            "account",
            create_resource(
                {
                    "type": "account",
                    "id": "someAccountID",
                }
            ),
        )

        assert resource.get_json_relationships() == {
            "account": {"data": {"type": "account", "id": "someAccountID"}}
        }

    def test_set_relationship(self) -> None:
        resource = create_resource({"type": "fake"})

        resource.relationship(
            "messages",
            [
                create_resource({"type": "message", "id": "messageOne"}),
                create_resource({"type": "message", "id": "messageTwo"}),
            ],
        )

        assert resource.get_json_relationships() == {
            "messages": {
                "data": [
                    {"id": "messageOne", "type": "message"},
                    {"id": "messageTwo", "type": "message"},
                ]
            }
        }

    def test_to_json(self) -> None:
        resource = ApiResource(
            {
                "type": "fake",
                "id": "FakeID",
            }
        )
        resource.set_relationship(
            "thing",
            create_resource(
                {
                    "type": "things",
                    "id": "thingID",
                }
            ),
        )

        assert json.dumps(resource.to_json()) == json.dumps(
            {
                "type": "fake",
                "attributes": {},
                "id": "FakeID",
                "relationships": {
                    "thing": {"data": {"type": "things", "id": "thingID"}}
                },
            }
        )

    def test_to_json_changed_attributes(self) -> None:
        resource = ApiResource(
            {
                "type": "fake",
                "id": "FakeID",
            }
        )
        assert resource.to_json_changed_attributes() == {}

        resource.attribute("test", "Hello World")
        resource.set_relationship(
            "thing",
            create_resource(
                {
                    "type": "things",
                    "id": "thingID",
                }
            ),
        )

        assert json.dumps(
            {"type": "fake", "attributes": {"test": "Hello World"}, "id": "FakeID"}
        ) == json.dumps(resource.to_json_changed_attributes())

    @mock.patch.object(RequestBuilder, "__init__", return_value=None)
    @mock.patch.object(RequestBuilder, "patch")
    def test_patch(self, mock_requestbuilder_patch, mock_requestbuilder_init) -> None:
        mock_requestbuilder_patch.patch = MagicMock(return_value=None)
        ApiResource({"type": "fake", "id": "FakeID"}).patch()
        mock_requestbuilder_init.assert_called_with("fake")

    @mock.patch.object(RequestBuilder, "__init__", return_value=None)
    @mock.patch.object(RequestBuilder, "delete")
    def test_delete(self, mock_requestbuilder_delete, mock_requestbuilder_init) -> None:
        mock_requestbuilder_delete.delete = MagicMock(return_value=None)
        ApiResource({"type": "fake", "id": "FakeID"}).delete()
        mock_requestbuilder_init.assert_called_with("fake")

    @mock.patch.object(RequestBuilder, "__init__", return_value=None)
    @mock.patch.object(RequestBuilder, "post")
    def test_post(self, mock_requestbuilder_post, mock_requestbuilder_init) -> None:
        mock_requestbuilder_post.post = MagicMock(return_value=None)
        ApiResource({"type": "fake", "id": "FakeID"}).post()
        mock_requestbuilder_init.assert_called_with("fake")

    def test_reset_changed_attributes(self) -> None:
        resource = ApiResource(
            {
                "type": "fake",
                "id": "FakeID",
            }
        )
        resource.attribute("test", "Hello World")

        assert resource.to_json_changed_attributes() == {
            "attributes": {"test": "Hello World"},
            "id": "FakeID",
            "type": "fake",
        }

        resource.reset_changed_attributes()
        assert resource.to_json_changed_attributes() == {}


if __name__ == "__main__":
    unittest.main()
