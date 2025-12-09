"""
Admin configuration for shop app.
"""
from django.contrib import admin
from .models import Category, Smartphone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin panel for categories."""

    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):
    """Admin panel for smartphones."""

    list_display = ('name', 'brand', 'model', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'brand', 'category', 'created_at')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand', 'model', 'description')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Характеристики', {
            'fields': ('brand', 'model', 'screen_size', 'ram', 'storage', 'battery', 'camera', 'processor', 'os')
        }),
    )
