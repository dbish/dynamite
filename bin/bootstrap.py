import time
import uuid
import random
from pprint import pprint
import boto3
from datetime import datetime

from sqlalchemy import create_engine, Column, Table, MetaData, Text, BigInteger, DateTime
from sqlalchemy.pool import NullPool
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import sql

from enums import DataType
from json_gen import DynamoAttributeGenerator

from config import url

def default_columns():
    return [
        Column('item', JSONB),
        Column('modify_time', DateTime, default=datetime.now, onupdate=datetime.now),
        Column('create_time', DateTime, default=datetime.now)
    ]


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

        # map column/table names to postgres appropriate names
        columns = [Column(key['AttributeName'], Text, primary_key=True) for key in keys] + default_columns()

        table_obj = Table(response['TableName'], metadata, *columns)

        print(repr(table_obj))

    engine = create_engine(url)
    metadata.create_all(engine)


if __name__ == '__main__':
    main()
