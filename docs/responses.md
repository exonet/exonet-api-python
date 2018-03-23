# Working with API Responses
There are two types of API responses upon a successful request. If a single resource is requested then a `Resource` instance is 
returned, if multiple resources are requested then an `list` of `Resource`'s is returned.

## The `Resource` class
Each resource returned by the API is transformed to an `Resource` instance. This makes it possible to have easy access
to the attributes, type and ID of the resource.

```php
certificate = client.resource('certificates').get('VX09kwR3KxNo')

print(
    'Certificate {domain} has ID: {id}.\n'
    '- expires {expire_date}\n'
    '- Wildcard? {wildcard}'.format(
        id=certificate.id(),
        domain=certificate.attribute('domain'),
        wildcard=certificate.attribute('wildcard'),
        expire_date=certificate.attribute('expires_at')
    )
)
```

## Multiple resources
When the API returns multiple resources, for example when getting an overview page, a list is returned.
This list contains the requested resources. Iterate over the list to handle the resources:

```php

# Get all certificates
certificates = CLIENT.resource('certificates').size(10).get()

for certificate in certificates:
    print(
        '- {domain} Expires at {expire_date}'.format(
            domain=certificate.attribute('domain'),
            expire_date=certificate.attribute('expires_at')
        )
    )
```

---

[Back to the index](index.md)
