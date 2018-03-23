import unittest
from unittest.mock import Mock, create_autospec

from requests import Response

from exonetapi.exceptions import ValidationException


class testValidationException(unittest.TestCase):
    def test_no_errors(self):
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(
            return_value={
                'errors': []
            }
        )

        v = ValidationException(response)
        response.json.assert_called_once()

        # Assert no validation exception message is set.
        self.assertEqual(v.args[0], '')

    def test_one_error(self):
        # Construct the request response.
        response = create_autospec(Response, spec_set=True)

        response.json = Mock(
            return_value={
                'errors': [
                    {
                        'status': 422,
                        'detail': 'Detailed error message',
                        'variables': {
                            'field': 'start_date',
                            'rule': 'iso8601-date',
                            'rule_requirement': 'Date must be in iso8601 format'
                        }
                    }
                ]
            }
        )

        # Create the validation exception
        v = ValidationException(response)

        response.json.assert_called_once()
        # Make sure the right message is set.
        self.assertEqual(v.args[0], 'Field: start_date, failed rule: iso8601-date(Date must be in iso8601 format).')

    def test_twoErrors(self):
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
                            "rule_requirement": ""
                        }
                    },
                    {
                        "status": 422,
                        "code": "102.10001",
                        "title": "validation.generic",
                        "detail": "The provided data is invalid.",
                        "variables": []
                    }
                ]
            }
        )

        # Create the validation exception
        v = ValidationException(response)

        response.json.assert_called_once()
        # Make sure the right message is set.
        self.assertEqual(v.args[0], 'Field: data.end_date, failed rule: Required(). The provided data is invalid.')

    def test_otherErrors(self):
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
        self.assertEqual(v.args[0], '')


if __name__ == '__main__':
    unittest.main()
