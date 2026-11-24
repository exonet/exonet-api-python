from importlib.metadata import version

import requests

from exonetapi.user_agent import USER_AGENT


def test_user_agent_names_the_client_and_requests() -> None:
    expected = (
        f"exonet-api-python/{version('exonetapi')} "
        f"{requests.utils.default_user_agent()}"
    )

    assert expected == USER_AGENT
