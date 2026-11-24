import unittest
from unittest import mock
from unittest.mock import MagicMock

from exonetapi.auth import Authenticator
from exonetapi.user_agent import USER_AGENT
from tests.base import BaseTestCase


class TestAuthenticator(BaseTestCase):
    """Tests for the Authenticator."""

    class MockResponse:
        """Stand-in for a requests response."""

        def __init__(self, content, status_code=200) -> None:
            self.content = content
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

    @mock.patch("requests.post")
    def test_get_new_token(self, mock_requests_post) -> None:
        mock_requests_post.return_value = self.MockResponse("new token")
        mock_requests_post.return_value.json = MagicMock(
            return_value={"access_token": "new token"}
        )

        a = Authenticator("https://test.url/", "auth")
        token = a.get_new_token("payload")

        mock_requests_post.assert_called_with(
            "https://test.url/auth",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "User-Agent": USER_AGENT,
            },
            data="payload",
            timeout=30,
        )

        assert token == "new token"  # noqa: S105

    def test_set_token(self) -> None:
        a = Authenticator("https://test.url/", "auth")
        a.set_token("a-new-token")

        assert a.get_token() == "a-new-token"

    @mock.patch("requests.post")
    def test_password_auth(self, mock_requests_post) -> None:
        a = Authenticator("https://test.url/", "auth")
        a.password_auth("user", "pwd", "client id", "client secret")

        mock_requests_post.assert_called_with(
            "https://test.url/auth",
            headers={
                "Accept": "application/vnd.Exonet.v1+json",
                "User-Agent": USER_AGENT,
            },
            data={
                "grant_type": "password",
                "username": "user",
                "password": "pwd",
                "client_id": "client id",
                "client_secret": "client secret",
            },
            timeout=30,
        )


if __name__ == "__main__":
    unittest.main()
