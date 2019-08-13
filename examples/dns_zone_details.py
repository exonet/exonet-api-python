# Run this script using: python examples/dns_zone_details.py <YOUR-TOKEN>
import sys
from exonetapi import Client

# Create a new Client.
client = Client()

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

'''
Get a single dns_zone resource. Because depending on who is authorized, the dns_zone IDs change, all dns_zones are
retrieved with a limit of 1. From this result, the first DNS zone is used. In a real world scenario you would call
something like `zone = client.resource('dns_zones').get('VX09kwR3KxNo')` to get a single DNS zone by it's ID.
'''
zones = client.resource('dns_zones').size(1).get()

# Show error when there are no zones available.
if len(zones) == 0:
    print('There are no DNS zones found.')
    sys.exit()

zone = zones[0]

# Output DNS zone details.
print('DNS zone:\t{zone_name}'.format(
    zone_name=zone.attribute('name'),
))

# Get the records for this zone.
records = zone.related('records').get()

# Show records.
for record in records:
    print('{type}\t{fqdn}\t{ttl}\t{content}'.format(
        type=record.attribute('type'),
        fqdn=record.attribute('fqdn'),
        ttl=record.attribute('ttl'),
        content=record.attribute('content')
    ))

print('\n')
