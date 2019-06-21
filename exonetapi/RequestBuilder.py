"""
Build requests to send to the API.
"""
import requests
from urllib.parse import urlencode

from exonetapi.auth import Authenticator
from .result import Parser
from exonetapi.exceptions.ValidationException import ValidationException

class RequestBuilder():
# class RequestBuilder():
    """Create and make requests to the API.

    Takes care of Authentication, accessing resources and related data.
    """

    # The url to access the resource.
    __resource = None
    # An Authenticator instance to use when making requests to the API.
    __client = None

    # The query params that will be used in the GET requests. Can contain filters and page options.
    __query_params = {}

    def __init__(self, resource, client=None):
        self.__resource = resource

        if client:
            self.__client = client
        else:
            from exonetapi import Client
            self.__client = Client()


    def id(self, identifier):
        """Prepare this RequestBuilder to query an individual resource on the API.

        :param identifier: The ID of the resource to access.
        :return: self
        """


        # Make ResourceIdentifier

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
        """Prepare this RequestBuilder to sort by a field in ascending order.
        :param sort_field: The field name to sort on.
        :return: self
        """
        return self.sort(sort_field, 'asc')

    def sortDesc(self, sort_field):
        """Prepare this RequestBuilder to sort by a field in descending order.
        :param sort_field: The field name to sort on.
        :return: self
        """
        return self.sort(sort_field, 'desc')


    def get(self, identifier = None):
        """Make a call to the API using the previously set options.

        :return: A Resource or a Collection of Resources.
        """
        if not self.__resource:
            raise ValueError('Setting a resource is required before making a call.')

        response = requests.get(
            self.__build_url(),
            headers=self.__get_headers(),
            params=self.__query_params if not identifier else None
        )

        # Raise exception on failed request.
        response.raise_for_status()

        return Parser(response.content).parse()

    def store(self, resource):
        """Make a POST request to the API with the provided Resource as data.

        :param resource: The Resource to use as POST data.
        :return: A Resource or a Collection of Resources.
        """
        if not self.__resource:
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

    def __build_url(self, id=None):
        """Get the URL to call, based on all previously called setter methods.

        :return: A URL.
        """
        url = self.__client.get_host() + '/' + self.__resource

        if id:
            url += '/' + id

        return url

    def __get_headers(self):
        """Get the required headers to make an API request.

        :return: A dict with all the headers.
        """
        return {
            'Accept': 'application/vnd.Exonet.v1+json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % (self.__client.authenticator.get_token())
        }
