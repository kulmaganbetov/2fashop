"""
Admin configuration for AI assistant app.
"""
from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin panel for chat messages."""

    list_display = ('id', 'user', 'session_id', 'question_preview', 'model_used', 'response_time', 'created_at')
    list_filter = ('model_used', 'created_at')
    search_fields = ('question', 'answer', 'session_id')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def question_preview(self, obj):
        """Show preview of question."""
        return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
    question_preview.short_description = 'Вопрос'
