"""
Work with API resources.
"""
from inflection import underscore

from exonetapi.structures.ResourceIdentifier import ResourceIdentifier


class Resource(ResourceIdentifier):
    """Basic Resource with attributes.
    """

    def __init__(self, attributes, id=None):

        type = underscore(self.__class__.__name__)
        # Call parent init method.
        super().__init__(type, id)

        # The Resource attributes.
        self.__attributes = attributes`


    def attribute(self, item):
        """Get Resource attributes if available.

        :param item: The name of the Resource attribute.
        :return: The attribute or None when attribute does not exist.
        """
        return self.__attributes.get(item)

    def attributes(self):
        """Get all resource attributes.
        :return: All defined attributes in a dict.
        """
        return self.__attributes

    def relationship(self, name, *data):
        """Define a new relationship for this resource, replace an existing one or get an existing one.
        When data is provided the relationship is set, without data the relationship is returned.

        :param name: The name of the relation to set.
        :param data: The value of the relation, can be a Resource or a dict of Resources.
        :return: self when setting a relationship, or the actual relationship when getting it
        """
        if len(data) is 1:
            return self.set_relationship(name, data[0])

        return self.get_relationship(name)


    def to_json(self):
        """Convert a Resource to a dict according to the JSON-API format.

        :return: The dict with attributes according to JSON-API spec.
        """
        json = {
            'type': self.type(),
            'attributes': self.attributes(),

        }

        if self.__id:
            json['id'] = self.__id

        if self.__relationships:
            json['relationships'] = self.get_json_relationships()

        return json

    def to_json_resource_identifier(self):
        """Convert a Resource to JSON, including only the type and ID.

        :return: A dict with the Resources type and ID.
        """
        return {
            'type': self.type(),
            'id': self.__id,
        }

    def get_json_relationships(self):
        """Get a dict representing the relations for the resource in JSON-API format.

        :return: A dict with the relationships.
        """
        relationships = {}

        for relation_name, relation in self.__relationships.items():
            relationships[relation_name] = {}
            if type(relation) is list:
                relation_list = []
                for relation_resource in relation:
                    relation_list.append(relation_resource.to_json_resource_identifier())
                relationships[relation_name]['data'] = relation_list
            elif type(relation) is dict:
                relationships[relation_name]['data'] = relation['data']
            else:
                relationships[relation_name]['data'] = relation.to_json_resource_identifier()

        return relationships
