import unittest
from unittest.mock import MagicMock
from unittest import mock

from requests import Response

from tests.testCase import testCase
from exonetapi import Client
from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures.ApiResource import ApiResource
from exonetapi.exceptions.ValidationException import ValidationException


class testRequestBuilder(testCase):
    def setUp(self):
        super().setUp()
        client = Client("https://api.exonet.nl")
        self.request_builder = RequestBuilder("things", client)

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
        self.assertEqual(self.request_builder._RequestBuilder__resource, "/things")

    def test_filter(self):
        self.request_builder.filter("firstFilterName", "firstFilterValue")
        self.request_builder.filter("secondFilterName", "secondFilterValue")
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params[
                "filter[firstFilterName]"
            ],
            "firstFilterValue",
        )
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params[
                "filter[secondFilterName]"
            ],
            "secondFilterValue",
        )

    def test_page(self):
        self.request_builder.page(3)
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params["page[number]"], 3
        )

    def test_size(self):
        self.request_builder.size(30)
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params["page[size]"], 30
        )

    def test_sort_default(self):
        self.request_builder.sort("domain")
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params["sort"], "domain"
        )

    def test_sort_invalid(self):
        self.assertRaises(ValueError, self.request_builder.sort, "domain", "topdown")

    def test_sortAsc(self):
        self.request_builder.sort_asc("domain")
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params["sort"], "domain"
        )

    def test_sortDesc(self):
        self.request_builder.sort_desc("domain")
        self.assertEqual(
            self.request_builder._RequestBuilder__query_params["sort"], "-domain"
        )

    @mock.patch("exonetapi.auth.Authenticator.Authenticator.get_token")
    def test_get_headers(self, mock_authenticator_get_token):
        mock_authenticator_get_token.return_value = "test_token"

        headers = self.request_builder._RequestBuilder__get_headers()
        self.assertEqual(
            headers,
            {
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token",
            },
        )

    @mock.patch("exonetapi.result.Parser.Parser.parse")
    @mock.patch("exonetapi.result.Parser.Parser.__init__")
    @mock.patch("requests.request")
    def test_get(self, mock_requests_request, mock_parser_init, mock_parser_parse):
        mock_parser_parse.return_value = "parsedReturnValue"
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.get("testIad")

        mock_requests_request.assert_called_with(
            "GET",
            "https://api.exonet.nl/things/testIad",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            params=None,
            json=None,
        )

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual("parsedReturnValue", result)

    @mock.patch("exonetapi.result.Parser.Parser.parse")
    @mock.patch("exonetapi.result.Parser.Parser.__init__")
    @mock.patch("requests.request")
    def test_post(self, mock_requests_request, mock_parser_init, mock_parser_parse):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.to_json = MagicMock(return_value={"name": "my_name"})
        resource.to_json_changed_attributes = MagicMock(
            return_value={"name": "my_name"}
        )

        mock_parser_parse.return_value = "parsedReturnValue"
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.post(resource)

        mock_requests_request.assert_called_with(
            "POST",
            "https://api.exonet.nl/things",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"name": "my_name"}},
            params=None,
        )

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual("parsedReturnValue", result)

    @mock.patch("exonetapi.result.Parser.Parser.parse")
    @mock.patch("exonetapi.result.Parser.Parser.__init__")
    @mock.patch("requests.request")
    def test_post_relation(
        self, mock_requests_request, mock_parser_init, mock_parser_parse
    ):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.get_json_changed_relationships = MagicMock(
            return_value={"name": {"data": {"type": "test", "id": 1}}}
        )

        mock_parser_parse.return_value = "parsedReturnValue"
        mock_parser_init.return_value = None
        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.post(resource)

        mock_requests_request.assert_called_with(
            "POST",
            "https://api.exonet.nl/things/someId/relationships/name",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"type": "test", "id": 1}},
            params=None,
        )

        mock_parser_init.assert_called_with('{"data": "getReturnData"}')

        self.assertTrue(mock_parser_parse.called)
        self.assertEqual(["parsedReturnValue"], result)

    @mock.patch("requests.request")
    def test_patch(self, mock_requests_request):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.to_json = MagicMock(return_value={"name": "my_name"})
        resource.to_json_changed_attributes = MagicMock(
            return_value={"name": "my_name"}
        )

        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.patch(resource)

        mock_requests_request.assert_called_with(
            "PATCH",
            "https://api.exonet.nl/things/someId",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"name": "my_name"}},
            params=None,
        )

        self.assertTrue(result)

    @mock.patch("requests.request")
    def test_patch_relation(self, mock_requests_request):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.get_json_changed_relationships = MagicMock(
            return_value={"name": {"data": {"type": "test", "id": 1}}}
        )

        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.patch(resource)

        mock_requests_request.assert_called_with(
            "PATCH",
            "https://api.exonet.nl/things/someId/relationships/name",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"type": "test", "id": 1}},
            params=None,
        )

        self.assertTrue(result)

    @mock.patch("requests.request")
    def test_delete(self, mock_requests_request):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.to_json = MagicMock(return_value={"name": "my_name"})
        resource.to_json_changed_attributes = MagicMock(
            return_value={"name": "my_name"}
        )

        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.delete(resource)

        mock_requests_request.assert_called_with(
            "DELETE",
            "https://api.exonet.nl/things/someId",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json=None,
            params=None,
        )

        self.assertTrue(result)

    @mock.patch("requests.request")
    def test_delete_relation(self, mock_requests_request):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.get_json_changed_relationships = MagicMock(
            return_value={"name": {"data": {"type": "test", "id": 1}}}
        )

        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}'
        )

        result = self.request_builder.delete(resource)

        mock_requests_request.assert_called_with(
            "DELETE",
            "https://api.exonet.nl/things/someId/relationships/name",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"type": "test", "id": 1}},
            params=None,
        )

        self.assertTrue(result)

    @mock.patch("requests.request")
    @mock.patch("exonetapi.exceptions.ValidationException.ValidationException.__init__", return_value=None)
    def test_post_validation_error(
        self, mock_validation_exception, mock_requests_request
    ):
        resource = ApiResource({"type": "things", "id": "someId"})
        resource.to_json = MagicMock(return_value={"name": "my_name"})
        resource.to_json_changed_attributes = MagicMock(
            return_value={"name": "my_name"}
        )

        mock_requests_request.return_value = self.MockResponse(
            '{"data": "getReturnData"}', 422
        )

        self.assertRaises(ValidationException, self.request_builder.post, resource)

        mock_requests_request.assert_called_with(
            "POST",
            "https://api.exonet.nl/things",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json={"data": {"name": "my_name"}},
            params=None,
        )

    @mock.patch("requests.request")
    def test_get_recursive(self, mock_requests_request):
        result_one = Response()
        result_one.status_code = 200
        result_one._content = str.encode(
            '{"data": '
            '[{"type": "test", "id": "abc"}], '
            '"meta": {"total": 2}, '
            '"links": {"next": "https://api.exonet.nl/next_page"}'
            "}"
        )

        result_two = Response()
        result_two.status_code = 200
        result_two._content = str.encode(
            '{"data": '
            '[{"type": "test", "id": "def"}], '
            '"meta": {"total": 2}, '
            '"links": {"next": null}'
            "}"
        )

        request_result = [result_one, result_two]
        mock_requests_request.side_effect = request_result

        self.request_builder.get_recursive()
        mock_requests_request.assert_any_call(
            "GET",
            "https://api.exonet.nl/things",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json=None,
            params={},
        )
        mock_requests_request.assert_any_call(
            "GET",
            "https://api.exonet.nl/next_page",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer None",
            },
            json=None,
            params=None,
        )


if __name__ == "__main__":
    unittest.main()
