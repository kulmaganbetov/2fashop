"""
Models for AI assistant app.
"""
from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    """Model for storing AI chat messages."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_id = models.CharField(max_length=255, db_index=True, verbose_name='ID сессии')
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    model_used = models.CharField(max_length=50, default='mock', verbose_name='Модель')
    response_time = models.FloatField(null=True, blank=True, verbose_name='Время ответа (сек)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        db_table = 'chat_messages'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.session_id} - {self.question[:50]}'
