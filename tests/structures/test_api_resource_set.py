import unittest
from unittest import mock

import pytest

from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures.ApiResource import ApiResource
from exonetapi.structures.ApiResourceSet import ApiResourceSet
from tests.base import BaseTestCase


class TestApiResourceSet(BaseTestCase):
    """Tests for the ApiResourceSet."""

    def test_total(self) -> None:
        api_resource_set = ApiResourceSet()
        meta = {"resources": {"total": 1337}}
        api_resource_set.set_meta(meta)

        assert api_resource_set.total() == 1337
        assert meta == api_resource_set.meta()

    def test_links(self) -> None:
        links = {"next": "next_link", "prev": "prev_link"}
        api_resource_set = ApiResourceSet()
        api_resource_set.set_links(links)

        assert links == api_resource_set.links()

    @mock.patch.object(RequestBuilder, "get", return_value="api_response")
    def test_pagination(self, mock_request_builder) -> None:
        links = {
            "next": "https://api.exonet.nl/next_url?filter[unit]=test",
            "prev": "https://api.exonet.nl/prev_url?filter[unit]=test",
            "first": "https://api.exonet.nl/first/url?filter[unit]=test",
            "last": "https://api.exonet.nl/last/url?filter[unit]=test&last=true",
        }
        api_resource_set = ApiResourceSet()
        api_resource_set.set_links(links)

        assert api_resource_set.next_page() == "api_response"
        mock_request_builder.assert_called_with("next_url?filter[unit]=test")

        assert api_resource_set.previous_page() == "api_response"
        mock_request_builder.assert_called_with("prev_url?filter[unit]=test")

        assert api_resource_set.first_page() == "api_response"
        mock_request_builder.assert_called_with("first/url?filter[unit]=test")

        assert api_resource_set.last_page() == "api_response"
        mock_request_builder.assert_called_with("last/url?filter[unit]=test&last=true")

        api_resource_set.set_links({"next": None})
        assert api_resource_set.next_page() is None

    def test_add_resource(self) -> None:
        resource_one = ApiResource("fake", "abc")
        resource_two = ApiResource("fake", "def")

        api_resource_set = ApiResourceSet()
        api_resource_set.add_resource(resource_one)
        api_resource_set.add_resource([resource_two])

        assert len(api_resource_set) == 2

        for api_resource in api_resource_set:
            assert api_resource.id() == "abc" or api_resource.id() == "def"

        for api_resource in api_resource_set.resources():
            assert api_resource.id() == "abc" or api_resource.id() == "def"

    def test_get_item(self) -> None:
        api_resource_set = ApiResourceSet()
        api_resource_set.add_resource(
            [ApiResource("fake", "abc"), ApiResource("fake", "def")]
        )

        assert api_resource_set[0].id() == "abc"
        assert api_resource_set[-1].id() == "def"

        with pytest.raises(IndexError):
            api_resource_set[2]


if __name__ == "__main__":
    unittest.main()
