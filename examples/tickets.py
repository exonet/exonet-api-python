# Run this script using: python examples/tickets.py <YOUR-TOKEN>
import sys

from exonetapi import Client

# Create a new Client.
client = Client()

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

print("\nNumber and creation date of the latest tickets (limit 5):\n")
# Get 5 tickets.
tickets = client.resource("tickets").size(5).get()
for ticket in tickets:
    # For all the tickets, print the ticket number with its creation date.
    print(f"{ticket.attribute('number')} - {ticket.attribute('created_date')}")


print("\nNumber and creation date of the open tickets:\n")
# Get all tickets that are open.
open_tickets = client.resource("tickets").filter("state", "open").get()
for ticket in open_tickets:
    # For the open tickets, print the ticket number with its creation date.
    print(f"{ticket.attribute('number')} - {ticket.attribute('created_date')}")
