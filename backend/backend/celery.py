import os
from celery import Celery

# setting the default django settings module for the celery program

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE','backend.settings'
)

app = Celery('backend')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()