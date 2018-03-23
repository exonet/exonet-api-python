import unittest
from unittest import mock
from unittest.mock import MagicMock

from exonetapi.auth import Authenticator


class testAuthenticator(unittest.TestCase):
    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content
            self.status_code = status_code

        def raise_for_status(self):
            return None

    @mock.patch('requests.post')
    def test_get_new_token(self, mock_requests_post):
        mock_requests_post.return_value = self.MockResponse('new token')
        mock_requests_post.return_value.json = MagicMock(return_value={
            'access_token': 'new token'
        })

        a = Authenticator('https://test.url/', 'auth')
        token = a.get_new_token('payload')

        mock_requests_post.assert_called_with(
            'https://test.url/auth',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
            },
            data='payload'
        )

        self.assertEqual(token, 'new token')

    def test_set_token(self):
        a = Authenticator('https://test.url/', 'auth')
        a.set_token('a-new-token')

        self.assertEqual(a.get_token(), 'a-new-token')

    @mock.patch('requests.post')
    def test_password_auth(self, mock_requests_post):
        a = Authenticator('https://test.url/', 'auth')
        a.password_auth(
            'user',
            'pwd',
            'client id',
            'client secret'
        )

        mock_requests_post.assert_called_with(
            'https://test.url/auth',
            headers={
                'Accept': 'application/vnd.Exonet.v1+json',
            },
            data={
                'grant_type': 'password',
                'username': 'user',
                'password': 'pwd',
                'client_id': 'client id',
                'client_secret': 'client secret'
            }
        )


if __name__ == '__main__':
    unittest.main()
