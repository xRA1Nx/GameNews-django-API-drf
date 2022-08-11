import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamenews_proj.settings')

app = Celery('gamenews_proj')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# события по расписанию
app.conf.beat_schedule = {
    'every_week_notify': {
        'task': 'gamenews_app.tasks.celery_every_week_notify',
        'schedule': crontab(hour=10, minute=0, day_of_week='monday'),
        'args': (),
    },
    # 'printer': {
    #     'task': 'GameNewsApp.tasks.printer',
    #     'schedule': 10,
    #     'args': (5,)
    # },
    # ДЛЯ ОТЛАДКИ:
    # 'every_week_notify': {
    #     'task': 'gamenews_app.tasks.celery_every_week_notify',
    #     'schedule': 60,
    #     'args': (),
    # },

}
