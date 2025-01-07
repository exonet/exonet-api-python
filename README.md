# exonetapi
Python 3 library for the Exonet API.

[![Latest Version on Packagist][ico-version]][link-pypi]
[![Python Versions][ico-pyversions]][link-pypi]
[![Software License][ico-license]](LICENSE.md)

## Install
Install using pip:

```bash
pip install exonetapi
```

## Usage
Example to get the user details of the authorised user:

```py
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
```

See the `/docs` directory for complete documentation and additional code snippets.

## Examples

The `/examples` directory contains ready to use scripts to help you get started. These examples can be executed with your personal access token. One of them gets a ticket with it's emails and prints the details::

```
$ python examples/ticket_details.py <YOUR-TOKEN>
```
This should make two API calls and print the ticket and email details for one of your tickets.

## Change log

Please see [releases][link-releases] for more information on what has changed recently.

# Contributing

When contributing to this repository, please first discuss the change you wish
to make via issue, email, or any other method with the owners of this repository
before making a change.

Please note we have a code of conduct, please follow it in all your interactions
with the project.

### Issues and feature requests

You've found a bug in the source code, a mistake in the documentation or maybe
you'd like a new feature? You can help us by submitting an issue to our
[GitHub Repository][github]. Before you create an issue, make sure you search
the archive, maybe your question was already answered.

Even better: You could submit a pull request with a fix / new feature!

### Pull request process

1. Search our repository for open or closed [pull requests][prs] that relates
   to your submission. You don't want to duplicate effort.

2. You may merge the pull request in once you have the sign-off of two other
   developers, or if you do not have permission to do that, you may request
   the second reviewer to merge it for you.

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.9+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

*Now you're all set to get started!*

To run the Python tests:

```bash
poetry run pytest
```

To run the bandit checks:

```bash
poetry run bandit
```


## Security

If you discover any security related issues please email [development@exonet.nl](mailto:development@exonet.nl) instead
of using the issue tracker.


## Credits

- [Exonet][link-author]
- [All Contributors][link-contributors]


## License

[MIT License](LICENSE.md)

[ico-version]: https://img.shields.io/pypi/v/exonetapi.svg?style=flat-square
[ico-license]: https://img.shields.io/pypi/l/exonetapi.svg?style=flat-square
[ico-pyversions]: https://img.shields.io/pypi/pyversions/exonetapi.svg?style=flat-square

[github]: https://github.com/exonet/exonet-api-python/issues
[prs]: https://github.com/exonet/exonet-api-python/pulls

[link-pypi]: https://pypi.org/project/exonetapi/
[link-author]: https://github.com/exonet
[link-releases]: https://github.com/exonet/exonet-api-python/releases
[link-contributors]: ../../contributors

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
