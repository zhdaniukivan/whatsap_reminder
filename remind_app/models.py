from django.db import models


class Remind(models.Model):
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    time_to_remind = models.DateTimeField()
    remind_about = models.TextField()


class ProcessedMessage(models.Model):
    message_sid = models.CharField(max_length=34, unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)



