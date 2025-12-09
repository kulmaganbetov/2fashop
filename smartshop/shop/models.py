"""
Models for shop app.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Product category model."""

    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])


class Smartphone(models.Model):
    """Smartphone product model."""

    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='smartphones',
        verbose_name='Категория'
    )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='smartphones/', blank=True, null=True, verbose_name='Изображение')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')

    # Specifications
    brand = models.CharField(max_length=100, verbose_name='Бренд')
    model = models.CharField(max_length=100, verbose_name='Модель')
    screen_size = models.CharField(max_length=50, blank=True, verbose_name='Диагональ экрана')
    ram = models.CharField(max_length=50, blank=True, verbose_name='Оперативная память')
    storage = models.CharField(max_length=50, blank=True, verbose_name='Память')
    battery = models.CharField(max_length=50, blank=True, verbose_name='Батарея')
    camera = models.CharField(max_length=100, blank=True, verbose_name='Камера')
    processor = models.CharField(max_length=100, blank=True, verbose_name='Процессор')
    os = models.CharField(max_length=50, blank=True, verbose_name='Операционная система')

    available = models.BooleanField(default=True, verbose_name='Доступен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'
        db_table = 'smartphones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['available']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    @property
    def in_stock(self):
        """Check if product is in stock."""
        return self.stock > 0
