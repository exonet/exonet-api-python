from inflection import camelize
from .structures.Resource import Resource


def create_resource(resource):
    """Create a dynamic Resource based on the type that is provided in the data.

    :param resource: The resource.
    :return: A Resource instance.
    """
    resource_type = resource['type']

    return type(camelize(resource_type), (Resource,), {})(resource)
