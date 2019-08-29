# Resources

## Getting data from a resource
Get data from the attributes or relationships of a resource. See [making API calls](calls.md) for more information on 
how to get resources from the API.

```python
dns_record = client.resource('dns_records').get('VX09kwR3KxNo')

# Show an attribute value:
print(dns_record.attribute('name'))

# Get a related value, in this case the name of the DNS zone:
print(dns_record.related('zone').get().attribute('name'))
```

## Creating a new resource
Post a new resource to the API by setting its attributes and relationships:

```python
record = Resource('dns_records')
record.attribute('name', 'www')
record.attribute('type', 'A')
record.attribute('content', '192.168.1.100')
record.attribute('ttl', 3600)
# The value of a relationship must be defined as a resource identifier.
record.relationship('zone', ApiResourceIdentifier('dns_zones', 'VX09kwR3KxNo'))
result = record.post()
print(result)
```

## Modifying a resource
Modify a resource by changing its attributes and/or relationships:

```python
dns_record = client.resource('dns_records').get('VX09kwR3KxNo')
# Or, if there is no need to retrieve the resource from the API first you can use the following:
# dns_record = ApiResource('dns_records', 'VX09kwR3KxNo')

# Change the 'name' attribute to 'changed-name'.
dns_record.attribute('name', 'changed-name')

# The value of a relationship must be defined as a resource identifier.
dns_record.relationship('dns_zone', ApiResourceIdentifier('dns_zones', 'X09kwRdbbAxN'))

# Patch the changed data to the API.
dns_record.patch()
``` 

## Deleting a resource
Delete a resource with a given ID:

```python
dns_record = client.resource('dns_records').get('VX09kwR3KxNo')
# Or, if there is no need to retrieve the resource from the API first you can use the following:
# dns_record = ApiResource('dns_records', 'VX09kwR3KxNo')

dns_record.delete()
```
