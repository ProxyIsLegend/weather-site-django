"""
Файл содержит модели для форм
"""
from django.db import models


class FeedbackHistory(models.Model):
    """
    fields:
    date – время, в которое было оставлено сообщение
    text – сообщение пользователя
    """
    date = models.CharField(max_length=1000)
    text = models.CharField(max_length=1000)