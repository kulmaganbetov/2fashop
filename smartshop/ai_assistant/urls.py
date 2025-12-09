"""
URL configuration for AI assistant app.
"""
from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.assistant_page, name='chat'),
    path('ask/', views.ask_question, name='ask_question'),
    path('clear/', views.clear_chat, name='clear_chat'),
]
