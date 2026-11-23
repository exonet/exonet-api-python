# Run this script using: python examples/tickets.py <YOUR-TOKEN>
import sys

from exonetapi import Client

# Create a new Client.
client = Client()

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

print("\nNumber and last email date of the latest tickets (limit 5):\n")
# Get 5 tickets.
tickets = client.resource("tickets").size(5).get()
for ticket in tickets:
    # For all the tickets, print the ticket number with the date of its last email.
    print(f"{ticket.attribute('number')} - {ticket.attribute('last_email_date')}")


print("\nNumber and last email date of the open tickets:\n")
# Get all tickets that are open.
open_tickets = client.resource("tickets").filter("state", "open").get()
for ticket in open_tickets:
    # For the open tickets, print the ticket number with the date of its last email.
    print(f"{ticket.attribute('number')} - {ticket.attribute('last_email_date')}")
