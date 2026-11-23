from __future__ import annotations

from typing import TYPE_CHECKING

from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from requests import Response

"""
Http validation exception.
"""


class ValidationException(HTTPError):
    """Raised when the API rejects a request because its data is invalid."""

    def __init__(self, response: Response) -> None:
        # Collect validation errors as list of strings.
        self.validation_errors: dict[str, list[str]] = {}

        # Loop errors.
        for error in response.json()["errors"]:
            # Handle only validation errors.
            if error["status"] == 422:
                field = "generic"
                if "field" in error["variables"]:
                    field = error["variables"]["field"] or error["detail"]

                if field not in self.validation_errors:
                    self.validation_errors[field] = []

                self.validation_errors[field].append(error["detail"])

        if self.validation_errors.__len__() == 1:
            validation_error = "There is {} validation error."
        else:
            validation_error = "There are {} validation errors."

        HTTPError.__init__(
            self,
            validation_error.format(self.validation_errors.__len__()),
            response=response,
        )

    def get_failed_validations(self) -> dict[str, list[str]]:
        return self.validation_errors
