"""
Models for two-factor authentication.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class OTPCode(models.Model):
    """Model for storing OTP codes."""

    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    code = models.CharField(max_length=6, verbose_name='Код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    expires_at = models.DateTimeField(verbose_name='Истекает')
    is_used = models.BooleanField(default=False, verbose_name='Использован')
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name='Telegram ID')

    class Meta:
        verbose_name = 'OTP код'
        verbose_name_plural = 'OTP коды'
        db_table = 'otp_codes'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phone_number} - {self.code}'

    def is_valid(self):
        """Check if OTP code is still valid."""
        return not self.is_used and timezone.now() < self.expires_at

    def save(self, *args, **kwargs):
        """Set expiration time on creation."""
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(
                minutes=settings.OTP_EXPIRY_MINUTES
            )
        super().save(*args, **kwargs)


class TelegramUser(models.Model):
    """Model for mapping phone numbers to Telegram IDs."""

    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Telegram Username')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'
        db_table = 'telegram_users'

    def __str__(self):
        return f'{self.phone_number} - {self.telegram_id}'
