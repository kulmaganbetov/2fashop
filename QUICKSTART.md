# Быстрый старт SmartShop

## Минимальная установка (5 минут)

### 1. Установка зависимостей

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate для Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Запуск PostgreSQL

```bash
# Запустить Docker контейнер с PostgreSQL
docker-compose up -d

# Подождать несколько секунд пока БД запустится
```

### 3. Настройка базы данных

```bash
# Создать таблицы
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser
# Введите номер телефона: +79991234567
```

### 4. Запуск проекта

```bash
# Запустить Django-сервер
python manage.py runserver
```

Откройте браузер: http://127.0.0.1:8000

## Базовое использование без Telegram

Если у вас нет токена Telegram-бота, вы всё равно можете:

1. ✅ Просматривать каталог товаров
2. ✅ Добавлять товары в корзину
3. ✅ Использовать админ-панель (http://127.0.0.1:8000/admin/)
4. ✅ Использовать ИИ-ассистента в mock-режиме

⚠️ **Без Telegram-бота не работает:**
- Регистрация и вход для обычных пользователей (требуется 2FA)
- Оформление заказов (требуется авторизация)

Для полного функционала настройте Telegram-бота (см. README.md).

## Добавление тестовых данных

### Через админ-панель

1. Войдите: http://127.0.0.1:8000/admin/
2. Создайте категорию: "Смартфоны" → "Категории" → "Добавить"
3. Создайте товар: "Смартфоны" → "Смартфоны" → "Добавить"

### Через Django shell

```bash
python manage.py shell
```

```python
from smartshop.shop.models import Category, Smartphone

# Создать категорию
category = Category.objects.create(
    name='Флагманы',
    slug='flagmany',
    description='Топовые смартфоны'
)

# Создать товар
smartphone = Smartphone.objects.create(
    name='iPhone 15 Pro Max',
    slug='iphone-15-pro-max',
    category=category,
    brand='Apple',
    model='iPhone 15 Pro Max',
    description='Новейший флагман от Apple с чипом A17 Pro',
    price=129990,
    stock=10,
    screen_size='6.7"',
    ram='8 GB',
    storage='256 GB',
    battery='4422 mAh',
    camera='48 MP + 12 MP + 12 MP',
    processor='Apple A17 Pro',
    os='iOS 17',
    available=True
)

print("Товар создан!")
```

## Настройка Telegram-бота (опционально)

### Получить токен бота

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте `/newbot`
4. Следуйте инструкциям
5. Скопируйте токен

### Добавить токен

Отредактируйте `.env`:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Запустить бота

В **отдельном терминале**:

```bash
python run_bot.py
```

### Привязать номер телефона

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Отправьте `/link`
4. Введите номер: `+79991234567`
5. Готово!

## Проверка работы

### Каталог
http://127.0.0.1:8000/catalog/

### ИИ-ассистент
http://127.0.0.1:8000/ai-assistant/

### Админка
http://127.0.0.1:8000/admin/

### Корзина
http://127.0.0.1:8000/orders/cart/

## Возможные проблемы

### Ошибка подключения к БД

```
django.db.utils.OperationalError: could not connect to server
```

**Решение:**
- Проверьте что Docker запущен: `docker ps`
- Перезапустите контейнер: `docker-compose restart`

### Модуль не найден

```
ModuleNotFoundError: No module named 'django'
```

**Решение:**
- Активируйте виртуальное окружение
- Установите зависимости: `pip install -r requirements.txt`

### Порт уже занят

```
Error: That port is already in use.
```

**Решение:**
- Используйте другой порт: `python manage.py runserver 8001`
- Или остановите процесс на порту 8000

## Следующие шаги

1. ✅ Добавьте товары через админку
2. ✅ Настройте Telegram-бота
3. ✅ Попробуйте оформить заказ
4. ✅ Протестируйте ИИ-ассистента
5. ✅ Изучите код и кастомизируйте под свои нужды

Подробная документация в README.md
