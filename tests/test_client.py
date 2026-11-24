from unittest.mock import patch

import pytest

from exonetapi.auth.Authenticator import Authenticator
from exonetapi.Client import Client
from exonetapi.RequestBuilder import RequestBuilder
from tests.base import BaseTestCase


class TestClient(BaseTestCase):
    """Tests for the Client."""

    @patch.object(Authenticator, "__init__", return_value=None)
    def test_init_arguments(self, mock_authenticator) -> None:
        client = Client("https://test.url")

        # Assert the host connection is set up.
        mock_authenticator.assert_called_once_with("https://test.url", "/oauth/token")

        assert client.get_host() == "https://test.url"

    def test_set_host(self) -> None:
        client = Client("https://test.url")
        client.set_host("http://new.host")
        assert client.get_host() == "http://new.host"

    def test_set_host_invalid_protocol(self) -> None:
        client = Client("https://test.url")
        with pytest.raises(ConnectionAbortedError, match="Invalid protocol for host"):
            client.set_host("ftp://new.host")

    def test_resource(self) -> None:
        client = Client("https://test.url")
        resource = client.resource("/test")

        assert isinstance(resource, RequestBuilder)
