"""Work with API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import exonetapi.RequestBuilder
from exonetapi.structures.ApiResourceIdentifier import ApiResourceIdentifier

if TYPE_CHECKING:
    from exonetapi.structures.ApiResourceSet import ApiResourceSet


class ApiResource(ApiResourceIdentifier):
    """Basic Resource with attributes."""

    def __init__(
        self, data_or_type: str | dict[str, Any], resource_id: str | None = None
    ) -> None:
        data = {}

        if type(data_or_type) is str:
            data["type"] = data_or_type
            data["id"] = resource_id
        elif type(data_or_type) is dict:
            data["type"] = data_or_type["type"]
            data["id"] = data_or_type.get("id")
        else:
            raise ValueError("First argument must be a string or dict.")

        # Call parent init method.
        super().__init__(data["type"], data["id"])

        self.__changed_attributes: list[str] = []
        self.__attributes: dict[str, Any] = {}

    def attribute(self, item: str, value: Any = None) -> Any:
        """Get Resource attributes if available.

        :param item: The name of the Resource attribute.
        :param value: The new value of the attribute.
        :return: The attribute or None when attribute does not exist.
        """
        if value is not None:
            self.__attributes[item] = value
            self.__changed_attributes.append(item)
            return self

        return self.__attributes.get(item)

    def attributes(self) -> dict[str, Any]:
        """Get all resource attributes.

        :return: All defined attributes in a dict.
        """
        return self.__attributes

    def to_json(self) -> dict[str, Any]:
        """Convert a Resource to a dict according to the JSON-API format.

        :return: The dict with attributes according to JSON-API spec.
        """
        json = {
            "type": self.type(),
            "attributes": self.attributes(),
        }

        if self.id():
            json["id"] = self.id()

        relationships = self.get_json_relationships()
        if relationships:
            json["relationships"] = relationships

        return json

    def to_json_changed_attributes(self) -> dict[str, Any]:
        """Convert the changed attributes to a dict according to the JSON-API format.

        :return: The dict with changed attributes according to JSON-API spec.
        """
        attributes = {}

        if len(self.__changed_attributes) == 0:
            return attributes

        for changed_attribute in self.__changed_attributes:
            attributes[changed_attribute] = self.attributes().get(changed_attribute)

        json = {
            "type": self.type(),
            "attributes": attributes,
        }

        if self.id():
            json["id"] = self.id()

        return json

    def to_json_resource_identifier(self) -> dict[str, Any]:
        """Convert a Resource to JSON, including only the type and ID.

        :return: A dict with the Resources type and ID.
        """
        return super().to_json()

    def patch(self) -> bool:
        return exonetapi.RequestBuilder(self.type()).patch(self)

    def post(
        self,
    ) -> ApiResource | ApiResourceSet | list[ApiResource | ApiResourceSet] | None:
        return exonetapi.RequestBuilder(self.type()).post(self)

    def delete(self) -> bool:
        return exonetapi.RequestBuilder(self.type()).delete(self)

    def reset_changed_attributes(self) -> Self:
        self.__changed_attributes = []
        return self
