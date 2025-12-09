"""
URL configuration for orders app.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:smartphone_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:smartphone_id>/', views.cart_remove, name='cart_remove'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
