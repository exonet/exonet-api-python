import unittest
from unittest.mock import Mock, create_autospec

from requests import Response

from exonetapi.exceptions import ValidationException
from tests.base import BaseTestCase


class TestValidationException(BaseTestCase):
    """Tests for the ValidationException."""

    def test_no_errors(self) -> None:
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(return_value={"errors": []})

        v = ValidationException(response)
        response.json.assert_called_once()

        assert v.args[0] == "There are 0 validation errors."

    def test_one_error(self) -> None:
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(
            return_value={
                "errors": [
                    {
                        "status": 422,
                        "detail": "Detailed error message",
                        "variables": {
                            "field": "start_date",
                            "rule": "iso8601-date",
                            "rule_requirement": "Date must be in iso8601 format",
                        },
                    }
                ]
            }
        )

        # Create the validation exception
        v = ValidationException(response)

        response.json.assert_called_once()
        # Make sure the right message is set.
        assert v.args[0] == "There is 1 validation error."
        assert v.get_failed_validations()["start_date"][0] == "Detailed error message"

    def test_two_errors(self) -> None:
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(
            return_value={
                "errors": [
                    {
                        "status": 422,
                        "code": "102.10001",
                        "title": "validation.generic",
                        "detail": "The data.end_date field is required.",
                        "variables": {
                            "field": "data.end_date",
                            "value": None,
                            "rule": "Required",
                            "rule_requirement": "",
                        },
                    },
                    {
                        "status": 422,
                        "code": "102.10001",
                        "title": "validation.generic",
                        "detail": "The provided data is invalid.",
                        "variables": [],
                    },
                ]
            }
        )

        # Create the validation exception
        v = ValidationException(response)

        response.json.assert_called_once()
        failed = v.get_failed_validations()
        # Make sure the right message is set.
        assert v.args[0] == "There are 2 validation errors."
        assert failed["data.end_date"][0] == "The data.end_date field is required."
        assert failed["generic"][0] == "The provided data is invalid."

    def test_other_errors(self) -> None:
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(
            return_value={
                "errors": [
                    {
                        "status": 500,
                    },
                ]
            }
        )

        # Create the validation exception
        v = ValidationException(response)

        response.json.assert_called_once()
        # Make sure there is no validation exception message.
        assert v.args[0] == "There are 0 validation errors."


if __name__ == "__main__":
    unittest.main()
