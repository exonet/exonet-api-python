import unittest
from unittest.mock import MagicMock
from unittest import mock

from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.auth.Authenticator import Authenticator
from exonetapi.result.Resource import Resource
from exonetapi.exceptions.ValidationException import ValidationException


class testRequestBuilder(unittest.TestCase):
    authenticator = Authenticator('https://test.url', '/auth/token')
    authenticator.get_token = MagicMock(return_value='test_token')

    request_builder = RequestBuilder('https://test.url', authenticator)

    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content
            self.status_code = status_code

        def raise_for_status(self):
            return None

    def test_init_arguments(self):
        self.assertEqual(self.request_builder._RequestBuilder__host, 'https://test.url')
        self.assertEqual(self.request_builder._RequestBuilder__authenticator, self.authenticator)

    def test_set_resource(self):
        self.request_builder.set_resource('/test')
        self.assertEqual(self.request_builder._RequestBuilder__resource_name, '/test')

    def test_id(self):
        self.request_builder.id('testId')
        self.assertEqual(self.request_builder._RequestBuilder__id, 'testId')

    def test_filter(self):
        self.request_builder.filter('firstFilterName', 'firstFilterValue')
        self.request_builder.filter('secondFilterName', 'secondFilterValue')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['filter[firstFilterName]'],
                         'firstFilterValue')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['filter[secondFilterName]'],
                         'secondFilterValue')

    def test_page(self):
        self.request_builder.page(3)
        self.assertEqual(self.request_builder._RequestBuilder__query_params['page[number]'], 3)

    def test_size(self):
        self.request_builder.size(30)
        self.assertEqual(self.request_builder._RequestBuilder__query_params['page[size]'], 30)

    def test_sort_default(self):
        self.request_builder.sort('domain')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['sort'], 'domain')

    def test_sortAsc(self):
        self.request_builder.sortAsc('domain')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['sort'], 'domain')

    def test_sortDesc(self):
        self.request_builder.sortDesc('domain')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['sort'], '-domain')

    def test_related(self):
        self.request_builder.related('relatedResource')
        self.assertEqual(self.request_builder._RequestBuilder__related, 'relatedResource')

    def test_build_url(self):
        self.request_builder.set_resource('testResource')
        self.request_builder.id('testId')
        self.request_builder.related('relatedResource')

        url = self.request_builder._RequestBuilder__build_url()
        self.assertEqual(url, 'https://test.url/testResource/testId/relatedResource')

    def test_get_headers(self):
        headers = self.request_builder._RequestBuilder__get_headers()
        self.assertEqual(headers, {
            'Accept': 'application/vnd.Exonet.v1+json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_token'
        })

    @mock.patch('exonetapi.result.Parser.parse')
    @mock.patch('exonetapi.result.Parser.__init__')
    @mock.patch('requests.get')
    def test_get(self, mock_requests_get, mock_parser_init, mock_parser_parse):
        mock_parser_parse.return_value = 'parsedReturnValue'
        mock_parser_init.return_value = None
        mock_requests_get.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.set_resource('test').related(None).id(None).get('testId')

        mock_requests_get.assert_called_with(
            'https://test.url/test/testId',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test_token'
            },
            params=None)

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual('parsedReturnValue', result)

    def test_get_without_resource_name(self):
        self.request_builder.set_resource(None).related(None).id(None)
        self.assertRaises(ValueError, self.request_builder.get)

    @mock.patch('exonetapi.result.Parser.parse')
    @mock.patch('exonetapi.result.Parser.__init__')
    @mock.patch('requests.post')
    def test_store(self, mock_requests_get, mock_parser_init, mock_parser_parse):
        resource = Resource('{"name": "test"}')
        resource.to_json = MagicMock(return_value={"name": "test"})

        mock_parser_parse.return_value = 'parsedReturnValue'
        mock_parser_init.return_value = None
        mock_requests_get.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.set_resource('test').related(None).id(None).store(resource)

        mock_requests_get.assert_called_with(
            'https://test.url/test',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test_token'
            },
            json={'data': {'name': 'test'}})

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual('parsedReturnValue', result)

    def test_store_without_resource_name(self):
        resource = Resource('{"name": "test"}')
        self.request_builder.set_resource(None).related(None).id(None)
        self.assertRaises(ValueError, self.request_builder.store, resource)

    @mock.patch('requests.post')
    @mock.patch('exonetapi.exceptions.ValidationException.__init__', return_value=None)
    def test_store_validation_error(self, mock_validation_exception, mock_requests_get):
        resource = Resource('{"name": "test"}')
        resource.to_json = MagicMock(return_value={"name": "test"})

        mock_requests_get.return_value = self.MockResponse('{"data": "getReturnData"}', 422)

        self.assertRaises(ValidationException, self.request_builder.store, resource)

        mock_requests_get.assert_called_with(
            'https://test.url/test',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test_token'
            },
            json={'data': {'name': 'test'}})


if __name__ == '__main__':
    unittest.main()
