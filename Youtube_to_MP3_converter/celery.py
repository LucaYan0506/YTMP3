from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Youtube_to_MP3_converter.settings')

app = Celery('Youtube_to_MP3_converter')

app.config_from_object('django.conf:settings', namespace= 'CELERY')

app.autodiscover_tasks()