from inflection import camelize
from .result.Resource import Resource

class create_resource:
    def create_resource(resource_type, attributes=(), id=None, relationships=None):
        """Create a dynamic Resource based on the type that is provided in the data.

        :param resource_type: The resource type.
        :param attributes: The json data to construct a Resource.
        :param id: The Resource identifier.
        :param relationships: The initial relationships for the resource.
        :return: A Resource instance.
        """
        return type(camelize(resource_type), (Resource,), {})(attributes=attributes, id=id, relationships=relationships)
