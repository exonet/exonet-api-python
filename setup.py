"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

# Prefer setuptools over distutils.
from setuptools import setup, find_packages
# To use a consistent encoding.
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='exonetapi',
    version='0.0.2',

    description='Library to interact with the Exonet API.',
    long_description=long_description,
    keywords='Exonet API',

    url='https://github.com/exonet/exonet-api-python',

    author='Exonet B.V.',
    author_email='dev@exonet.nl',

    license='MIT',

    python_requires='~=3.4',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_dir={'exonetapi': 'exonetapi'},
    install_requires=['requests', 'inflection'],
)
