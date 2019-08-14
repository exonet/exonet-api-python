"""
Main class to interact with the Exonet API.
"""
from .auth import Authenticator
from .RequestBuilder import RequestBuilder
from urllib.parse import urlparse


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Client(metaclass=Singleton):
    """The client to interact with the API.

    Manages connection details.
    """

    # The URL to use for authentication.
    authentication_endpoint = '/oauth/token'

    def __init__(self, host=None):
        self.__host = 'https://api.exonet.nl'

        if host:
            self.set_host(host)

        self.authenticator = Authenticator(self.get_host(), self.authentication_endpoint)

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

    def get_host(self):
        return self.__host

    def resource(self, resource):
        """Prepare a new request to a resource endpoint.

        :param resource: The type of resource.
        :return: A RequestBuilder to make API calls.
        """
        return RequestBuilder(resource, self)
