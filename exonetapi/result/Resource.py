"""
Work with API resources.
"""
from inflection import underscore


class Resource:
    """Basic Resource with attributes.
    """

    def __init__(self, attributes, id=None, relationships=None):
        # Keep track of the resource type.
        self.__type = underscore(self.__class__.__name__)
        # The Resource attributes.
        self.__attributes = attributes
        # Keep track of the resource id.
        self.__id = id

        # The relationships for this resource.
        if relationships:
            self.__relationships = relationships
        else :
            self.__relationships = {}

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

    def get_relationship(self, name):
        """Get a relationship for this resource.

        :param name: The name of the relation to get.
        :return: The defined relation or None
        """

        if name in self.__relationships:
            return self.__relationships[name]

        return None

    def set_relationship(self, name, data):
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
