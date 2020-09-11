# Working with API Responses
There are two types of API responses upon a successful request. If a single resource is requested then a [`ApiResource`](resources.md) instance is
returned, if multiple resources are requested then an `ApiResourceSet` is returned.

## The `ApiResourceSet` class
When the API returns multiple resources, for example when getting an overview page, an instance of the `ApiResourceSet` class
is returned. The instance of this class contains the requested resources. Traverse each individual resource by using a
`for`-loop on the instance:
```python
certificates = client.resource('certificates').get()
for certificate in certificates:
    # Each item is an instance of an ApiResource.
    print(certificate.id())
```

The get the number of items in a resource set, you can use one of the following methods:
```php
len(certificates); // Returns the number of resources in the current resource set.
certificates.total() // Returns the total number of resources in the resource set, ignoring pagination.
```

If `len != total` you can get the next/previous/first/last page by calling one of the pagination methods:
```python
# Get the next resource set:
certificates.next_page()
# Get the previous resource set:
certificates.previous_page()
# Get the first resource set:
certificates.first_page()
# Get the last resource set:
certificates.last_page()
```

Each of this methods will return `None` if not available.

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

---

[Back to the index](index.md)
