"""Main class to interact with the Exonet API."""

from typing import Any, ClassVar
from urllib.parse import urlparse

from .auth import Authenticator
from .RequestBuilder import RequestBuilder


class Singleton(type):
    """Metaclass that gives every class using it a single shared instance."""

    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Return the existing instance, or create it on the first call."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Client(metaclass=Singleton):
    """The client to interact with the API.

    Manages connection details.
    """

    # The URL to use for authentication.
    authentication_endpoint = "/oauth/token"

    def __init__(self, host: str | None = None) -> None:
        self.__host = "https://api.exonet.nl"

        if host:
            self.set_host(host)

        self.authenticator = Authenticator(
            self.get_host(), self.authentication_endpoint
        )

    def set_host(self, host: str) -> None:
        """Set the API host.

        Make sure a protocol is set.

        :param host: The API host including the http(s) protocol.
        """
        parsed_host = urlparse(host)

        # Make sure the host uses a valid scheme.
        if parsed_host.scheme not in ("http", "https"):
            message = f"Invalid protocol for host: {host}"
            raise ConnectionAbortedError(message)

        self.__host = parsed_host.geturl()

    def get_host(self) -> str:
        return self.__host

    def resource(self, resource: str) -> RequestBuilder:
        """Prepare a new request to a resource endpoint.

        :param resource: The type of resource.
        :return: A RequestBuilder to make API calls.
        """
        return RequestBuilder(resource, self)
