import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery("management")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_login': {
        'task': 'users.tasks.send_monthly_report',
        'schedule': crontab(minute='*/1')
    }
}



