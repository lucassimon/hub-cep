# -*- coding: utf-8 -*-

# Third
from setuptools import setup
from __version__ import version


def long_description():
    with open('README.md', encoding='utf8') as f:
        return f.read()


__description__ = 'Hub to connect multiple cep providers and setup a lambda func'

__author__ = 'Lucas Simon'
__author_email__ = 'lucassrod@gmail.com'

testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='hub_cep',
    version=version,

    author=__author__,
    author_email=__author_email__,

    license='MIT',
    description=__description__,
    long_description=long_description(),
    url='https://github.com:lucassimon/api.git',
    keywords='correios busca endereco cep',

    packages=['hub_cep'],
    package_dir={
        'hub_cep': 'hub_cep',
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.4",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Natural Language :: Portuguese',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
)
