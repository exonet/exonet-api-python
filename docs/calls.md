# Making API calls
After the client has been initialised, use the `resource` method to define which type of resource you want to get from
the API:

```python
certificates_request = client.resource('certificates')
```

This will return a `RequestBuilder` instance on which additional request parameters can be set:

```python
# Define which filters must be applied:
certificates_request.filter('expired', True)

# Set the number of resources to get:
certificates_request.size(10)

# Set the page to get:
certificates_request.page(2)

# Order by domain, desc:
certificates_request.sort('domain', 'desc')
```

After setting the options you can call the `get()` method to retrieve the resource:
```python
certificates = certificates_request.get()
```

It is also possible to get all resource sets recursively. The package will check the URL defined in `links.next` and as
long as the value is not `null` it will make an additional request and merge the results:

```python
certificates = certificates_request.get_recursive()
```

Please note that the `get_recursive` method respects pagination and filters. So the following example will get all
non-expired certificates, starting from page two in batches of ten:
```python
certificates = certificates_request.filter('expired', False).page(2).size.get_recursive()
```

## Getting a single resource by ID
If you want to get a specific resource by its ID, you can pass it as an argument to the `get` method:
```python
certificate = client.resource('certificates').get('VX09kwR3KxNo')
```

---

[Back to the index](index.md)
