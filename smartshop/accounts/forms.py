"""
Forms for accounts app.
"""
from django import forms
from .models import User


class PhoneLoginForm(forms.Form):
    """Form for phone number login."""

    phone_number = forms.CharField(
        max_length=20,
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67',
            'required': True,
        })
    )


class OTPVerificationForm(forms.Form):
    """Form for OTP code verification."""

    otp_code = forms.CharField(
        max_length=6,
        label='Код подтверждения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456',
            'required': True,
            'maxlength': '6',
        })
    )


class ProfileForm(forms.ModelForm):
    """Form for user profile editing."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone_number': 'Номер телефона',
        }
