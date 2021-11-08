"""
Create object from json resource.
"""
import json
from exonetapi.create_resource import create_resource
from exonetapi.structures import ApiResourceIdentifier, ApiResourceSet
from exonetapi.structures.Relationship import Relationship


class Parser:
    """Parse API responses into Resources.
    Accepts JSON strings in the JSON-API format.
    """

    def __init__(self, data):
        self.__data = data
        self.__json = json.loads(self.__data.decode())
        self.__json_data = self.__json.get('data')

    def parse(self):
        """Parse JSON string into a ApiResource or a list of Resources.

        :return ApiResourceSet|ApiResource: An ApiResourceSet or a single ApiResource.
        """
        if type(self.__json_data) is list:
            resources = ApiResourceSet()
            resources \
                .set_meta(self.__json.get('meta')) \
                .set_links(self.__json.get('links'))

            for resource_data in self.__json_data:
                resource = self.make_resource(resource_data)
                resources.add_resource(resource)

            return resources
        else:
            return self.make_resource(self.__json_data)

    def make_resource(self, resource_data):
        resource = create_resource({
            'type': resource_data['type'],
            'id': resource_data['id']
        })

        # Set attributes.
        if 'attributes' in resource_data.keys():
            for attribute_name, attribute_value in resource_data['attributes'].items():
                resource.attribute(attribute_name, attribute_value)

        resource.reset_changed_attributes()

        # Extract and parse all included relations.
        if 'relationships' in resource_data.keys():
            parsed_relations = self.parse_relations(
                resource_data['relationships'],
                resource.type(),
                resource.id()
            )

            for k, r in parsed_relations.items():
                resource.set_relationship(k, r)

        resource.reset_changed_relations()

        return resource

    def parse_relations(self, relationships, origin_type, origin_id):
        parsed_relations = {}

        if relationships:
            for relationName, relation in relationships.items():
                # Set a relation
                if ('data' in relation.keys()) and relation['data']:
                    relationship = Relationship(relationName, origin_type, origin_id)

                    # Set a single relationship.
                    if 'type' in relation['data']:
                        relationship.set_resource_identifiers(
                            ApiResourceIdentifier(relation['data']['type'], relation['data']['id'])
                        )

                    # Set a multi relationship.
                    elif isinstance(relation['data'], list):
                        relationships = []
                        for relationItem in relation['data']:
                            relationships.append(ApiResourceIdentifier(
                                relationItem['type'],
                                relationItem['id'])
                            )

                        relationship.set_resource_identifiers(relationships)

                    parsed_relations[relationName] = relationship

        return parsed_relations
