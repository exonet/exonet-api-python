import unittest
from unittest.mock import MagicMock
from unittest import mock

from tests.testCase import testCase
from exonetapi import Client
from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures.Resource import Resource
from exonetapi.exceptions.ValidationException import ValidationException


class testRequestBuilder(testCase):
    def setUp(self):
        super().setUp()
        client = Client('https://test.url')
        self.request_builder = RequestBuilder('things', client)

    def tearDown(self):
        super().tearDown()
        self.request_builder = None

    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content
            self.status_code = status_code

        def raise_for_status(self):
            return None

    def test_init_arguments(self):
        self.assertEqual(self.request_builder._RequestBuilder__resource, '/things')

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

    def test_sort_invalid(self):
        self.assertRaises(ValueError, self.request_builder.sort, 'domain', 'topdown')

    def test_sortAsc(self):
        self.request_builder.sort_asc('domain')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['sort'], 'domain')

    def test_sortDesc(self):
        self.request_builder.sort_desc('domain')
        self.assertEqual(self.request_builder._RequestBuilder__query_params['sort'], '-domain')

    @mock.patch('exonetapi.auth.Authenticator.get_token')
    def test_get_headers(self, mock_authenticator_get_token):
        mock_authenticator_get_token.return_value = 'test_token'

        headers = self.request_builder._RequestBuilder__get_headers()
        self.assertEqual(headers, {
            'Accept': 'application/vnd.Exonet.v1+json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_token'
        })

    @mock.patch('exonetapi.result.Parser.parse')
    @mock.patch('exonetapi.result.Parser.__init__')
    @mock.patch('requests.request')
    def test_get(self, mock_requests_request, mock_parser_init, mock_parser_parse):
        mock_parser_parse.return_value = 'parsedReturnValue'
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.get('testId')

        mock_requests_request.assert_called_with(
            'GET',
            'https://test.url/things/testId',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            params=None,
            json=None)

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual('parsedReturnValue', result)

    @mock.patch('exonetapi.result.Parser.parse')
    @mock.patch('exonetapi.result.Parser.__init__')
    @mock.patch('requests.request')
    def test_store(self, mock_requests_request, mock_parser_init, mock_parser_parse):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.to_json = MagicMock(return_value={'name': 'my_name'})
        resource.to_json_changed_attributes = MagicMock(return_value={'name': 'my_name'})

        mock_parser_parse.return_value = 'parsedReturnValue'
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.store(resource)

        mock_requests_request.assert_called_with(
            'POST',
            'https://test.url/things',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'name': 'my_name'}},
            params=None)

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual('parsedReturnValue', result)

    @mock.patch('exonetapi.result.Parser.parse')
    @mock.patch('exonetapi.result.Parser.__init__')
    @mock.patch('requests.request')
    def test_store_relation(self, mock_requests_request, mock_parser_init, mock_parser_parse):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.get_json_changed_relationships = MagicMock(return_value={'name': {'data': {'type': 'test', 'id': 1}}})

        mock_parser_parse.return_value = 'parsedReturnValue'
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.store(resource)

        mock_requests_request.assert_called_with(
            'POST',
            'https://test.url/things/someId/relationships/name',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'type': 'test', 'id': 1}},
            params=None)

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual(['parsedReturnValue'], result)

    @mock.patch('requests.request')
    def test_patch(self, mock_requests_request):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.to_json = MagicMock(return_value={'name': 'my_name'})
        resource.to_json_changed_attributes = MagicMock(return_value={'name': 'my_name'})

        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.patch(resource)

        mock_requests_request.assert_called_with(
            'PATCH',
            'https://test.url/things/someId',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'name': 'my_name'}},
            params=None)

        self.assertTrue(result)

    @mock.patch('requests.request')
    def test_patch_relation(self, mock_requests_request):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.get_json_changed_relationships = MagicMock(return_value={'name': {'data': {'type': 'test', 'id': 1}}})

        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.patch(resource)

        mock_requests_request.assert_called_with(
            'PATCH',
            'https://test.url/things/someId/relationships/name',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'type': 'test', 'id': 1}},
            params=None)

        self.assertTrue(result)

    @mock.patch('requests.request')
    def test_delete(self, mock_requests_request):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.to_json = MagicMock(return_value={'name': 'my_name'})
        resource.to_json_changed_attributes = MagicMock(return_value={'name': 'my_name'})

        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.delete(resource)

        mock_requests_request.assert_called_with(
            'DELETE',
            'https://test.url/things/someId',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json=None,
            params=None)

        self.assertTrue(result)

    @mock.patch('requests.request')
    def test_delete_relation(self, mock_requests_request):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.get_json_changed_relationships = MagicMock(
            return_value={'name': {'data': {'type': 'test', 'id': 1}}})

        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}')

        result = self.request_builder.delete(resource)

        mock_requests_request.assert_called_with(
            'DELETE',
            'https://test.url/things/someId/relationships/name',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'type': 'test', 'id': 1}},
            params=None)

        self.assertTrue(result)

    @mock.patch('requests.request')
    @mock.patch('exonetapi.exceptions.ValidationException.__init__', return_value=None)
    def test_store_validation_error(self, mock_validation_exception, mock_requests_request):
        resource = Resource({'type': 'things', 'id': 'someId'})
        resource.to_json = MagicMock(return_value={'name': 'my_name'})
        resource.to_json_changed_attributes = MagicMock(return_value={'name': 'my_name'})

        mock_requests_request.return_value = self.MockResponse('{"data": "getReturnData"}', 422)

        self.assertRaises(ValidationException, self.request_builder.store, resource)

        mock_requests_request.assert_called_with(
            'POST',
            'https://test.url/things',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer None'
            },
            json={'data': {'name': 'my_name'}},
            params=None)


if __name__ == '__main__':
    unittest.main()
