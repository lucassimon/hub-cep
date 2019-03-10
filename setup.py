# -*- coding: utf-8 -*-
import os
import sys
# Third
from setuptools import setup
from setuptools.command.install import install
from __version__ import version


def long_description():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


__description__ = 'Hub to connect multiple cep providers and setup a lambda func'

__author__ = 'Lucas Simon'
__author_email__ = 'lucassrod@gmail.com'

requirements = [
    'requests==2.21.0',
    'requests-toolbelt==0.9.1'
]

test_requirements = [
    'coveralls >= 1.1',
    'flake8 >= 3.3.0',
]

testing_extras = [
    'pytest',
    'pytest-cov',
]


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version
            )
            sys.exit(info)


setup(
    name='hub_cep',
    version=version,

    author=__author__,
    author_email=__author_email__,

    license='MIT',
    description=__description__,
    long_description=long_description(),
    url='https://github.com/lucassimon/hub-cep',
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
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
