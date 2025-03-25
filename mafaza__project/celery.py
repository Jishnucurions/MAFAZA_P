import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mafaza__project.settings')
app = Celery('mafaza__project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-transaction-returns-every-minute': {
        'task': 'mafazaapp.tasks.update_transaction_returns',  # Correct task path
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}