# Working with API Responses
There are two types of API responses upon a successful request. If a single resource is requested then a [`ApiResource`](resources.md) instance is
returned, if multiple resources are requested then an `list` of `ApiResource`'s is returned.

## The [`ApiResource`](resources.md) class
Each resource returned by the API is transformed to an [`ApiResource`](resources.md) instance. This makes it possible to have easy access
to the attributes, type and ID of the resource.

```python
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

```python

# Get all certificates
certificates = client.resource('certificates').size(10).get()

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
