# Run this script using: python examples/ticket_details.py <YOUR-TOKEN>
import sys
from exonetapi import Client

# Create a new Client.
client = Client('https://api.exonet.nl')

# Authorize with a personal access token.
client.authenticator.set_token(sys.argv[1])

# Get a single ticket resource. Because depending on who is authorized, the ticket IDs change, all tickets are
# retrieved with a limit of 1. From this result, the first ticket is used. In a real world scenario you would
# call something like `ticket = client.resource('tickets').get('VX09kwR3KxNo')` to get a single ticket by it's ID.
ticket = client.resource('tickets').size(1).get()[0]

print(
    '\nTicket id:\t\t{id}\n'
    'Ticket subject:\t\t{subject}\n'
    'Created at:\t\t{ticket_date}\n'
    'Last message date:\t{last_message_date}\n'
    'Department:\t\t{department}\n'.format(
        subject=ticket.attribute('last_message_subject'),
        ticket_date=ticket.attribute('created_date'),
        last_message_date=ticket.attribute('last_message_date'),
        department=ticket.attribute('department'),
        id=ticket.id()
    )
)


# Get the emails in the ticket.
emails = client.resource('tickets/{id}/emails'.format(id=ticket.id())).get()

print('This ticket has {mailCount} emails'.format(
    mailCount=len(emails)
))
for email in emails:
    print(
        '---------------------------------------------\n'
        'Email id:\t{id}\n'
        'Subject:\t{subject}\n'
        'Date:\t\t{message_date}\n\n'
        '{message}'.format(
            subject=email.attribute('subject'),
            message_date=email.attribute('created_date'),
            id=email.id(),
            message=email.attribute('body')[:100]
        )
    )