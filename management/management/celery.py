import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery("lms")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'every-1-minute': {
#         'task': 'catalog.tasks.some_scheduled_task',
#         'schedule': 10.0
#     },
#     'check_orders': {
#         'task': 'catalog.tasks.check_orders_and_send_mails',
#         'schedule': crontab(minute='*/1')
#
#     }
# }
