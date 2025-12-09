"""
User models for accounts app.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for phone-based authentication."""

    def create_user(self, phone_number, **extra_fields):
        """Create and save a regular user."""
        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with phone number authentication."""

    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name='Telegram ID')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')

    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Последний вход')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        """Return the full name of the user."""
        return f'{self.first_name} {self.last_name}'.strip() or self.phone_number

    def get_short_name(self):
        """Return the short name of the user."""
        return self.first_name or self.phone_number
