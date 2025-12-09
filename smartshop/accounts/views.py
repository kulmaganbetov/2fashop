"""
Views for accounts app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import PhoneLoginForm, OTPVerificationForm, ProfileForm
from .models import User
from smartshop.two_factor.services import OTPService


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle phone number login and OTP request."""
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            # Get or create user
            user, created = User.objects.get_or_create(phone_number=phone_number)

            # Generate and send OTP
            otp_service = OTPService()
            success = otp_service.generate_and_send_otp(phone_number)

            if success:
                # Store phone number in session for verification
                request.session['pending_phone'] = phone_number
                messages.success(request, 'Код подтверждения отправлен в Telegram!')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'Ошибка отправки кода. Проверьте, что вы подписаны на бота.')
    else:
        form = PhoneLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def verify_otp_view(request):
    """Verify OTP code and log in user."""
    phone_number = request.session.get('pending_phone')
    if not phone_number:
        messages.error(request, 'Сессия истекла. Пожалуйста, начните заново.')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']

            # Verify OTP
            otp_service = OTPService()
            if otp_service.verify_otp(phone_number, otp_code):
                # Get user and log in
                try:
                    user = User.objects.get(phone_number=phone_number)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    # Clear session data
                    del request.session['pending_phone']

                    messages.success(request, 'Вы успешно вошли в систему!')
                    next_url = request.GET.get('next', 'shop:index')
                    return redirect(next_url)
                except User.DoesNotExist:
                    messages.error(request, 'Пользователь не найден.')
            else:
                messages.error(request, 'Неверный код или код истёк.')
    else:
        form = OTPVerificationForm()

    return render(request, 'accounts/verify_otp.html', {
        'form': form,
        'phone_number': phone_number
    })


@login_required
def logout_view(request):
    """Log out user."""
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('shop:index')


@login_required
def profile_view(request):
    """View and edit user profile."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def orders_history_view(request):
    """View user's order history."""
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'accounts/orders_history.html', {'orders': orders})
