"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    """Form for creating new users in admin."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'telegram_id', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for updating users in admin."""
    password = ReadOnlyPasswordHashField(
        label='Пароль',
        help_text=(
            'Пароли хранятся в зашифрованном виде. '
            '<a href="../password/">Изменить пароль</a>.'
        )
    )

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin panel for custom User model."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'first_name', 'last_name', 'telegram_id', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('phone_number', 'first_name', 'last_name', 'telegram_id')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'telegram_id')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'telegram_id', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)
