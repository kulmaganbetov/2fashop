"""
Models for orders app.
"""
from django.db import models
from django.conf import settings
from smartshop.shop.models import Smartphone


class Order(models.Model):
    """Order model."""

    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    # Customer information
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(verbose_name='Адрес доставки')
    city = models.CharField(max_length=100, verbose_name='Город')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Индекс')

    # Order details
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.user.phone_number}'

    def get_total_cost(self):
        """Calculate total order cost."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Order item model."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    smartphone = models.ForeignKey(
        Smartphone,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Смартфон'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        db_table = 'order_items'

    def __str__(self):
        return f'{self.quantity}x {self.smartphone.name}'

    def get_cost(self):
        """Calculate item cost."""
        return self.price * self.quantity
