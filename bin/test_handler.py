from dynamite import dynamo_streams_event_handler

from dynamite.test.utils import prepare_test
from dynamite.test.generators import create_event_records

def test_main():
    prepare_test()
    dynamo_streams_event_handler(create_event_records(distinct=100, event_count=1000), None)

if __name__ == '__main__':
    test_main()
