"""
Admin configuration for two_factor app.
"""
from django.contrib import admin
from .models import OTPCode, TelegramUser


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    """Admin panel for OTP codes."""

    list_display = ('phone_number', 'code', 'created_at', 'expires_at', 'is_used', 'is_valid')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number', 'code')
    readonly_fields = ('created_at', 'expires_at')
    ordering = ('-created_at',)

    def is_valid(self, obj):
        """Display if code is valid."""
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Действителен'


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Admin panel for Telegram users."""

    list_display = ('phone_number', 'telegram_id', 'username', 'first_name', 'last_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone_number', 'telegram_id', 'username', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
