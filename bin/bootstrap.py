"""
Introspect an account's dynamo tables for a certain region and
create the schema in the corresponding postgres database to reflect
that.
"""
import time
import uuid
import random
from pprint import pprint
from datetime import datetime

import boto3

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.pool import NullPool
from sqlalchemy import sql

from dyanmite.enums import DataType
from dynamite.test.generators import DynamoAttributeGenerator

from config import url


def main():
    metadata = MetaData()

    client = boto3.client('dynamodb', 'us-west-2')
    tables = client.list_tables()['TableNames']

    table_info = {}
    for table in tables:
        response = client.describe_table(TableName=table)['Table']

        table_info[table] = response

        keys = response['KeySchema']
        attrs = response['AttributeDefinitions']

        columns = table_columns(keys)
        table_obj = Table(response['TableName'], metadata, *columns)

        print(repr(table_obj))
        print()

    engine = create_engine(url, poolclass=NullPool)
    metadata.create_all(engine)


if __name__ == '__main__':
    main()
