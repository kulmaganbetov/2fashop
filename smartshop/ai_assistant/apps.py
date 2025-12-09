"""
App configuration for AI assistant.
"""
from django.apps import AppConfig


class AiAssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartshop.ai_assistant'
    verbose_name = 'ИИ Ассистент'
