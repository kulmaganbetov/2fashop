"""
Unit tests for two_factor app.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import OTPCode, TelegramUser
from .services import OTPService


class OTPCodeModelTest(TestCase):
    """Tests for OTPCode model."""

    def setUp(self):
        """Set up test data."""
        self.phone_number = '+79991234567'

    def test_otp_creation(self):
        """Test OTP code creation."""
        otp = OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456'
        )

        self.assertEqual(otp.phone_number, self.phone_number)
        self.assertEqual(otp.code, '123456')
        self.assertFalse(otp.is_used)
        self.assertIsNotNone(otp.expires_at)

    def test_otp_is_valid_when_not_used_and_not_expired(self):
        """Test OTP is valid when not used and not expired."""
        otp = OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456'
        )

        self.assertTrue(otp.is_valid())

    def test_otp_is_invalid_when_used(self):
        """Test OTP is invalid when already used."""
        otp = OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456',
            is_used=True
        )

        self.assertFalse(otp.is_valid())

    def test_otp_is_invalid_when_expired(self):
        """Test OTP is invalid when expired."""
        otp = OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456'
        )
        # Manually set expiration to past
        otp.expires_at = timezone.now() - timedelta(minutes=1)
        otp.save()

        self.assertFalse(otp.is_valid())


class OTPServiceTest(TestCase):
    """Tests for OTPService."""

    def setUp(self):
        """Set up test data."""
        self.service = OTPService()
        self.phone_number = '+79991234567'

    def test_generate_code(self):
        """Test OTP code generation."""
        code = self.service.generate_code()

        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_verify_otp_with_valid_code(self):
        """Test OTP verification with valid code."""
        # Create OTP
        code = '123456'
        OTPCode.objects.create(
            phone_number=self.phone_number,
            code=code
        )

        # Verify
        result = self.service.verify_otp(self.phone_number, code)

        self.assertTrue(result)

        # Check that OTP is marked as used
        otp = OTPCode.objects.get(phone_number=self.phone_number, code=code)
        self.assertTrue(otp.is_used)

    def test_verify_otp_with_invalid_code(self):
        """Test OTP verification with invalid code."""
        # Create OTP
        OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456'
        )

        # Verify with wrong code
        result = self.service.verify_otp(self.phone_number, '654321')

        self.assertFalse(result)

    def test_verify_otp_with_expired_code(self):
        """Test OTP verification with expired code."""
        # Create expired OTP
        otp = OTPCode.objects.create(
            phone_number=self.phone_number,
            code='123456'
        )
        otp.expires_at = timezone.now() - timedelta(minutes=1)
        otp.save()

        # Verify
        result = self.service.verify_otp(self.phone_number, '123456')

        self.assertFalse(result)

    def test_link_telegram_account(self):
        """Test linking Telegram account to phone number."""
        telegram_id = 123456789
        username = 'testuser'
        first_name = 'Test'
        last_name = 'User'

        telegram_user = OTPService.link_telegram_account(
            phone_number=self.phone_number,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(telegram_user.phone_number, self.phone_number)
        self.assertEqual(telegram_user.telegram_id, telegram_id)
        self.assertEqual(telegram_user.username, username)
        self.assertEqual(telegram_user.first_name, first_name)
        self.assertEqual(telegram_user.last_name, last_name)


class TelegramUserModelTest(TestCase):
    """Tests for TelegramUser model."""

    def test_telegram_user_creation(self):
        """Test Telegram user creation."""
        telegram_user = TelegramUser.objects.create(
            phone_number='+79991234567',
            telegram_id=123456789,
            username='testuser'
        )

        self.assertEqual(telegram_user.phone_number, '+79991234567')
        self.assertEqual(telegram_user.telegram_id, 123456789)
        self.assertEqual(telegram_user.username, 'testuser')

    def test_telegram_user_unique_phone(self):
        """Test that phone number is unique."""
        TelegramUser.objects.create(
            phone_number='+79991234567',
            telegram_id=123456789
        )

        # Try to create another user with same phone
        with self.assertRaises(Exception):
            TelegramUser.objects.create(
                phone_number='+79991234567',
                telegram_id=987654321
            )

    def test_telegram_user_unique_telegram_id(self):
        """Test that Telegram ID is unique."""
        TelegramUser.objects.create(
            phone_number='+79991234567',
            telegram_id=123456789
        )

        # Try to create another user with same Telegram ID
        with self.assertRaises(Exception):
            TelegramUser.objects.create(
                phone_number='+79999999999',
                telegram_id=123456789
            )
