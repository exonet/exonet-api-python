"""
Obtain tokens and keep track of authentication details.
"""
import requests


class Authenticator:
    """
    Manage the authentication and keep track of (valid) tokens.
    """
    # The host to connect to when authenticating.
    __host = None

    # The endpoint on the Host to use when authenticating.
    __authentication_endpoint = None

    # The obtained authentication details.
    __auth_details = None

    def __init__(self, host, authentication_endpoint):
        self.__host = host
        self.__authentication_endpoint = authentication_endpoint

    def get_token(self):
        """Get the obtained authentication token.

        :return: The token if available.
        """
        if self.__auth_details:
            return self.__auth_details['access_token']

    def password_auth(self, username, password, client_id, client_secret):
        """Authorize using the password grant.

        :param username: The username.
        :param password: The password.
        :param client_id: The OAuth client ID.
        :param client_secret: The OAuth client secret.
        :return: None
        """
        self.get_new_token({
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        })

    def set_token(self, token):
        """Set a token to use when authorizing.

        This bypasses any calls to the authorization endpoint, but instead uses the provided token.

        :param token: A previously obtained token.
        :return: None
        """
        self.__auth_details = {
            'access_token': token
        }

    def get_new_token(self, payload):
        """Get a new token via the authorization endpoint.

        :param payload:
        :return: A new access token.
        """
        headers = {'Accept': 'application/vnd.Exonet.v1+json'}

        response = requests.post(
            self.__host + self.__authentication_endpoint,
            headers=headers,
            data=payload
        )

        # Raise exception on failed request.
        response.raise_for_status()

        # Set the auth details in the request for later use.
        self.__auth_details = response.json()

        return response.json()['access_token']
