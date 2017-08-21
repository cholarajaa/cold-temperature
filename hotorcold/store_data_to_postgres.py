import os
import csv
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotorcold.settings")
django.setup()

from reactor.models import EventsDump
from reactor.tasks import create_event, update_aggregated_userdata


def test_create_20000_events():
    with open('events_01.csv') as f:
        for row in csv.DictReader(f):
            EventsDump.objects.create(events_json=row)
            create_event.apply_async((json.dumps(row), ))
    return True


def test_update_20000_events():
    with open('events_02.csv') as f:
        for row in csv.DictReader(f):
            EventsDump.objects.create(events_json=row)
            create_event.apply_async((json.dumps(row), ))
    return True


def aggregate_user_data():
    update_aggregated_userdata.apply_async()
    return True


if __name__ == '__main__':
    t = time.time()
    test_create_20000_events()
    print("created tasks to create 20,000 records in secs:", (t - time.time()))
    test_update_20000_events()
    print("created tasks to update 20,000 records in secs:", (t - time.time()))
    aggregate_user_data()
    print("created task to aggregate userdata in secs:", (t - time.time()))
