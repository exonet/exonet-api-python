"""
Build requests to send to the API.
"""
import requests
from urllib.parse import urlencode

from .result import Parser
from exonetapi.exceptions.ValidationException import ValidationException


class RequestBuilder:
    """Create and make requests to the API.

    Takes care of Authentication, accessing resources and related data.
    """
    # The API host.
    __host = None
    # An Authenticator instance to use when making requests to the API.
    __authenticator = None

    def __init__(self, host, authenticator):
        self.__host = host
        self.__authenticator = authenticator

        # The resource name to access.
        self.__resource_name = None
        # Optional resource ID.
        self.__id = None
        # Optional related resources name.
        self.__related = None
        # The query params that will be used in the GET requests. Can contain filters and page options.
        self.__query_params = {}

    def set_resource(self, resource_name):
        """Prepare this RequestBuilder to query a specific resource.

        :param resource_name: The resource type name.
        :return: self
        """
        self.__resource_name = resource_name
        return self

    def id(self, identifier):
        """Prepare this RequestBuilder to query an individual resource on the API.

        :param identifier: The ID of the resource to access.
        :return: self
        """
        self.__id = identifier
        return self

    def filter(self, filter_name, filter_value):
        """Prepare this RequestBuilder to apply a filter on the next get request.
        :param filter_name: The name of the filter to apply.
        :param filter_value: The value of the applied filter.
        :return: self
        """
        self.__query_params['filter['+filter_name+']'] = filter_value
        return self

    def page(self, page_number):
        """Prepare this RequestBuilder to get a specific page.
        :param page_number: The page number.
        :return: self
        """
        self.__query_params['page[number]'] = page_number
        return self

    def size(self, page_size):
        """Prepare this RequestBuilder to apply a page size limit.
        :param page_size: The maximum number of returned resources.
        :return: self
        """
        self.__query_params['page[size]'] = page_size
        return self

    def sort(self, sort_field, sort_order='asc'):
        """Prepare this RequestBuilder to sort by a field.
        :param sort_field: The field name to sort on.
        :param sort_order: The order for sorting (asc/desc), default: asc.
        :return: self
        """
        if sort_order not in ['asc', 'desc']:
            raise ValueError('Sort order can only be "asc" or "desc".')

        self.__query_params['sort'] = '{sort}{field}'.format(
            sort='-' if sort_order == 'desc' else '',
            field=sort_field,
        )
        return self

    def sortAsc(self, sort_field):
        return self.sort(sort_field, 'asc')

    def sortDesc(self, sort_field):
        return self.sort(sort_field, 'desc')

    def related(self, related):
        """Prepare this RequestBuilder to query related resources on the API.

        :param related: The name of the relationship to get resources for.
        :return: self
        """
        self.__related = related
        return self

    def get(self, identifier = None):
        """Make a call to the API using the previously set options.

        :return: A Resource or a Collection of Resources.
        """
        if not self.__resource_name:
            raise ValueError('Setting a resource is required before making a call.')

        # Set the resource ID if an identifier was provided.
        if identifier:
            self.id(identifier)

        response = requests.get(
            self.__build_url(),
            headers=self.__get_headers(),
            params=self.__query_params if not self.__id else None
        )

        # Raise exception on failed request.
        response.raise_for_status()

        return Parser(response.content).parse()

    def store(self, resource):
        """Make a POST request to the API with the provided Resource as data.

        :param resource: The Resource to use as POST data.
        :return: A Resource or a Collection of Resources.
        """
        if not self.__resource_name:
            raise ValueError('Setting a resource is required before making a call.')

        response = requests.post(
            self.__build_url(),
            headers=self.__get_headers(),
            json={'data': resource.to_json()}
        )

        # Handle validation errors.
        if response.status_code == 422:
            raise ValidationException(response)

        # Raise exception on failed request.
        response.raise_for_status()

        return Parser(response.content).parse()

    def __build_url(self):
        """Get the URL to call, based on all previously called setter methods.

        :return: A URL.
        """
        url = self.__host + '/' + self.__resource_name

        if self.__id:
            url += '/' + self.__id

        if self.__related:
            url += '/' + self.__related

        return url

    def __get_headers(self):
        """Get the required headers to make an API request.

        :return: A dict with all the headers.
        """
        return {
            'Accept': 'application/vnd.Exonet.v1+json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % (self.__authenticator.get_token())
        }
