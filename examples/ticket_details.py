# Run this script using: python examples/ticket_details.py <YOUR-TOKEN>
import sys

from exonetapi import Client

# Create a new Client.
client = Client()

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

"""
Get a single ticket resource. Because depending on who is authorized, the ticket IDs
change, all tickets are retrieved with a limit of 1. From this result, the first
ticket is used. In a real world scenario you would call something like
`ticket = client.resource('tickets').get('VX09kwR3KxNo')` to get a single ticket by
its ID.
"""
tickets = client.resource("tickets").size(1).get()

# Show this message when there are no tickets available.
if len(tickets) == 0:
    print("There are no tickets available")
    sys.exit()

ticket = tickets[0]

print(
    f"\nTicket id:\t\t{ticket.id()}\n"
    f"Ticket number:\t\t{ticket.attribute('number')}\n"
    f"Created at:\t\t{ticket.attribute('created_date')}\n"
    f"Status:\t\t\t{ticket.attribute('status')}\n"
)

# The conversation of a ticket holds all its messages. Keep only the emails.
conversation = ticket.related("conversation").get()
emails = [message for message in conversation if message.type() == "emails"]

print(f"This ticket has {len(emails)} emails")
for email in emails:
    print(
        "---------------------------------------------\n"
        f"Email id:\t{email.id()}\n"
        f"Subject:\t{email.attribute('subject')}\n"
        f"Date:\t\t{email.attribute('date')}\n\n"
        f"{email.attribute('body')[:100]}"
    )
