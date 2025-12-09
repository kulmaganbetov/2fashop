"""
Views for shop app.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Smartphone, Category


def index_view(request):
    """Home page with featured products."""
    smartphones = Smartphone.objects.filter(available=True)[:8]
    categories = Category.objects.all()

    context = {
        'smartphones': smartphones,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)


def catalog_view(request):
    """Catalog page with all products."""
    smartphones_list = Smartphone.objects.filter(available=True)

    # Search functionality
    query = request.GET.get('q')
    if query:
        smartphones_list = smartphones_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        smartphones_list = smartphones_list.filter(category__slug=category_slug)

    # Price sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        smartphones_list = smartphones_list.order_by('price')
    elif sort == 'price_desc':
        smartphones_list = smartphones_list.order_by('-price')
    elif sort == 'name':
        smartphones_list = smartphones_list.order_by('name')

    # Pagination
    paginator = Paginator(smartphones_list, 12)
    page_number = request.GET.get('page')
    smartphones = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'smartphones': smartphones,
        'categories': categories,
        'query': query,
        'current_category': category_slug,
        'current_sort': sort,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail_view(request, slug):
    """Product detail page."""
    smartphone = get_object_or_404(Smartphone, slug=slug, available=True)

    # Get related products from same category
    related_products = Smartphone.objects.filter(
        category=smartphone.category,
        available=True
    ).exclude(id=smartphone.id)[:4]

    context = {
        'smartphone': smartphone,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


def category_detail_view(request, slug):
    """Category page."""
    category = get_object_or_404(Category, slug=slug)
    smartphones_list = Smartphone.objects.filter(category=category, available=True)

    # Pagination
    paginator = Paginator(smartphones_list, 12)
    page_number = request.GET.get('page')
    smartphones = paginator.get_page(page_number)

    context = {
        'category': category,
        'smartphones': smartphones,
    }
    return render(request, 'shop/category_detail.html', context)
