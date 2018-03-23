"""
Main class to interact with the Exonet API.
"""
from .auth import Authenticator
from .RequestBuilder import RequestBuilder
from urllib.parse import urlparse


class Client:
    """The client to interact with the API.

    Manages connection details.
    """
    # The API hostname.
    __host = None

    # The URL to use for authentication.
    authentication_endpoint = '/oauth/token'

    # An instance of the Authenticator that keeps track of the token.
    authenticator = None

    def __init__(self, host):
        self.set_host(host)
        self.authenticator = Authenticator(self.__host, self.authentication_endpoint)

    def set_host(self, host):
        """
        Set the API host.
        Make sure a protocol is set.

        :param host: The API host including the http(s) protocol.
        :return: The parsed API host.
        """
        parsed_host = urlparse(host)

        # Make sure the host uses a valid scheme.
        if parsed_host.scheme not in ('http', 'https'):
            raise ConnectionAbortedError('Invalid protocol for host: %s' % host)

        self.__host = parsed_host.geturl()

    def resource(self, resource):
        """Prepare a new request to a resource endpoint.

        :param resource: The type of resource.
        :return: A RequestBuilder to make API calls.
        """
        return RequestBuilder(self.__host, self.authenticator).set_resource(resource)
