"""The User-Agent sent with every request, so the API can tell this client apart."""

from importlib.metadata import PackageNotFoundError, version

import requests


def _package_version() -> str:
    try:
        return version("exonetapi")
    except PackageNotFoundError:
        # A source checkout that is not installed has no package metadata.
        return "unknown"


USER_AGENT = (
    f"exonet-api-python/{_package_version()} {requests.utils.default_user_agent()}"
)
