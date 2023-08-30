from unittest.mock import patch

from tests.testCase import testCase
from exonetapi.Client import Client
from exonetapi.RequestBuilder import RequestBuilder


class testClient(testCase):
    @patch("exonetapi.auth.Authenticator.Authenticator.__init__", return_value=None)
    def test_init_arguments(self, mock_authenticator):
        client = Client("https://test.url")

        # Assert the host connection is set up.
        mock_authenticator.assert_called_once_with("https://test.url", "/oauth/token")

        self.assertEqual(client.get_host(), "https://test.url")

    def test_set_host(self):
        client = Client("https://test.url")
        client.set_host("http://new.host")
        self.assertEqual(client.get_host(), "http://new.host")

    def test_set_host_invalid_protocol(self):
        client = Client("https://test.url")
        self.assertRaises(ConnectionAbortedError, client.set_host, "ftp://new.host")

    def test_resource(self):
        client = Client("https://test.url")
        resource = client.resource("/test")

        self.assertIsInstance(resource, RequestBuilder)

