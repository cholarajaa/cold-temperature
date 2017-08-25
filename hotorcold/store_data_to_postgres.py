import os
import csv
import json
import time
import datetime
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotorcold.settings")
django.setup()

from reactor.models import EventsDump, Event, AggregatedUserData
from reactor.tasks import create_or_update_event_data


def test_create_20000_events():
    with open('events_01.csv') as f:
        for row in csv.DictReader(f):
            row['user_data'] = json.loads(row['user_data'])
            EventsDump.objects.create(events_json=row)
            create_or_update_event_data.apply_async((json.dumps(row), ))
    return True


def test_update_20000_events():
    with open('events_02.csv') as f:
        for row in csv.DictReader(f):
            row['user_data'] = json.loads(row['user_data'])
            EventsDump.objects.create(events_json=row)
            create_or_update_event_data.apply_async((json.dumps(row), ))
    return True


if __name__ == '__main__':
    Event.objects.all().delete()
    EventsDump.objects.all().delete()
    AggregatedUserData.objects.all().delete()
    t = time.time()
    test_create_20000_events()
    print("created tasks to create 20,000 records in secs:", (time.time() - t))
    time.sleep(350)
    print("check if 20000 records exists")
    assert Event.objects.count() == 20000
    assert EventsDump.objects.count() == 20000
    print("20000 Events and EventsDump records exists in database")
    test_update_20000_events()
    time.sleep(300)
    print("check if any duplicated created")
    assert Event.objects.count() == 20000
    assert EventsDump.objects.count() == 20000
    print("No duplicates were added")
    print("created tasks to update 20,000 records in secs:", (time.time() - t))
