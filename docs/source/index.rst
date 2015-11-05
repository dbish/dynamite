.. Dynamite documentation master file, created by
   sphinx-quickstart on Wed Nov  4 15:24:06 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dynamite
========

Contents:

.. toctree::
   :maxdepth: 2

Dynamite provides a mechanism to keep a postgres replica of one or
more dynamodb table. At its core, dynamite is an AWS Lambda event
handler for processing dynamodb streams record events and shuttling
those record events into an associated postgres database.

Getting Started with Dynamite
#############################

*General prerequisites:*

* Existing Dynamodb tables with **NEW_IMAGE** or **NEW_AND_OLD_IMAGE** streams enabled.
* A running postgres server with a database you want to use for your replica.


Clone the Dynamite repository::

  git clone https://github.com/vengefuldrx/dynamite.git

Setup the virtual environment::

  cd dynamite
  virtualenv -p python2.7 venv
  source ./venv/bin/activate
  pip install -r requirements.txt

Create a config module with the url to the postgres database and the
region in which the dynamodb tables to replicate exist::

  cd dynamite
  echo "url = 'postgres+pg8000://<username>:<password>@<db-url>:<port>/<db-name>'" >> config.py
  echo "region = '<region>'" >> config.py

The config module is required since you cannot pass arguments to an
AWS Lambda function. The code and configuration has to be self
contained.

Set the python path to the root of the dynamite module in order to
have the config module on the path so it will be found by the
python interpreter. ::

    export PYTHONPATH=PYTHONPATH:`pwd`

.. Note:: When running on Lambda the python path is set for you by the
          Lambda execution environment.

Verify that the config is correct by using verifydb to generate a test
table and feed random events through dynamite::

  bin/verifydb

There should be a lot of json output followed by a line that reads
similarly to::

  Successfully processed 150 records.

Bootstrap the postgres replica database by creating the requisite
tables by introspecting the dynamo.::

  bin/bootstrapdb

The bootstrap script requires no arguments because it uses the config
module created previously.






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
