# Run this script using: python examples/dns_zones.py <YOUR-TOKEN>
import sys
from exonetapi import Client
from exonetapi.structures import ApiResourceIdentifier
from exonetapi.structures import ApiResource

# Create a new Client.
client = Client()

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

print("\nAdd a new DNS zone\n")

# Create a new resource with the desired attributes.
zone = ApiResource("dns_zones")
zone.attribute("name", "my-new-zone.com")
zone.attribute("dnssec", True)
# Replace the customer ID with your own customer ID.
zone.relationship("customer", ApiResourceIdentifier("customers", "X09kwRdbbAxN"))
# Send the new resource to the API.
zone_result = zone.post()

# Add some records.
record1 = ApiResource("dns_records")
record1.attribute("name", "www")
record1.attribute("type", "A")
record1.attribute("content", "192.168.1.100")
record1.attribute("ttl", 3600)
record1.relationship("zone", ApiResourceIdentifier("dns_zones", zone_result.id()))
record_result_1 = record1.post()

record2 = ApiResource("dns_records")
record2.attribute("name", "test")
record2.attribute("type", "A")
record2.attribute("content", "192.168.1.200")
record2.attribute("ttl", 3600)
record2.relationship("zone", ApiResourceIdentifier("dns_zones", zone_result.id()))
record_result_2 = record2.post()

# Change the the 'www' record to an AAAA record.
record_result_1.attribute("type", "AAAA")
record_result_1.attribute("content", "fe80::1ff:fe23:4567:890a")
record_result_1.patch()

# Delete the test record.
record_result_2.delete()

print("DNS Zone ID: {}".format(zone_result.id()))
print("DNS Record ID: {}".format(record_result_1.id()))
print(record_result_1.related("zone").get().attribute("name"))
