import sys
import random
import math
import json

from decimal import Decimal
from functools import partial, wraps

from enums import DataType
##-----------------------------------------------------------------------

class JsonGenerator(object):
    """modified from: https://github.com/maxtaco/python-random-json"""
    def __init__ (self):
        # a consistently seeded own random object
        self.random = random.Random()

    def null(self):
        return None

    def boolean(self):
        return self.random.choice((True, False))

    def byte (self):
        return self.random.randint(0, 0xff)

    def integer (self, signed=False):
        i = self.random.randint(0, 0xffffffff)
        if signed:
            i = 0x7fffffff - i
        return i

    def _small_float (self, pos=True):
        n = self.integer(not pos)
        d = self.integer(False)
        d = 1 if d is 0 else d
        try:
            return float(d) / float(n)
        except OverflowError as e:
            return 0.0


    def float(self):
        base = self._small_float(True)
        exp = self._small_float()
        try:
            return math.pow(base, exp)
        except OverflowError as e:
            return sys.float_info.max

    def string(self, n = None):
        if not n:
            n = self.random.randint(1, 200)
        s = ''.join([ chr(self.byte()) for i in range(n) ])
        return s.encode('base64').strip()

    def array (self, n, d):
        if not n:
            n = self.random.randint(0, 10)
        return [ self.json(d+1) for i in range(n) ]

    def obj (self, n, d=0):
        if not n:
            n = self.random.randint(0, 8)

        name_length = partial(self.random.randint, 12, 16)
        return { self.string(name_length()) :  self.json(d + 1) for i in range(n) }

    def json(self, d=0):
        b = self.random.randint(0, 7)
        ret = None

        # Don't go more than 4 levels deep. Cut if off by
        # not allowing recursive structures at level 5.
        if d > 4 and b > 5:
            b = b % 5

        if False: pass
        elif b is 0: ret = False
        elif b is 1: ret = True
        elif b is 2: ret = None
        elif b is 3: ret = self.integer(True)
        elif b is 4: ret = self.float()
        elif b is 5: ret = self.string()
        elif b is 6: ret = self.array(None, d)
        elif b is 7: ret = self.obj(None, d)
        return ret

def add_dynamo_type(func):
    data_types = DataType._asdict()

    @wraps(func)
    def dynamo_type_adder(*args, **kwargs):
        type_descriptor = data_types[func.__name__]
        return { type_descriptor : func(*args, **kwargs) }

    return dynamo_type_adder

POS_NUMBER_MAX = Decimal('9.9999999999999999999999999999999999999E+125')
POS_NUMBER_MIN = Decimal('1E-130')
NEG_NUMBER_MAX = Decimal('-9.9999999999999999999999999999999999999E+125')
NEG_NUMBER_MIN = Decimal('-1E-130')


class DynamoAttributeGenerator(object):
    def __init__(self):
        self.random = random.Random()
        self.json_generator = JsonGenerator()

    @add_dynamo_type
    def null(self):
        return True

    @add_dynamo_type
    def boolean(self):
        return self.json_generator.boolean()

    @add_dynamo_type
    def number(self, subtype=None):
        if subtype is None:
            subtype = self.random.choice(('byte', 'integer', 'float'))

        value = None
        if subtype == 'integer':
            value = json.dumps(self.json_generator.integer())

        elif subtype == 'float':
            value = self.json_generator.float()

            is_pos = value > 0
            if is_pos:
                if value > POS_NUMBER_MAX:
                    value = str(POS_NUMBER_MAX)
                elif value < POS_NUMBER_MIN:
                    value = str(POS_NUMBER_MIN)
                else:
                    value = json.dumps(value)
            else:
                if value < NEG_NUMBER_MAX:
                    value = str(POS_NUMBER_MAX)
                elif value > POS_NUMBER_MIN:
                    value = str(POS_NUMBER_MIN)
                else:
                    value = json.dumps(value)

        elif subtype == 'byte':
            value = json.dumps(self.json_generator.byte())
        else:
            value = json.dumps(self.json_generator.integer())

        return value

    @add_dynamo_type
    def string(self, length=None):
        return self.json_generator.string(length)

    @add_dynamo_type
    def binary(self, length=None):
        return self.json_generator.string(length)

    @add_dynamo_type
    def number_set(self, length=None):
        if length is None:
            length = self.random.randint(1, 8)

        return list({self.number()[DataType.number] for i in range(length)})


    @add_dynamo_type
    def string_set(self, length=None):
        if length is None:
            length = self.random.randint(1, 8)

        return list({self.json_generator.string(16) for i in range(length)})

    @add_dynamo_type
    def binary_set(self, length=None):
        if length is None:
            length = self.random.randint(1, 8)

        return list({self.json_generator.string(16) for i in range(length)})


    @add_dynamo_type
    def list(self, n=None, d=0):
        if not n:
            n = self.random.randint(1, 8)
        return [ self.random_attribute(d + 1) for i in range(n) ]

    @add_dynamo_type
    def map(self, n=None, d=0):
        if not n:
            n = self.random.randint(1, 8)

        name_length = partial(self.random.randint, 6, 10)
        attr_map = {}
        for i in range(n):
            name = self.json_generator.string(name_length())
            value = self.random_attribute(d + 1)

            attr_map[name] = value

        return attr_map


    def random_attribute(self, d=0):
        b = self.random.randint(0, 9)
        ret = None

        # Don't go more than 4 levels deep. Cut if off by
        # not allowing recursive structures at level 7.
        if d > 4 and b > 7:
            b = b % 7

        if   b is 0: ret = self.null()
        elif b is 1: ret = self.boolean()
        elif b is 2: ret = self.number()
        elif b is 3: ret = self.string()
        elif b is 4: ret = self.binary()
        elif b is 5: ret = self.number_set()
        elif b is 6: ret = self.string_set()
        elif b is 7: ret = self.binary_set()
        elif b is 8: ret = self.list(None, d)
        elif b is 9: ret = self.map(None, d)
        return ret
