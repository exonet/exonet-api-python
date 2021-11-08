"""
Work with API resources.
"""
import exonetapi.RequestBuilder
from exonetapi.structures.ApiResourceIdentifier import ApiResourceIdentifier


class ApiResource(ApiResourceIdentifier):
    """Basic Resource with attributes.
    """
    def __init__(self, data_or_type, resource_id=None):
        data = dict()

        if type(data_or_type) is str:
            data['type'] = data_or_type
            data['id'] = resource_id
        elif type(data_or_type) is dict:
            data['type'] = data_or_type['type']
            data['id'] = data_or_type['id'] if 'id' in data_or_type else None
        else:
            raise ValueError("First argument must be a string or dict.")

        # Call parent init method.
        super().__init__(data['type'], data['id'])

        self.__changed_attributes = []
        self.__attributes = {}

    def attribute(self, item, value=None):
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

    def to_json_changed_attributes(self):
        """Convert the changed attributes of the resource to a dict according to
        the JSON-API format.

        :return: The dict with changed attributes according to JSON-API spec.
        """
        attributes = {}

        if len(self.__changed_attributes) == 0:
            return attributes

        for changed_attribute in self.__changed_attributes:
            attributes[changed_attribute] = self.attributes().get(changed_attribute)

        json = {
            'type': self.type(),
            'attributes': attributes,
        }

        if self.id():
            json['id'] = self.id()

        return json

    def to_json_resource_identifier(self):
        """Convert a Resource to JSON, including only the type and ID.

        :return: A dict with the Resources type and ID.
        """

        return super().to_json()

    def patch(self):
        return exonetapi.RequestBuilder(self.type()).patch(self)

    def post(self):
        return exonetapi.RequestBuilder(self.type()).post(self)

    def delete(self):
        return exonetapi.RequestBuilder(self.type()).delete(self)

    def reset_changed_attributes(self):
        self.__changed_attributes = []
        return self
