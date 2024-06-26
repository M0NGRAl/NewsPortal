import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sending_posts_every_monday': {
        'task': 'news.tasks.week_email',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),
    },
}