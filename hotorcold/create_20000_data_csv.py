import os
import csv
import json
import time
import django
import random
import string
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotorcold.settings")
django.setup()

# #################### #
#   data preparation   #
# #################### #


def randomword(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def get_event_type():
    return random.choice([
        'FTStopEvent', 'FTInspectEvent', 'FTCommitEvent',
        'FTHandoverEvent', 'FTStartEvent', 'FTClearEvent', 'FTEnableEvent',
        'FTResetEvent', 'FTGroupEvent', 'FTUngroupEven', 'FTReadEvent',
        'FTCheckpointEvent', 'FTWriteEvent'])


def get_user_type():
    return random.choice(
        ['Shipment', 'Storage', 'Manufacturer', 'Retailer', 'Grower'])


usr_lst = [
    json.dumps({
        'owner_name': randomword(10),
        'company': randomword(10),
        'usertype': get_user_type(),
        'partnerName': randomword(20),
        'segmentTypeDeparture': randomword(20),
        'functionalName': randomword(20),
        'partnerTypeStart': randomword(20),
        'bizLocationTypeStart': randomword(20),
        'packagingTypeCode': randomword(20),
        'tradeItemCountryOfOrigin': randomword(30),
        'lowTemp': random.randint(0, 373),
        'referenceTemp': random.randint(0, 373),
        'referenceLife': random.randint(0, 200)
    }) for i in range(2000)]


def get_user():
    return random.choice(usr_lst)


def create_event():
    return {
        'time': timezone.now(),
        'organization_id': random.randint(100000, 12000000),
        'raspberry_id': random.randint(100000, 12000000),
        'event_type': get_event_type(),
        'event_order': random.randint(3000000, 402000000),
        'is_current': random.choice([0, 1]),
        'elapsed_seconds': random.randint(0, 300),
        'company_name': randomword(20),
        'client': randomword(20),
        'read_point': randomword(20),
        'biz_location': randomword(20),
        'biz_step': randomword(20),
        'version': random.randint(1, 100),
        'user_data': get_user()
    }


events_list = []
c = time.time()
for i in range(0, 20000):
    events_list.append(create_event())

keys = events_list[0].keys()
with open('events_01.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(events_list)

for event in events_list:
    event.update({
        'is_current': random.choice([0, 1]),
        'elapsed_seconds': random.randint(0, 300),
        'company_name': randomword(20),
        'client': randomword(20),
        'read_point': randomword(20),
        'biz_location': randomword(20),
        'biz_step': randomword(20),
        'version': random.randint(1, 100)
    })


with open('events_02.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(events_list)


x = time.time() - c
print('total time required to create 40000 csv file:', x)
