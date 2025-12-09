"""
Services for two-factor authentication.
"""
import random
import string
from django.conf import settings
from .models import OTPCode, TelegramUser
from .telegram_bot import send_otp_code


class OTPService:
    """Service for managing OTP codes."""

    @staticmethod
    def generate_code(length=6):
        """Generate random OTP code."""
        return ''.join(random.choices(string.digits, k=length))

    def generate_and_send_otp(self, phone_number):
        """Generate OTP code and send via Telegram."""
        # Invalidate all previous codes for this phone number
        OTPCode.objects.filter(phone_number=phone_number, is_used=False).update(is_used=True)

        # Generate new code
        code = self.generate_code()

        # Get Telegram ID for this phone number
        try:
            telegram_user = TelegramUser.objects.get(phone_number=phone_number)
            telegram_id = telegram_user.telegram_id
        except TelegramUser.DoesNotExist:
            telegram_id = None

        # Save OTP code
        otp = OTPCode.objects.create(
            phone_number=phone_number,
            code=code,
            telegram_id=telegram_id
        )

        # Send code via Telegram
        if telegram_id:
            success = send_otp_code(telegram_id, code)
            return success
        else:
            # If no Telegram ID, we can't send the code
            # In real app, you might want to send SMS or show error
            print(f"Warning: No Telegram ID for phone {phone_number}")
            print(f"OTP Code (for testing): {code}")
            return False

    def verify_otp(self, phone_number, code):
        """Verify OTP code."""
        try:
            otp = OTPCode.objects.filter(
                phone_number=phone_number,
                code=code,
                is_used=False
            ).latest('created_at')

            if otp.is_valid():
                otp.is_used = True
                otp.save()
                return True

        except OTPCode.DoesNotExist:
            pass

        return False

    @staticmethod
    def link_telegram_account(phone_number, telegram_id, username=None, first_name=None, last_name=None):
        """Link phone number to Telegram account."""
        telegram_user, created = TelegramUser.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'telegram_id': telegram_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        return telegram_user
