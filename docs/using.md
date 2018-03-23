# Using this package
The base of every request to the API is the `exonetapi.Client` class. This class will take care of constructing
and executing request to the API. When instantiating this class the host for the Exonet API must be specified.

## Authenticating requests
Requests to the API can not be made if no authentication method is set. Currently, the only valid authentication method
is the "Personal Access Token":

```python
from exonetapi import Client

# Create a new Client.
client = Client('https://api.exonet.nl')

# Authenticate with personal access token.
client.authenticator.set_token('<YOUR_API_TOKEN>')
```

---

[Back to the index](index.md)
