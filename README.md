# SmartShop - Интернет-магазин смартфонов

Полноценный интернет-магазин на Django с двухфакторной аутентификацией через Telegram и ИИ-ассистентом.

## Технологии

- **Backend**: Django 4.2.7, Django REST Framework
- **База данных**: PostgreSQL 15 (Docker)
- **Шаблоны**: Django Templates
- **Аутентификация**: Кастомная 2FA через Telegram-бот
- **ИИ**: OpenAI API / Anthropic Claude API (опционально)
- **Python**: 3.8+

## Основной функционал

### Магазин
- ✅ Каталог смартфонов с фильтрацией и поиском
- ✅ Детальная страница товара с характеристиками
- ✅ Корзина (добавление/удаление товаров)
- ✅ Оформление заказа
- ✅ Личный кабинет с историей заказов

### Аутентификация
- ✅ Регистрация и вход по номеру телефона
- ✅ 2FA через Telegram-бот с одноразовыми кодами
- ✅ Автоматическое создание аккаунта при первом входе

### ИИ-Ассистент
- ✅ Виртуальный консультант для помощи клиентам
- ✅ Интеграция с OpenAI/Claude API (или mock-режим)
- ✅ Логирование всех запросов в БД

## Структура проекта

```
2fashop/
├── smartshop/
│   ├── core/              # Настройки Django
│   ├── shop/              # Каталог товаров
│   ├── orders/            # Корзина и заказы
│   ├── accounts/          # Пользователи
│   ├── two_factor/        # 2FA и Telegram-бот
│   ├── ai_assistant/      # ИИ-консультант
│   ├── templates/         # HTML-шаблоны
│   └── static/            # CSS, JS, изображения
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd 2fashop
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=smartshop
DB_USER=smartshop_user
DB_PASSWORD=smartshop_pass
DB_HOST=localhost
DB_PORT=5432

# Telegram Bot (обязательно!)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here

# AI Assistant (опционально)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 5. Запуск PostgreSQL через Docker

```bash
docker-compose up -d
```

Это создаст и запустит контейнер с PostgreSQL 15.

### 6. Создание базы данных и миграции

```bash
# Применить миграции
python manage.py makemigrations
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser
# Введите номер телефона в формате: +79991234567
```

### 7. Создание статических файлов

```bash
python manage.py collectstatic --noinput
```

### 8. Запуск Telegram-бота

В **отдельном терминале** запустите Telegram-бота:

```bash
python -m smartshop.two_factor.telegram_bot
```

Или используйте удобный скрипт:

```bash
python run_bot.py
```

### 9. Запуск Django-сервера

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000

## Настройка Telegram-бота

### 1. Создание бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и получите токен
4. Добавьте токен в `.env` файл как `TELEGRAM_BOT_TOKEN`

### 2. Привязка номера телефона

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Отправьте `/link`
4. Введите ваш номер телефона в формате: `+79991234567`
5. Готово! Теперь вы можете получать коды подтверждения

## Тестирование

### Запуск всех тестов

```bash
python manage.py test
```

### Запуск тестов конкретного приложения

```bash
# Тесты 2FA
python manage.py test smartshop.two_factor

# Тесты аутентификации
python manage.py test smartshop.accounts
```

### Coverage (опционально)

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Создаст HTML-отчет в htmlcov/
```

## Использование

### Админ-панель

Доступ к админ-панели: http://127.0.0.1:8000/admin/

Здесь можно:
- Управлять товарами и категориями
- Просматривать заказы и менять их статус
- Управлять пользователями
- Просматривать OTP-коды и Telegram-аккаунты
- Просматривать логи ИИ-ассистента

### Добавление товаров

1. Войдите в админ-панель
2. Перейдите в "Категории" и создайте категорию (например, "Флагманы")
3. Перейдите в "Смартфоны" и создайте товар:
   - Заполните название, slug, описание
   - Укажите цену и количество на складе
   - Добавьте характеристики
   - Загрузите изображение (опционально)
   - Отметьте "Доступен"

### Процесс покупки

1. Пользователь просматривает каталог
2. Добавляет товары в корзину
3. Переходит к оформлению заказа
4. Если не авторизован - проходит 2FA через Telegram
5. Заполняет данные для доставки
6. Подтверждает заказ
7. Заказ появляется в админ-панели и в личном кабинете

### ИИ-Ассистент

Доступен по адресу: http://127.0.0.1:8000/ai-assistant/

**Mock-режим** (без API ключей):
- По умолчанию используется mock-ассистент
- Отвечает на базовые вопросы о товарах, ценах, доставке

**Режим с реальным API**:
В файле `smartshop/ai_assistant/views.py` измените:
```python
ai_service = AIAssistantService(use_real_api=True, provider='openai')
# или
ai_service = AIAssistantService(use_real_api=True, provider='claude')
```

## API (опционально)

Проект поддерживает Django REST Framework. API endpoints можно добавить по необходимости.

## Полезные команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Запустить сервер разработки
python manage.py runserver

# Запустить Telegram-бота
python -m smartshop.two_factor.telegram_bot

# Создать суперпользователя
python manage.py createsuperuser

# Собрать статику
python manage.py collectstatic

# Запустить тесты
python manage.py test

# Запустить shell
python manage.py shell
```

## Production Deploy

Для production рекомендуется:

1. Установить `DEBUG=False` в `.env`
2. Настроить `ALLOWED_HOSTS`
3. Использовать gunicorn вместо runserver:
   ```bash
   pip install gunicorn
   gunicorn smartshop.core.wsgi:application
   ```
4. Настроить nginx для статических файлов
5. Использовать supervisor/systemd для автозапуска
6. Настроить SSL сертификаты
7. Использовать отдельный сервер для PostgreSQL
8. Настроить резервное копирование БД

## Лицензия

MIT License

## Автор

Разработано с помощью Claude AI

## Поддержка

Если возникли вопросы или проблемы, создайте issue в репозитории.
