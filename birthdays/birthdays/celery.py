import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birthdays.settings')

app = Celery('birthdays')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-every-day-birthday-users': {
        'task': 'check_birthday_users_task',
        'schedule': crontab(minute='*/3')
    }
}
