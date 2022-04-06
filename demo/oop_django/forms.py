"""
Файл содержит формы для получения данных со страницы
"""
from django import forms


class FeedbackForm(forms.Form):
    """
    fields:
    review – отзыв пользователя
    """
    review = forms.CharField(label="Review", min_length=1, max_length=1000, required=True)


