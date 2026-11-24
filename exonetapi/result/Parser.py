"""Create object from json resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from exonetapi.create_resource import create_resource
from exonetapi.structures.ApiResourceIdentifier import ApiResourceIdentifier
from exonetapi.structures.ApiResourceSet import ApiResourceSet
from exonetapi.structures.Relationship import Relationship

if TYPE_CHECKING:
    from exonetapi.structures.ApiResource import ApiResource


class Parser:
    """Parse API responses into Resources.

    Accepts JSON strings in the JSON-API format.
    """

    def __init__(self, data: bytes) -> None:
        self.__data = data
        self.__json = json.loads(self.__data.decode())
        self.__json_data = self.__json.get("data")

    def parse(self) -> ApiResource | ApiResourceSet:
        """Parse JSON string into a ApiResource or a list of Resources.

        :return ApiResourceSet|ApiResource: An ApiResourceSet or a single ApiResource.
        """
        if type(self.__json_data) is list:
            resources = ApiResourceSet()
            resources.set_meta(self.__json.get("meta")).set_links(
                self.__json.get("links")
            )

            for resource_data in self.__json_data:
                resource = self.make_resource(resource_data)
                resources.add_resource(resource)

            return resources
        return self.make_resource(self.__json_data)

    def make_resource(self, resource_data: dict[str, Any]) -> ApiResource:
        resource = create_resource(
            {"type": resource_data["type"], "id": resource_data["id"]}
        )

        # Set attributes.
        if "attributes" in resource_data:
            for attribute_name, attribute_value in resource_data["attributes"].items():
                resource.attribute(attribute_name, attribute_value)

        resource.reset_changed_attributes()

        # Extract and parse all included relations.
        if "relationships" in resource_data:
            parsed_relations = self.parse_relations(
                resource_data["relationships"], resource.type(), resource.id()
            )

            for k, r in parsed_relations.items():
                resource.set_relationship(k, r)

        resource.reset_changed_relations()

        return resource

    def parse_relations(
        self,
        relationships: dict[str, Any] | None,
        origin_type: str,
        origin_id: str | None,
    ) -> dict[str, Relationship]:
        parsed_relations = {}

        if relationships:
            for relation_name, relation in relationships.items():
                # Set a relation
                if relation.get("data"):
                    relationship = Relationship(relation_name, origin_type, origin_id)

                    # Set a single relationship.
                    if "type" in relation["data"]:
                        relationship.set_resource_identifiers(
                            ApiResourceIdentifier(
                                relation["data"]["type"], relation["data"]["id"]
                            )
                        )

                    # Set a multi relationship.
                    elif isinstance(relation["data"], list):
                        identifiers = [
                            ApiResourceIdentifier(
                                relation_item["type"], relation_item["id"]
                            )
                            for relation_item in relation["data"]
                        ]

                        relationship.set_resource_identifiers(identifiers)

                    parsed_relations[relation_name] = relationship

        return parsed_relations
