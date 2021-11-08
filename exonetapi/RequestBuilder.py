"""
Build requests to send to the API.
"""
import requests

from exonetapi.structures import ApiResourceSet
from exonetapi.exceptions.ValidationException import ValidationException
from .result import Parser


class RequestBuilder(object):
    """Create and make requests to the API.
    """

    def __init__(self, resource=None, client=None):
        if resource is not None and not resource.startswith('/'):
            resource = '/' + resource

        self.__resource = resource
        """
        The query params that will be used in the GET requests.
        Can contain filters and page options.
        """
        self.__query_params = {}

        if client:
            self.__client = client
        elif not hasattr(self, '__client'):
            from exonetapi import Client
            self.__client = Client()

    def filter(self, filter_name, filter_value):
        """Prepare this RequestBuilder to apply a filter on the next get request.
        :param filter_name: The name of the filter to apply.
        :param filter_value: The value of the applied filter.
        :return: self
        """
        self.__query_params['filter[' + filter_name + ']'] = filter_value
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

    def sort_asc(self, sort_field):
        """Prepare this RequestBuilder to sort by a field in ascending order.
        :param sort_field: The field name to sort on.
        :return: self
        """
        return self.sort(sort_field, 'asc')

    def sort_desc(self, sort_field):
        """Prepare this RequestBuilder to sort by a field in descending order.
        :param sort_field: The field name to sort on.
        :return: self
        """
        return self.sort(sort_field, 'desc')

    def get(self, identifier=None):
        """Make a call to the API using the previously set options.
        :param: identifier The optional identifier to get.
        :return: A Resource or a Collection of Resources.
        """

        response = self.__make_call(
            'GET',
            self.__build_url(identifier),
            params=self.__query_params if not identifier else None
        )

        return Parser(response.content).parse()

    def get_recursive(self):
        return self.__get_recursive()

    def post(self, resource):
        """Make a POST request to the API with the provided resource as data.

        :param resource: The resource to use as POST data.
        :return: A resource or a collection of resources.
        """
        changed_attributes = resource.to_json_changed_attributes()
        changed_relations = resource.get_json_changed_relationships()

        # If there are changed attributes, assume it s a new resource.
        if len(changed_attributes) > 0:
            response = self.__make_call('POST', self.__build_url(), {'data': resource.to_json()})

            return Parser(response.content).parse()

        # If there are changed relations and no changed attributes, assume a POST to the relation.
        if len(changed_relations) > 0:
            responses = []
            for relation_name in changed_relations:
                response = self.__make_call(
                    'POST',
                    '{}/relationships/{}'.format(self.__build_url(resource.id()), relation_name),
                    changed_relations[relation_name]
                )
                responses.append(Parser(response.content).parse())

            return responses

    def patch(self, resource):
        changed_attributes = resource.to_json_changed_attributes()
        changed_relations = resource.get_json_changed_relationships()

        # Patch changed attributes.
        if len(changed_attributes) > 0:
            self.__make_call(
                'PATCH',
                self.__build_url(resource.id()),
                {'data': changed_attributes}
            )

        # Patch changed relations.
        if len(changed_relations) > 0:
            for relation_name in changed_relations:
                self.__make_call(
                    'PATCH',
                    '{}/relationships/{}'.format(self.__build_url(resource.id()), relation_name),
                    changed_relations[relation_name]
                )

        return True

    def delete(self, resource):
        changed_relations = resource.get_json_changed_relationships()

        # If no relations are changed, DELETE the whole resource.
        if len(changed_relations) == 0:
            self.__make_call('DELETE', self.__build_url(resource.id()))

            return True

        for relation_name in changed_relations:
            self.__make_call(
                'DELETE',
                '{}/relationships/{}'.format(self.__build_url(resource.id()), relation_name),
                changed_relations[relation_name]
            )

        return True

    def __build_url(self, identifier=None):
        """Get the URL to call, based on all previously called setter methods.

        :return: A URL.
        """
        url = self.__client.get_host()

        if self.__resource is not None:
            url += self.__resource

        if identifier:
            url += '/' + identifier

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

    def __make_call(self, method, url, json_data=None, params=None):
        response = requests.request(
            method,
            url,
            headers=self.__get_headers(),
            json=json_data,
            params=params
        )

        # Handle validation errors.
        if response.status_code == 422:
            raise ValidationException(response)

        # Raise exception on failed request.
        response.raise_for_status()

        return response

    def __get_recursive(self, data=None, url=None):
        """
        Get the URL and call this method recursivly as long as there is an URL in the 'next' field
        of the 'links' data.

        :param data: The ApiResourceSet to append the resources to.
        :param url: The URL to call.
        :return: The ApiResourceSet containing all requested resources.
        """
        response = self.__make_call(
            'GET',
            url or self.__build_url(),
            params=self.__query_params if not url else None
        )

        content = Parser(response.content).parse()

        if data is None:
            data = ApiResourceSet()
            data.set_meta(content.meta().copy())

        data.add_resource(content.resources())

        next_link = content.links().get('next')
        if next_link is not None:
            return self.__get_recursive(data, next_link)

        return data
