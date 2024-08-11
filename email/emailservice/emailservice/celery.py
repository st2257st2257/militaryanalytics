import os
from celery import Celery
# import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailservice.settings')
app = Celery('emailservice')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
