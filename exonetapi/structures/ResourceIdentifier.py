"""
Work with API resources.
"""
from exonetapi.structures.Relation import Relation
from exonetapi.structures.Relationship import Relationship


class ResourceIdentifier(object):
    """Basic Resource identifier.
    """
    def __init__(self, type, id=None):
        # Keep track of the resource type.
        self.__type = type
        # Keep track of the resource id.
        self.__id = id

        self.__relationships = {}

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

    def related(self, name):
        """Define a new relation for the resource. Can be used to make new requests to the API.


        :param name: The name of the relation.
        :return Relation: The new relation.
        """
        return Relation(name, self.type(), self.id())

    def relationship(self, name, *data):
        """Define a new relationship for this resource, replace an existing one or get an
        existing one. When data is provided the relationship is set, without data the relationship
        is returned.

        :param name: The name of the relation to set.
        :param data: The value of the relation, can be a Resource or a dict of Resources.
        :return self: when setting a relationship, or the actual relationship when getting it
        """
        if len(data) is 1:
            return self.set_relationship(name, data[0])

        return self.get_relationship(name)

    def get_relationship(self, name):
        """Get a relationship for this resource.

        :param name: The name of the relation to get.
        :return: The defined relation or None
        """
        if not name in self.__relationships.keys():
            self.__relationships[name] = Relationship(name, self.type(), self.id())

        return self.__relationships[name]

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
        """Convert a ResourceIdentifier to JSON.

        :return: A dict with the resource type and ID.
        """
        return {
            'type': self.type(),
            'id': self.id(),
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
