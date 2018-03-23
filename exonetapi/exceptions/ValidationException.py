from requests.exceptions import HTTPError
"""
Http validation exception.
"""
class ValidationException(HTTPError):
    def __init__(self, response):
        # Collect validation errors as list of strings.
        validationErrors = []

        # Loop errors.
        for error in response.json()['errors']:
            # Handle only validation errors.
            if error['status'] == 422:
                # Use the error details as error message.
                errorMessage = error['detail']

                # If the error has variables available, use those.
                if len(error['variables']) >= 3:
                    errorMessage = "Field: %s, failed rule: %s(%s)." % (
                        error['variables']['field'],
                        error['variables']['rule'],
                        error['variables']['rule_requirement']
                    )
                # Add this error message to the list of errors.
                validationErrors.append(errorMessage)

        HTTPError.__init__(self, ' '.join(validationErrors), response=response)
