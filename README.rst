Exonet API python package
=========================
Python 3 library for the Exonet API.

.. image:: https://img.shields.io/pypi/v/exonetapi.svg?style=flat-square
.. image:: https://img.shields.io/pypi/pyversions/exonetapi.svg?style=flat-square
.. image:: https://img.shields.io/lgtm/grade/python/g/exonet/exonet-api-python.svg
   :target: https://lgtm.com/projects/g/exonet/exonet-api-python/context:python
.. image:: https://img.shields.io/pypi/l/exonetapi.svg?style=flat-square

Conventions
-----------

- Code style guide: PEP 8.
- Docstring conventions: PEP 257 and reStructuredText.

Install
-------
Install using pip::

 pip install exonetapi

Usage
-----
Example to get the user details of the authorised user::

 from exonetapi import Client

 # Create a new Client.
 client = Client('https://api.exonet.nl')

 # Authorize with a personal access token.
 client.authenticator.set_token('<YOUR_TOKEN>')

 # Make an API call. Get details of the authorized user.
 user_details = client.resource('me').get()

 # Print user's name.
 print('Autorized as: {name}'.format(
     name=user_details.attribute('name')
 ))

See the `/docs` directory for complete documentation and additional code snippets.

Examples
--------

The `/examples` directory contains ready to use scripts to help you get started. These examples can be executed with your personal access token. One of them gets a ticket with it's emails and prints the details::

 $ python examples/ticket_details.py <YOUR-TOKEN>

This should make two API calls and print the ticket and email details for one of your tickets.

Testing
-------

Run unit tests and coverage::

 coverage run -m unittest discover tests -v && coverage html

Change log
----------

Please see `releases <https://github.com/exonet/exonet-api-python/releases>` for more information on what has changed recently.

Security
--------

If you discover any security related issues please email `support@exonet.nl <mailto:support@exonet.nl>`_ instead of using the issue tracker.

Credits
-------

- `Exonet <https://github.com/exonet>`_
- `All Contributors <https://github.com/exonet/exonet-api-python/graphs/contributors>`_

License
-------

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
