"""
App configuration for two_factor.
"""
from django.apps import AppConfig


class TwoFactorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartshop.two_factor'
    verbose_name = 'Двухфакторная аутентификация'
