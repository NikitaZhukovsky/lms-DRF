import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery("management")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'send_monthly_report': {
        'task': 'users.tasks.send_monthly_report',
        'schedule': crontab(minute='*/1'),
    },
}


