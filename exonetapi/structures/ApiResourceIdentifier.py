"""Work with API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import exonetapi.RequestBuilder
from exonetapi.structures.Relation import Relation
from exonetapi.structures.Relationship import Relationship

if TYPE_CHECKING:
    from exonetapi.structures.ApiResource import ApiResource
    from exonetapi.structures.ApiResourceSet import ApiResourceSet


class ApiResourceIdentifier:
    """Basic ApiResource identifier."""

    # The argument names are part of the public API, so they keep shadowing builtins.
    def __init__(self, type: str, id: str | None = None) -> None:  # noqa: A002
        """Initialize the resource.

        :param type: The type of the resource.
        :param id: The ID of the resource (optional).
        """
        # Keep track of the resource type.
        self.__type = type
        # Keep track of the resource id.
        self.__id = id

        self.__changed_relations: list[str] = []
        self.__relationships: dict[str, Any] = {}

    def type(self) -> str:
        """Get the resource type of this ApiResource instance.

        :return: The resource type.
        """
        return self.__type

    def id(self) -> str | None:
        """Get the resource id of this ApiResource instance.

        :return: The resource id.
        """
        return self.__id

    def get(self) -> ApiResource | ApiResourceSet:
        """Try to get the defined resource from the API.

        :return: A resource or a collection of resources.
        """
        return exonetapi.RequestBuilder(self.type()).get(self.id())

    def related(self, name: str) -> Relation:
        """Define a new relation for the resource.

        Can be used to make new requests to the API.

        :param name: The name of the relation.
        :return Relation: The new relation.
        """
        return Relation(name, self.type(), self.id())

    def relationship(self, name: str, *data: Any) -> Any:
        """Define, replace or get a relationship for this resource.

        When data is provided the relationship is set, without data the relationship
        is returned.

        :param name: The name of the relation to set.
        :param data: The value of the relation, can be a ApiResource or a dict
                     of Resources.
        :return self: when setting a relationship, or the actual relationship when
                      getting it
        """
        if len(data) == 1:
            return self.set_relationship(name, data[0])

        return self.get_relationship(name)

    def get_relationship(self, name: str) -> Any:
        """Get a relationship for this resource.

        :param name: The name of the relation to get.
        :return: The defined relation or None
        """
        if name not in self.__relationships:
            self.__relationships[name] = Relationship(name, self.type(), self.id())

        return self.__relationships[name]

    def set_relationship(self, name: str, data: Any) -> Self:
        """Define a new relationship for this resource or replace an existing one.

        Can be a relation to a single ApiResource or a dict of Resources.

        :param name: The name of the relation to set.
        :param data: The value of the relation, can be a ApiResource or a dict of
                     Resources.
        :return: self
        """
        self.__relationships[name] = data
        self.__changed_relations.append(name)

        return self

    def to_json(self) -> dict[str, Any]:
        """Convert a ApiResourceIdentifier to JSON.

        :return: A dict with the resource type and ID.
        """
        return {
            "type": self.type(),
            "id": self.id(),
        }

    def get_json_relationships(
        self, only_changed_relations: bool = False
    ) -> dict[str, dict[str, Any]]:
        """Get a dict representing the relations for the resource in JSON-API format.

        :return: A dict with the relationships.
        """
        relationships = {}

        for relation_name, relation in self.__relationships.items():
            if (
                only_changed_relations is True
                and relation_name not in self.__changed_relations
            ):
                continue

            relationships[relation_name] = {}
            if type(relation) is list:
                relation_list = []
                for relation_resource in relation:
                    try:
                        identifier = relation_resource.to_json_resource_identifier()
                    except AttributeError:
                        identifier = relation_resource.to_json()
                    relation_list.append(identifier)
                relationships[relation_name]["data"] = relation_list
            elif type(relation) is dict:
                relationships[relation_name]["data"] = relation["data"]
            else:
                try:
                    relationships[relation_name]["data"] = (
                        relation.to_json_resource_identifier()
                    )
                except AttributeError:
                    relationships[relation_name]["data"] = relation.to_json()

        return relationships

    def get_json_changed_relationships(self) -> dict[str, dict[str, Any]]:
        """Get the relationships that are changed.

        :return: A dict with the changed relationships.
        """
        return self.get_json_relationships(only_changed_relations=True)

    def reset_changed_relations(self) -> Self:
        """Empty the list of changed relations.

        :return self
        """
        self.__changed_relations = []
        return self
