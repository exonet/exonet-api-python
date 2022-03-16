import unittest
from unittest import mock

from tests.testCase import testCase
from exonetapi.Client import Client
from exonetapi.RequestBuilder import RequestBuilder


class testClient(testCase):
    @mock.patch("exonetapi.auth.Authenticator.__init__", return_value=None)
    def test_init_arguments(self, mock_authenticator):
        client = Client("https://test.url")

        self.assertEqual(client.get_host(), "https://test.url")
        mock_authenticator.assert_called_with("https://test.url", "/oauth/token")

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


if __name__ == "__main__":
    unittest.main()
