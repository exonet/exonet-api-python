# Error handling

For incorrect or failed requests the Exonet API will return exceptions or errors. In most cases this will be because
invalid data is provided (validation) or because the authenticated user does not have the right permissions to make
the request. These exceptions can be handled in the following way.

## Default exception behavior
A failed request will result in an exception containing the error message. The following example has no custom error
handling and will throw an exception when the request fails.
```python
from exonetapi import Client

# Create a new Client.
client = Client('https://api.exonet.nl')

# Login with machine token.
client.authenticator.set_token('INVALID_TOKEN')

# Try to make a request, will fail due to invalid token.
myDetails = client.resource('me').get()
```

## Catching exceptions and outputting errors
For validation exceptions you might be interested in the response body, since this can contain detail information about
why the request was invalid. Catch the exception and output the request body containing the validation exception.

```python
from exonetapi import Client
# Import the exception to catch.
from requests.exceptions import HTTPError

# Create a new Client.
client = Client('https://api.exonet.nl')

# Login with machine token.
client.Authenticator.set_token('A_PREVIOUSLY_OBTAINED_TOKEN')

try:
    # Try to get a certificate while providing an invalid ID.
    certificate = client.request('certificates').id('invalidID').get()
except HTTPError as e:
    print(e.response.text)
    raise e
```

This will output the request body where the details of the error can be found:
```
{"errors":[{"status":400,"code":"101.10002","title":"request.invalidId","detail":"The id provided for 'certificate' is invalid.","variables":[]}]}

requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://api.exonet.nl/certificates/invalidID
```

## Handling validation errors
When there are validation errors, an extended version of the HTTPError as describe above is returned. It contains the
validation errors grouped per field, accessible with the `get_failed_validations` method:

```python
# Assuming 'record' is an already constructed variable.
try:
    created_item = record.post()
except ValidationException as err:
    # Print validation errors.
    print('{}'.format(err))
    validation_errors = err.get_failed_validations()
    for field in validation_errors:
        for error in validation_errors[field]:
            print('{}: {}'.format(field, error))
except HTTPError as err:
    # Print all other errors.
    print('HTTP Error: {}'.format(err))
``` 

Validation errors that are not related to a field are keyed with `generic`.

---

[Back to the index](index.md)
