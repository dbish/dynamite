import time
import uuid
import random
from pprint import pprint
import boto3


from dynamite.enums import DataType
from dynamite.test.generators import DynamoAttributeGenerator

STD_SLEEP_INT = .150 # 500ms

animals = ['moose', 'mouse', 'mantis', 'moth', 'dog', 'cat', 'snake']


def infinity():
    while True:
        yield

def generate_items(item_count=100):
    items = range(item_count) if item_count is not None else infinity()
    g = DynamoAttributeGenerator()

    for i in items:
        obj= {
            'genus-id' : { 'S' : '{}-{}'.format(random.choice(animals), uuid.uuid4().hex[:9]) },
            'species-id' : { 'S' : str(random.randint(9999, 100000)) }}
        try:
            obj.update(g.map(4)[DataType.map])
        except Exception as e:
            print(e)
            continue

        yield obj

def main():
    client = boto3.client('dynamodb', 'us-west-2')
    #client.get_item(TableName='sandbox2', Key={'name' : {'S' : 'slarp'} })

    for i, item in enumerate(generate_items(item_count=None)):
        print('Put item {}: {}'.format(i, item['genus-id']))
        try:
            client.put_item(TableName='sandbox2', Item=item)
        except Exception as e:
            print(e)

        time.sleep(STD_SLEEP_INT)




if __name__ == '__main__':
    main()
