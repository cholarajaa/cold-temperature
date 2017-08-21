from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
from hotorcold import celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotorcold.settings')

app = Celery('hotorcold')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.config_from_object('hotorcold:celeryconfig')
