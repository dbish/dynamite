import random

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from config import url

__all__ = [
    'prepare_test',
    'default_event_records',
    'create_event_records'
]

def prepare_test():
    test_table =
    engine = create_engine(url, poolclass=NullPool)
    metadata.drop_all(engine)

templates = [Template.insert, Template.modify, Template.remove]

def infinity():
    while True:
        yield

def generate_events(distinct=10, event_count=250):

    item_names = ['item-{}'.format(i) for i in range(distinct)]

    events = range(event_count) if event_count is not None else infinity()

    for e in events:
        template = random.choice(templates)
        subs = { 'NAME' : random.choice(item_names),
                 'MESSAGE' : ' '.join(random.sample(ipsum_words, 10)),
                 'TABLE' : 'test1'
        }
        yield eval(template %  subs)


def create_event_records(distinct=10, event_count=250):
    return {
        "Records": generate_events(distinct, event_count)
    }


class Template(object):
    insert = """{
      "eventID": "1",
      "eventVersion": "1.0",
      "dynamodb": {
        "Keys": {
          "name": {
            "S": "%(NAME)s"
          }
        },
        "NewImage": {
          "Message": {
            "S": "New item! %(MESSAGE)s"
          },
          "name": {
            "S": "%(NAME)s"
          }
        },
        "StreamViewType": "NEW_AND_OLD_IMAGES",
        "SequenceNumber": "111",
        "SizeBytes": 26
      },
      "awsRegion": "us-west-2",
      "eventName": "INSERT",
      "eventSourceARN": "arn:aws:dynamodb:us-west-2:account-id:table/%(TABLE)s/stream/2015-06-27T00:48:05.899",
      "eventSource": "aws:dynamodb"
    }"""

    modify =  """{
      "eventID": "2",
      "eventVersion": "1.0",
      "dynamodb": {
        "OldImage": {
          "Message": {
            "S": "New item!"
          },
          "name": {
            "S": "%(NAME)s"
          }
        },
        "SequenceNumber": "222",
        "Keys": {
          "name": {
            "S": "%(NAME)s"
          }
        },
        "SizeBytes": 59,
        "NewImage": {
          "Message": {
            "S": "%(MESSAGE)s"
          },
          "name": {
            "S": "%(NAME)s"
          }
        },
        "StreamViewType": "NEW_AND_OLD_IMAGES"
      },
      "awsRegion": "us-west-2",
      "eventName": "MODIFY",
      "eventSourceARN": "arn:aws:dynamodb:us-west-2:account-id:table/%(TABLE)s/stream/2015-06-27T00:48:05.899",
      "eventSource": "aws:dynamodb"
    }"""

    remove =   """{
      "eventID": "3",
      "eventVersion": "1.0",
      "dynamodb": {
        "Keys": {
          "name": {
            "S": "%(NAME)s"
          }
        },
        "SizeBytes": 38,
        "SequenceNumber": "333",
        "OldImage": {
          "Message": {
            "S": "%(MESSAGE)s"
          },
          "name": {
            "S": "%(NAME)s"
          }
        },
        "StreamViewType": "NEW_AND_OLD_IMAGES"
      },
      "awsRegion": "us-west-2",
      "eventName": "REMOVE",
      "eventSourceARN": "arn:aws:dynamodb:us-west-2:account-id:table/%(TABLE)s/stream/2015-06-27T00:48:05.899",
      "eventSource": "aws:dynamodb"
    }"""

ipsum_words = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum mattis et ante quis congue. Curabitur id nunc hendrerit, pretium orci id, bibendum erat. Pellentesque ipsum nibh, molestie id lobortis et, feugiat a ligula. Integer eu tellus at lectus pretium suscipit. Sed ut mi sodales felis euismod rhoncus in ac lectus. Donec eu turpis in felis eleifend egestas sed nec purus. Pellentesque molestie, metus sed fermentum lacinia, neque libero laoreet massa, vitae elementum nulla purus nec quam. Curabitur est ex, consequat vitae egestas at, dignissim sit amet justo. Nulla venenatis orci ut nisl mattis, sit amet fermentum lorem facilisis. Vivamus consequat massa fringilla ullamcorper dictum. Vivamus eros odio, porttitor condimentum mi nec, facilisis pharetra magna. Donec nisl odio, pretium quis auctor ac, aliquet vel mi. Nunc rhoncus risus ut vulputate auctor. Proin elementum sodales augue, eu tristique orci. Fusce sed odio est. Suspendisse dui justo, vestibulum ac facilisis vel, placerat et purus. Nulla interdum diam ut arcu elementum, at sagittis neque feugiat. Aenean a nisi ac odio blandit bibendum. Nunc sit amet eros ut magna ornare cursus. Donec finibus leo id varius laoreet. Nunc vel elit justo. Sed vel quam sit amet sapien tincidunt posuere. Suspendisse ultricies ante eu faucibus tincidunt. Morbi sit amet vestibulum justo, vitae blandit purus. Nulla quis erat sodales, aliquet sapien quis, auctor arcu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ac volutpat sapien. Pellentesque sollicitudin nunc consequat, sollicitudin ligula efficitur, tristique ante. Sed a condimentum arcu, vitae sollicitudin justo. Aenean tincidunt semper tellus, vitae faucibus augue molestie cursus. Suspendisse volutpat dolor nulla. Vestibulum non elit ligula. Vivamus sapien sapien, porta quis tincidunt nec, hendrerit a mauris. Mauris elementum nec sapien vitae rutrum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nulla porttitor ante eu massa feugiat rhoncus. Sed eu hendrerit neque. Maecenas ultricies lacus sed egestas suscipit. Nullam volutpat velit quis rhoncus faucibus. Maecenas pretium auctor faucibus. Pellentesque ac mattis velit, ac mattis lorem. Suspendisse a enim lacus. Sed eleifend quam urna, nec commodo lacus ultrices vitae. In porttitor enim vitae orci blandit euismod. In ac justo eget nisi efficitur pulvinar sed eget ante. Duis eget dignissim enim, et facilisis augue. Cras rhoncus, dui vel volutpat feugiat, nisl lectus pulvinar ante, at feugiat velit sem consectetur odio. Suspendisse molestie, nisi a varius dictum, mauris ante eleifend ligula, et congue orci turpis eget arcu. Nulla finibus velit non neque tempus, sodales ornare nunc semper. Quisque nulla lectus, viverra fringilla tellus eget, porta finibus libero. Aenean suscipit fringilla sapien, vel tempus nisi porta non. Curabitur eleifend sollicitudin maximus. Maecenas mattis augue sit amet sem semper mollis. Suspendisse sed nunc nisi. Nulla facilisi. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aliquam scelerisque dictum elementum. Sed eros eros, finibus posuere efficitur non, faucibus nec dolor. Nullam quis est in ipsum commodo placerat quis dapibus nisl. Curabitur pretium elit interdum, ultricies velit nec, sollicitudin eros. Morbi vel imperdiet nisi. Sed feugiat dui lacinia erat commodo, sit amet tempus turpis convallis. Integer eu est faucibus, dignissim metus vitae, commodo eros.""".split()

default_event_records = create_event_records()
