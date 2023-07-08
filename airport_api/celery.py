import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'airport_api.settings')

app = Celery("airport_api")

app.config_from_object('django.conf:settings', namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
