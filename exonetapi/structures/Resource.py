"""
Work with API resources.
"""

from exonetapi.structures.ResourceIdentifier import ResourceIdentifier


class Resource(ResourceIdentifier):
    """Basic Resource with attributes.
    """
    def __init__(self, data):
        # Call parent init method.
        super().__init__(
            data['type'],
            data['id'] if 'id' in data else None
        )

        self.__attributes = {}

    def attribute(self, item, value=None):
        """Get Resource attributes if available.

        :param item: The name of the Resource attribute.
        :param value: The new value of the attribute.
        :return: The attribute or None when attribute does not exist.
        """
        if value:
            self.__attributes[item] = value

        return self.__attributes.get(item)

    def attributes(self):
        """Get all resource attributes.
        :return: All defined attributes in a dict.
        """
        return self.__attributes

    def to_json(self):
        """Convert a Resource to a dict according to the JSON-API format.

        :return: The dict with attributes according to JSON-API spec.
        """
        json = {
            'type': self.type(),
            'attributes': self.attributes(),

        }

        if self.id():
            json['id'] = self.id()

        relationships = self.get_json_relationships()
        if relationships:
            json['relationships'] = relationships

        return json

    def to_json_resource_identifier(self):
        """Convert a Resource to JSON, including only the type and ID.

        :return: A dict with the Resources type and ID.
        """

        return super().to_json()

