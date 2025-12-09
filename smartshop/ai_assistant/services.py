"""
AI assistant services.
"""
import time
from django.conf import settings
from .models import ChatMessage


class AIAssistant:
    """Base AI assistant class."""

    def __init__(self, model='mock'):
        self.model = model

    def get_response(self, question, context=None):
        """Get AI response to a question."""
        raise NotImplementedError


class MockAIAssistant(AIAssistant):
    """Mock AI assistant for testing without API keys."""

    def __init__(self):
        super().__init__(model='mock')

    def get_response(self, question, context=None):
        """Generate mock response."""
        question_lower = question.lower()

        # Simple keyword-based responses
        if any(word in question_lower for word in ['смартфон', 'телефон', 'купить', 'выбрать']):
            return (
                "Здравствуйте! Я помогу вам выбрать смартфон. У нас в наличии широкий ассортимент "
                "смартфонов от ведущих производителей: Apple iPhone, Samsung Galaxy, Xiaomi и другие. "
                "Какие характеристики для вас важны? (цена, камера, производительность, батарея)"
            )

        elif any(word in question_lower for word in ['цена', 'стоимость', 'сколько']):
            return (
                "Цены на наши смартфоны варьируются от 15 000 до 150 000 рублей. "
                "Бюджетные модели начинаются от 15-30 тыс. руб., средний класс - 30-60 тыс. руб., "
                "флагманы - от 60 тыс. руб. Посмотрите наш каталог для подробной информации."
            )

        elif any(word in question_lower for word in ['доставка', 'доставить']):
            return (
                "Мы осуществляем доставку по всей России. Доставка по Москве - 1-2 дня (бесплатно при заказе от 30 000 руб.), "
                "по России - 3-7 дней. Также доступен самовывоз из нашего магазина."
            )

        elif any(word in question_lower for word in ['гарантия', 'возврат']):
            return (
                "На все смартфоны предоставляется официальная гарантия производителя сроком 1 год. "
                "Возврат товара надлежащего качества возможен в течение 14 дней с момента покупки."
            )

        elif any(word in question_lower for word in ['apple', 'iphone', 'айфон']):
            return (
                "У нас представлены все актуальные модели iPhone: iPhone 15 Pro Max, iPhone 15 Pro, "
                "iPhone 15, iPhone 14, а также более ранние модели. Все устройства новые, с официальной гарантией."
            )

        elif any(word in question_lower for word in ['samsung', 'самсунг', 'galaxy']):
            return (
                "В наличии флагманская серия Samsung Galaxy S24, складные модели Galaxy Z Fold/Flip, "
                "а также модели среднего класса серии Galaxy A. Все с официальной гарантией."
            )

        else:
            return (
                "Спасибо за ваш вопрос! Я - виртуальный консультант SmartShop. "
                "Могу помочь вам с выбором смартфона, рассказать о наличии, ценах, доставке и гарантии. "
                "Что бы вы хотели узнать?"
            )


class OpenAIAssistant(AIAssistant):
    """OpenAI GPT assistant."""

    def __init__(self):
        super().__init__(model='gpt-3.5-turbo')
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")

    def get_response(self, question, context=None):
        """Get response from OpenAI API."""
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY

            system_prompt = """Вы - виртуальный консультант интернет-магазина SmartShop по продаже смартфонов.
            Помогайте клиентам выбирать смартфоны, отвечайте на вопросы о товарах, ценах, доставке и гарантии.
            Будьте вежливы, профессиональны и полезны."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]

            if context:
                messages.insert(1, {"role": "assistant", "content": f"Контекст: {context}"})

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Извините, произошла ошибка при обработке запроса: {str(e)}"


class ClaudeAssistant(AIAssistant):
    """Anthropic Claude assistant."""

    def __init__(self):
        super().__init__(model='claude-3-sonnet-20240229')
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")

    def get_response(self, question, context=None):
        """Get response from Claude API."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

            system_prompt = """Вы - виртуальный консультант интернет-магазина SmartShop по продаже смартфонов.
            Помогайте клиентам выбирать смартфоны, отвечайте на вопросы о товарах, ценах, доставке и гарантии.
            Будьте вежливы, профессиональны и полезны."""

            prompt = question
            if context:
                prompt = f"Контекст: {context}\n\nВопрос: {question}"

            message = client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except Exception as e:
            return f"Извините, произошла ошибка при обработке запроса: {str(e)}"


class AIAssistantService:
    """Service for managing AI assistant interactions."""

    def __init__(self, use_real_api=False, provider='openai'):
        """Initialize AI assistant service."""
        if use_real_api:
            if provider == 'openai' and settings.OPENAI_API_KEY:
                self.assistant = OpenAIAssistant()
            elif provider == 'claude' and settings.ANTHROPIC_API_KEY:
                self.assistant = ClaudeAssistant()
            else:
                # Fallback to mock if no API key
                self.assistant = MockAIAssistant()
        else:
            self.assistant = MockAIAssistant()

    def ask(self, question, session_id, user=None, context=None):
        """Ask question and save to database."""
        start_time = time.time()

        # Get AI response
        answer = self.assistant.get_response(question, context)

        response_time = time.time() - start_time

        # Save to database
        chat_message = ChatMessage.objects.create(
            user=user,
            session_id=session_id,
            question=question,
            answer=answer,
            model_used=self.assistant.model,
            response_time=response_time
        )

        return chat_message

    def get_chat_history(self, session_id, limit=10):
        """Get chat history for a session."""
        return ChatMessage.objects.filter(session_id=session_id).order_by('-created_at')[:limit]
