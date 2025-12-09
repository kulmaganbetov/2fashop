"""
App configuration for orders.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartshop.orders'
    verbose_name = 'Заказы'
