"""
Work with API resources.
"""
from inflection import underscore


class Resource:
    """Basic Resource with attributes.
    """
    # Keep track of the resource type.
    __type = None
    # Keep track of the resource id.
    __id = None
    # The Resource attributes.
    __attributes = {}

    # The relationships for this resource.
    __relationships = {}

    def __init__(self, attributes, id=None, relationships=None):
        self.__type = underscore(self.__class__.__name__)
        self.__attributes = attributes
        self.__id = id

        if relationships:
            self.__relationships = relationships

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

    def type(self):
        """Get the resource type of this Resource instance.

        :return: The resource type.
        """
        return self.__type

    def id(self):
        """Get the resource id of this Resource instance.

        :return: The resource id.
        """
        return self.__id

    def relationship(self, name, data):
        """Define a new relationship for this resource or replace an existing one.
        Can be a relation to a single Resource or a dict of Resources.

        :param name: The name of the relation to set.
        :param data: The value of the relation, can be a Resource or a dict of Resources.
        :return: self
        """

        self.__relationships[name] = data

        return self

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
