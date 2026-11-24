import json
import unittest
from unittest import mock
from unittest.mock import MagicMock

from exonetapi import create_resource
from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures import ApiResourceIdentifier
from exonetapi.structures.ApiResource import ApiResource
from exonetapi.structures.Relation import Relation
from exonetapi.structures.Relationship import Relationship
from tests.base import BaseTestCase


class TestApiResourceIdentifier(BaseTestCase):
    """Tests for the ApiResourceIdentifier."""

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

    def test_get_relationship_create(self) -> None:
        resource = create_resource(
            {
                "type": "fake",
            }
        )

        relationship = resource.get_relationship("something")
        assert isinstance(relationship, Relationship)

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

    def test_get_json_relationships(self) -> None:
        resource = create_resource({"type": "fake"})
        resource.relationship(
            "ignored",
            {
                "data": {
                    "type": "this",
                    "id": "that",
                }
            },
        )
        resource.reset_changed_relations()

        resource.relationship("object", {"data": {"type": "this", "id": "that"}})
        resource.relationship("resource", ApiResource("this", "that"))
        resource.relationship(
            "resource_identifier", ApiResourceIdentifier("this", "that")
        )
        resource.relationship("list", [ApiResourceIdentifier("this", "that")])

        assert resource.get_json_changed_relationships() == {
            "object": {"data": {"id": "that", "type": "this"}},
            "resource": {"data": {"id": "that", "type": "this"}},
            "resource_identifier": {"data": {"id": "that", "type": "this"}},
            "list": {"data": [{"id": "that", "type": "this"}]},
        }

    def test_get_json_changed_relationships(self) -> None:
        resource = create_resource({"type": "fake"})

        resource.relationship(
            "messages",
            {
                "data": {
                    "type": "this",
                    "id": "that",
                }
            },
        )

        assert resource.get_json_changed_relationships() == {
            "messages": {"data": {"id": "that", "type": "this"}}
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

    def test_related(self) -> None:
        resource = create_resource(
            {
                "type": "fake",
            }
        )

        relation = resource.related("something")
        assert isinstance(relation, Relation)

    @mock.patch.object(RequestBuilder, "__init__", return_value=None)
    @mock.patch.object(RequestBuilder, "get")
    def test_post(self, mock_requestbuilder_get, mock_requestbuilder_init) -> None:
        mock_requestbuilder_get.get = MagicMock(return_value=None)
        ApiResource({"type": "fake", "id": "FakeID"}).get()
        mock_requestbuilder_get.assert_called_with("FakeID")
        mock_requestbuilder_init.assert_called_with("fake")


if __name__ == "__main__":
    unittest.main()
