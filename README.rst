Exonet API python package
=========================

.. image:: https://img.shields.io/pypi/v/exonetapi.svg?style=flat-square
.. image:: https://img.shields.io/pypi/pyversions/exonetapi.svg?style=flat-square
.. image:: https://img.shields.io/pypi/l/exonetapi.svg?style=flat-square

Python 3 library for the Exonet API.

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

Please see the `/docs` folder for complete documentation and additional examples.

Testing
-------

Run unit tests and coverage::

 coverage run -m unittest discover tests -v && coverage html

Change log
----------

Please see `CHANGELOG <https://github.com/exonet/exonet-api-python/blob/master/CHANGELOG.md>`_ for more information on what has changed recently.

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
