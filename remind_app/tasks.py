from celery import shared_task
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from .models import Remind, ProcessedMessage
from datetime import datetime, timedelta
import pytz
import re
from django.utils import timezone


# Глобальная переменная для хранения времени последнего запроса
last_check_time = datetime.utcnow()

@shared_task
def send_remind(remind_id):

    try:
        remind = Remind.objects.get(id=remind_id)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Вы просили напомнить:\n{remind.remind_about}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=remind.phone_number
        )
        remind.delete()
        print(f'Remind sent and deleted: {remind_id}')
    except Remind.DoesNotExist:
        print(f'Remind with id {remind_id} does not exist.')
    except TwilioRestException as e:
        print(f'Failed to send message: {e}')


@shared_task
def check_reminds():

    now = timezone.localtime()
    print(f'Checking reminds at {now}')
    reminds = Remind.objects.filter(time_to_remind__lte=now)
    for remind in reminds:

        print(f'Sending remind: {remind.id}')
        send_remind.apply_async(args=[remind.id])


@shared_task
def check_incoming_messages():
    global last_check_time
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    now = timezone.localtime()

    # Запрашиваем только сообщения, отправленные после времени последней проверки
    messages = client.messages.list(date_sent_after=last_check_time)

    for message in messages:
        if message.from_ != settings.TWILIO_PHONE_NUMBER:
            message_sid = message.sid
            from_number = message.from_
            body = message.body.strip()
            pattern = r'^(\d{2}:\d{2})\s(.+)$'
            # Проверка и выделение
            match = re.match(pattern, body)
            if match:
                time = match.group(1)  # Время
                reminder = match.group(2)  # Напоминание
                now = timezone.localtime()
                time_to_remind = datetime.strptime(time, '%H:%M').replace(year=now.year, month=now.month,
                                                                          day=now.day, tzinfo=now.tzinfo)
                if ProcessedMessage.objects.filter(message_sid=message_sid).exists():
                    print(f'Message {message_sid} already processed.')
                    continue
                if time_to_remind < now:
                    time_to_remind += timedelta(days=1)
                remind = Remind.objects.create(
                    time_to_remind=time_to_remind,
                    remind_about=reminder,
                    phone_number=from_number
                )
                ProcessedMessage.objects.create(message_sid=message_sid)
                message = client.messages.create(
                    body=f'Ваше напоминание:\n{reminder} \nуспешно установлено на:\n{time_to_remind}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=from_number
                )
                print('we saved data in db and send message')
            else:
                print("Сообщение не соответствует формату")
        # Обновляем время последней проверки
        last_check_time = now
    return 'Проверка входящих сообщений завершена'

