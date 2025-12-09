"""
Views for AI assistant app.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.models import Session
from .services import AIAssistantService
import uuid


def assistant_page(request):
    """AI assistant chat page."""
    # Get or create session ID for chat
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())

    session_id = request.session['chat_session_id']

    # Get chat history
    ai_service = AIAssistantService()
    chat_history = ai_service.get_chat_history(session_id)

    return render(request, 'ai_assistant/chat.html', {
        'chat_history': reversed(list(chat_history)),
        'session_id': session_id
    })


@require_http_methods(["POST"])
def ask_question(request):
    """Handle AJAX question from user."""
    question = request.POST.get('question', '').strip()

    if not question:
        return JsonResponse({
            'success': False,
            'error': 'Вопрос не может быть пустым'
        })

    # Get or create session ID
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())

    session_id = request.session['chat_session_id']
    user = request.user if request.user.is_authenticated else None

    # Get AI response
    # Set use_real_api=True and provider='openai' or 'claude' to use real AI
    ai_service = AIAssistantService(use_real_api=False)
    chat_message = ai_service.ask(question, session_id, user)

    return JsonResponse({
        'success': True,
        'question': chat_message.question,
        'answer': chat_message.answer,
        'timestamp': chat_message.created_at.strftime('%H:%M'),
    })


def clear_chat(request):
    """Clear chat history."""
    if 'chat_session_id' in request.session:
        del request.session['chat_session_id']

    return JsonResponse({'success': True})
