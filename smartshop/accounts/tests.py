"""
Unit tests for accounts app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserModelTest(TestCase):
    """Tests for User model."""

    def setUp(self):
        """Set up test data."""
        self.phone_number = '+79991234567'

    def test_user_creation(self):
        """Test user creation."""
        user = User.objects.create_user(phone_number=self.phone_number)

        self.assertEqual(user.phone_number, self.phone_number)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_creation(self):
        """Test superuser creation."""
        user = User.objects.create_superuser(phone_number=self.phone_number)

        self.assertEqual(user.phone_number, self.phone_number)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str_method(self):
        """Test user string representation."""
        user = User.objects.create_user(phone_number=self.phone_number)

        self.assertEqual(str(user), self.phone_number)

    def test_get_full_name_with_names(self):
        """Test get_full_name with first and last name."""
        user = User.objects.create_user(
            phone_number=self.phone_number,
            first_name='Иван',
            last_name='Иванов'
        )

        self.assertEqual(user.get_full_name(), 'Иван Иванов')

    def test_get_full_name_without_names(self):
        """Test get_full_name without names."""
        user = User.objects.create_user(phone_number=self.phone_number)

        self.assertEqual(user.get_full_name(), self.phone_number)

    def test_get_short_name_with_first_name(self):
        """Test get_short_name with first name."""
        user = User.objects.create_user(
            phone_number=self.phone_number,
            first_name='Иван'
        )

        self.assertEqual(user.get_short_name(), 'Иван')

    def test_get_short_name_without_first_name(self):
        """Test get_short_name without first name."""
        user = User.objects.create_user(phone_number=self.phone_number)

        self.assertEqual(user.get_short_name(), self.phone_number)

    def test_user_unique_phone_number(self):
        """Test that phone number is unique."""
        User.objects.create_user(phone_number=self.phone_number)

        # Try to create another user with same phone
        with self.assertRaises(Exception):
            User.objects.create_user(phone_number=self.phone_number)


class LoginViewTest(TestCase):
    """Tests for login view."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.login_url = reverse('accounts:login')

    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Вход в систему')

    def test_login_view_post_creates_user(self):
        """Test POST request creates user if not exists."""
        phone_number = '+79991234567'

        response = self.client.post(self.login_url, {
            'phone_number': phone_number
        })

        # Check user was created
        self.assertTrue(User.objects.filter(phone_number=phone_number).exists())

    def test_login_view_redirects_authenticated_user(self):
        """Test that authenticated user is redirected."""
        user = User.objects.create_user(phone_number='+79991234567')
        self.client.force_login(user)

        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 302)


class ProfileViewTest(TestCase):
    """Tests for profile view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            phone_number='+79991234567',
            first_name='Иван',
            last_name='Иванов'
        )
        self.profile_url = reverse('accounts:profile')

    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication."""
        response = self.client.get(self.profile_url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_get(self):
        """Test GET request to profile view."""
        self.client.force_login(self.user)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, self.user.phone_number)

    def test_profile_view_post_updates_user(self):
        """Test POST request updates user profile."""
        self.client.force_login(self.user)

        new_first_name = 'Петр'
        new_last_name = 'Петров'

        response = self.client.post(self.profile_url, {
            'first_name': new_first_name,
            'last_name': new_last_name,
            'phone_number': self.user.phone_number  # readonly but required
        })

        # Refresh user from database
        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, new_first_name)
        self.assertEqual(self.user.last_name, new_last_name)


class LogoutViewTest(TestCase):
    """Tests for logout view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(phone_number='+79991234567')
        self.logout_url = reverse('accounts:logout')

    def test_logout_view(self):
        """Test logout view."""
        self.client.force_login(self.user)

        # User should be authenticated
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

        # Logout
        response = self.client.get(self.logout_url)

        # Should redirect
        self.assertEqual(response.status_code, 302)

        # User should no longer be authenticated
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
