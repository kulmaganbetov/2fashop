"""
URL configuration for shop app.
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
]
