import random

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.pool import NullPool

from ..utils import table_columns
from .data import test_table_keys, test_table_name

from config import url

__all__ = [
    'prepare_test',
    'cleanup_test',
]

def prepare_test():

    metadata = MetaData()

    columns = table_columns(test_table_keys)
    table = Table(test_table_name, metadata, *columns)
    engine = create_engine(url, poolclass=NullPool)

    metadata.drop_all(engine)
    metadata.create_all(engine)


def cleanup_test():

    metadata = MetaData()

    columns = table_columns(test_table_keys)
    table = Table(test_table_name, metadata, *columns)
    engine = create_engine(url, poolclass=NullPool)
    metadata.drop_all(engine)
