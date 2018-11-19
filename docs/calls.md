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

## Getting a single resource by ID
If you want to get a specific resource by its ID, you can pass it as an argument to the `get` method:
```python
certificate = client.resource('certificates').get('VX09kwR3KxNo')
```

---

[Back to the index](index.md)
