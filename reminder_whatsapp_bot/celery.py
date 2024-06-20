from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab, schedule

# Указываем путь к настройкам Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder_whatsapp_bot.settings')

# Создаем экземпляр приложения Celery
app = Celery('reminder_whatsapp_bot')

# Загружаем конфигурацию из объекта настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в зарегистрированных приложениях Django
app.autodiscover_tasks()

# Расписание задач Celery
app.conf.beat_schedule = {
    'send-remind-every-minute': {
        'task': 'remind_app.tasks.check_reminds',
        'schedule': crontab(minute='*/1'),
    },
    'check-incoming-messages-every-10-second': {
        'task': 'remind_app.tasks.check_incoming_messages',
        'schedule': schedule(10.0),
    },
}

