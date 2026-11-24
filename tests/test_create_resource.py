import unittest

from exonetapi.create_resource import create_resource
from tests.base import BaseTestCase


class TestCreateResource(BaseTestCase):
    """Tests for create_resource."""

    def test_create_resource(self) -> None:
        resource_data = {"type": "test_resource"}

        resource = create_resource(resource_data)

        assert resource.__class__.__name__ == "TestResource"


if __name__ == "__main__":
    unittest.main()
