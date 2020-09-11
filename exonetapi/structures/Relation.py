class Relation(object):
    # string Pattern to create the relation url.
    __urlPattern = '/%s/%s/%s'

    def __init__(self, relation_name, origin_type, origin_id):
        """Relation constructor.

        :param str relation_name: The name of the relation.
        :param str origin_type: The resource type of the origin resource.
        :param str origin_id: The resource ID of the origin resource.
        """
        self.__name = relation_name
        self.__url = self.__urlPattern % (origin_type, origin_id, relation_name)

        # ApiResourceSet|ApiResourceIdentifier The related resource identifier or a ApiResourceSet.
        self.__resourceIdentifiers = None

        from exonetapi import RequestBuilder
        self.__request = RequestBuilder(self.__url)

    def __len__(self):
        if self.__resourceIdentifiers:
            return len(self.__resourceIdentifiers)

        return 0

    def __getattr__(self, name):
        def method():
            return getattr(self.__request, name)()

        return method

    def get_resource_identifiers(self):
        """
        Get the resource identifiers for this relation.

        :return ApiResourceSet|ApiResourceIdentifier: The resource identifier or a resource set.
        """
        return self.__resourceIdentifiers

    def set_resource_identifiers(self, new_relationship):
        """
        Replace the related resource identifiers with new data.

        :param ApiResourceSet|ApiResourceIdentifier new_relationship: A new resource identifier or a
        new resource set.
        :return self:
        """
        self.__resourceIdentifiers = new_relationship

        return self
