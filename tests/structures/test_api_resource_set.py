import unittest
from unittest import mock

from exonetapi.structures.ApiResourceSet import ApiResourceSet
from exonetapi.structures.ApiResource import ApiResource
from tests.testCase import testCase


class testApiResourceSet(testCase):

    def test_total(self):
        api_resource_set = ApiResourceSet()
        meta = {'resources': {'total': 1337}}
        api_resource_set.set_meta(meta)

        self.assertEqual(1337, api_resource_set.total())
        self.assertEqual(meta, api_resource_set.meta())

    def test_links(self):
        links = {
            'next': 'next_link',
            'prev': 'prev_link'
        }
        api_resource_set = ApiResourceSet()
        api_resource_set.set_links(links)

        self.assertEqual(links, api_resource_set.links())

    @mock.patch('exonetapi.RequestBuilder.get', return_value='api_response')
    def test_pagination(self, mock_request_builder):
        links = {
            'next': 'https://api.exonet.nl/next_url?filter[unit]=test',
            'prev': 'https://api.exonet.nl/prev_url?filter[unit]=test',
            'first': 'https://api.exonet.nl/first/url?filter[unit]=test',
            'last': 'https://api.exonet.nl/last/url?filter[unit]=test&last=true',
        }
        api_resource_set = ApiResourceSet()
        api_resource_set.set_links(links)

        self.assertEqual('api_response', api_resource_set.next_page())
        mock_request_builder.assert_called_with('next_url?filter[unit]=test')

        self.assertEqual('api_response', api_resource_set.previous_page())
        mock_request_builder.assert_called_with('prev_url?filter[unit]=test')

        self.assertEqual('api_response', api_resource_set.first_page())
        mock_request_builder.assert_called_with('first/url?filter[unit]=test')

        self.assertEqual('api_response', api_resource_set.last_page())
        mock_request_builder.assert_called_with('last/url?filter[unit]=test&last=true')

        api_resource_set.set_links({'next': None})
        self.assertEqual(None, api_resource_set.next_page())

    def test_add_resource(self):
        resource_one = ApiResource('fake', 'abc')
        resource_two = ApiResource('fake', 'def')

        api_resource_set = ApiResourceSet()
        api_resource_set.add_resource(resource_one)
        api_resource_set.add_resource([resource_two])

        self.assertEqual(2, len(api_resource_set))

        for api_resource in api_resource_set:
            self.assertTrue(api_resource.id() is 'abc' or api_resource.id() is 'def')

        for api_resource in api_resource_set.resources():
            self.assertTrue(api_resource.id() is 'abc' or api_resource.id() is 'def')


if __name__ == '__main__':
    unittest.main()
