import re
from operator import and_

from .enums import *

arn_regex = re.compile(r'arn:aws:dynamodb:(?P<region>.*?):(?P<account_id>.*?):table/(?P<table>.*?)/.*')
def parse_arn(arn):
    return arn_regex.match(arn).groupdict()

def primary_key_stmt(keys, table):
    """combine the individual equalities incase of composite primary keys"""
    return reduce(and_, [table.c.get(key) == value for key, value in keys.iteritems()])


def image_as_item(image):
    item = {}
    for column_name, field in image.iteritems():
        data_type, value = next(iter(field.items()))

        if data_type == DataType.number:
            try:
                value = int(value)
            except ValueError:
                value = float(value)

        elif data_type == DataType.string:
            pass
        else:
            print('Unhandled data type')
            try:
                json.dumps(value)
            except:
                value = str(value)

        item[column_name] = value

    return item
