from collections import namedtuple

__all__ = [
    'EventType',
    'DataType',
    'ItemState'
    'KeyType',
]

def Enum(name, **fields):
    """Uses named tuple to make an instance with immutable attributes that
    is also enumerable. This is very similar, but not exactly like,
    the python 3.4 enum functionality
    """
    class EnumFactory(namedtuple(name, fields.keys())):
        def __new__(cls, *args, **kwargs):
            self = super(EnumFactory, cls).__new__(cls, *args, **kwargs)

            def _reverse_dict():
                return { v : k for k,v in self._asdict().items() }

            self._reverse_dict = _reverse_dict

            return self

        def __call__(self, value):
            """Reverse lookup by value => SomeEnum('value') """
            return self._reverse_dict()[value]

        # def __getitem__(self, name):
        #     """lookup value by attribute name => SomeEnum['name']"""
        #     return self._asdict()[name]


    instance = EnumFactory(**fields)
    return instance

EventType = Enum('EventType',
    insert='INSERT',
    modify='MODIFY',
    remove='REMOVE')

KeyType = Enum('KeyType',
    hash='HASH',
    range='RANGE'
)

DataType = Enum('DataType',
    binary='B',
    boolean='BOOL',
    number='N',
    string='S',
    list='L',
    null='NULL',
    map='M',
    binary_set='BS',
    number_set='NS',
    string_set='SS')

ItemState = Enum('ItemRowState',
    does_not_exist='does_not_exist',
    exists='exists',
    new='new')
