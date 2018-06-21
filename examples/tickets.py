# Run this script using: python examples/tickets.py <YOUR-TOKEN>
import sys
from exonetapi import Client

# Create a new Client.
client = Client('https://api.exonet.nl')

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

print('\nID and subject of all tickets (limit 5):\n')
# Get 5 tickets.
all_tickets = client.resource('tickets').size(5).get()
for ticket in all_tickets:
    # For all the tickets, print the ticket ID with the subject.
    print('{id} - {subject}'.format(
        id=ticket.id(),
        subject=ticket.attribute('last_message_subject')
    ))


print('\nID and subject of all open tickets:\n')
# Get all tickets that are considered 'open' by Exonet.
open_tickets = client.resource('tickets').filter('open', 1).get()
for ticket in open_tickets:
    # For the open tickets, print the ticket ID with the subject.
    print('{id} - {subject}'.format(
        id=ticket.id(),
        subject=ticket.attribute('last_message_subject')
    ))
