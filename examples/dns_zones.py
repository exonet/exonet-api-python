# Run this script using: python examples/dns_zones.py <YOUR-TOKEN>
import sys
from exonetapi import Client

# Create a new Client.
client = Client('https://api.exonet.nl')

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

print('\nDNS zones (max 20):\n')
# Get max 20  DNS zones.
zones = client.resource('dns_zones').size(20).get()

# Loop zones.
for zone in zones:
    # Print zone name and record count.
    print('{zone_name} - {record_count} records'.format(
        zone_name=zone.attribute('name'),
        record_count=len(zone.relationship('records'))
    ))

print('\n')
