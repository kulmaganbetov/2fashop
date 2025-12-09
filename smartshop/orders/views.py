"""
Views for orders app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from smartshop.shop.models import Smartphone
from .models import Order, OrderItem
from .cart import Cart
from .forms import OrderCreateForm, CartAddProductForm


def cart_detail(request):
    """Cart detail view."""
    cart = Cart(request)

    # Add form for each cart item
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True}
        )

    return render(request, 'orders/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, smartphone_id):
    """Add product to cart."""
    cart = Cart(request)
    smartphone = get_object_or_404(Smartphone, id=smartphone_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            smartphone=smartphone,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
        messages.success(request, f'{smartphone.name} добавлен в корзину!')

    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, smartphone_id):
    """Remove product from cart."""
    cart = Cart(request)
    smartphone = get_object_or_404(Smartphone, id=smartphone_id)
    cart.remove(smartphone)
    messages.success(request, 'Товар удалён из корзины.')

    return redirect('orders:cart_detail')


@login_required
def order_create(request):
    """Create order from cart."""
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, 'Корзина пуста!')
        return redirect('shop:catalog')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    smartphone=item['smartphone'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart
            cart.clear()

            messages.success(request, f'Заказ #{order.id} успешно оформлен!')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone_number,
        }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})


@login_required
def order_detail(request, order_id):
    """Order detail view."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
