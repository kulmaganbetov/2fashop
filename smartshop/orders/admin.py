"""
Admin configuration for orders app.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items."""
    model = OrderItem
    raw_id_fields = ['smartphone']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin panel for orders."""

    list_display = ('id', 'user', 'first_name', 'last_name', 'phone', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'address')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Информация о клиенте', {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        ('Доставка', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin panel for order items."""

    list_display = ('order', 'smartphone', 'price', 'quantity', 'get_cost')
    list_filter = ('order__created_at',)
    raw_id_fields = ['order', 'smartphone']

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Сумма'
