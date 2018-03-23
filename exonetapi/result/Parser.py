"""
Create object from json resource.
"""
import json
from exonetapi.create_resource import create_resource


class Parser:
    """Parse API responses into Resources.
    Accepts JSON strings in the JSON-API format.
    """
    # The plain JSON as a string.
    __data = None
    # The parsed JSON data as a dict.
    __json_data = None

    def __init__(self, data):
        self.__data = data
        self.__json_data = json.loads(self.__data).get('data')

    def parse(self):
        """Parse JSON string into a Resource or a list of Resources.

        :return list|Resource: List with Resources or a single Resource.
        """
        if type(self.__json_data) is list:
            resources = []
            for resource_data in self.__json_data:
                resources.append(create_resource.create_resource(
                    resource_data.get('type'),
                    resource_data.get('attributes', {}),
                    resource_data.get('id'),
                    resource_data.get('relationships', {})
                ))

            return resources
        else:
            return create_resource.create_resource(
                self.__json_data.get('type'),
                self.__json_data.get('attributes', {}),
                self.__json_data.get('id'),
                self.__json_data.get('relationships', {})
            )
