"""
dynamite
========

Use dynamite to keep a postgres replica of one or more dynamodb
tables. At its core, dynamite is an AWS Lambda event handler for
processing dynamodb streams record events and shuttling those record
events into an associated postgres database. Dynamite only has a
couple of pure python dependencies all of which make it easy to make
dynamite into sand-alone Lambda Function.
"""
import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s*=\s*(.*)\s*')

with open('dynamite/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f]
    requirements = [line for line in requirements if line != '']

setup(
    name='dynamite',
    version=version,
    url='http://github.com/vengefuldrx/dynamite',
    license='Apache License Version 2',
    author='Dillon Hicks',
    author_email='chronodynamic@gmail.com',
    description='A module to be used as an AWS Lambda function to keep postgres replicas of dynamodb tables.',
    long_description=__doc__,
    packages=['dynamite'],
    package_data={},
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: System :: Archiving :: Mirroring'
    ]
)
