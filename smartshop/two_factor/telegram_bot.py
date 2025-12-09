"""
Telegram bot for sending OTP codes.
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot application
bot_application = None


def get_bot_application():
    """Get or create bot application."""
    global bot_application
    if bot_application is None and settings.TELEGRAM_BOT_TOKEN:
        bot_application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    return bot_application


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    welcome_message = f"""
Добро пожаловать в SmartShop, {user.first_name}!

Этот бот используется для двухфакторной аутентификации на сайте.

Для привязки вашего аккаунта к номеру телефона:
1. Отправьте /link
2. Введите ваш номер телефона в формате: +79991234567

После этого вы сможете получать коды подтверждения при входе на сайт.
    """
    await update.message.reply_text(welcome_message)


async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /link command."""
    await update.message.reply_text(
        "Отправьте ваш номер телефона в формате: +79991234567"
    )
    context.user_data['awaiting_phone'] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    from asgiref.sync import sync_to_async

    user = update.effective_user
    text = update.message.text

    # Check if we're waiting for phone number
    if context.user_data.get('awaiting_phone'):
        phone_number = text.strip()

        # Basic validation
        if phone_number.startswith('+') and len(phone_number) >= 11:
            # Import here to avoid circular imports
            from .services import OTPService

            # Link Telegram account (use sync_to_async for Django ORM)
            await sync_to_async(OTPService.link_telegram_account)(
                phone_number=phone_number,
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )

            await update.message.reply_text(
                f"✅ Ваш номер {phone_number} успешно привязан!\n\n"
                f"Теперь вы можете использовать его для входа на сайт."
            )
            context.user_data['awaiting_phone'] = False
        else:
            await update.message.reply_text(
                "❌ Неверный формат номера телефона.\n"
                "Используйте формат: +79991234567"
            )
    else:
        await update.message.reply_text(
            "Используйте команду /start для начала работы."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
Доступные команды:

/start - Начать работу с ботом
/link - Привязать номер телефона
/help - Показать эту справку

Для входа на сайт:
1. Привяжите ваш номер телефона командой /link
2. На сайте введите ваш номер телефона
3. Получите код подтверждения в этом чате
4. Введите код на сайте
    """
    await update.message.reply_text(help_text)


def send_otp_code(telegram_id, code):
    """Send OTP code to Telegram user."""
    try:
        application = get_bot_application()
        if application is None:
            logger.error("Bot application not initialized")
            return False

        # Send message synchronously
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def send_message():
            await application.bot.send_message(
                chat_id=telegram_id,
                text=f"🔐 Ваш код подтверждения: {code}\n\n"
                     f"Код действителен {settings.OTP_EXPIRY_MINUTES} минут."
            )

        loop.run_until_complete(send_message())
        loop.close()
        return True

    except Exception as e:
        logger.error(f"Error sending OTP to {telegram_id}: {e}")
        return False


def run_bot():
    """Run the Telegram bot."""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not configured")
        return

    application = get_bot_application()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("link", link_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    run_bot()
