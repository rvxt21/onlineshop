from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from . models import Category, Product, Brand


def index(request):
    context = {}
    return render(request, 'index.html', context=context)


def catalog(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.filter(categories=category)[:16]
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'shop.html', context=context)


def product(request):
    context = {}
    return render(request, 'product-details.html', context=context)


def brand_logo(request):
    brands = Brand.objects.distinct()
    print(brands)
    context = {'brands': brands}
    return render(request, 'brands-logo.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context=context)


def create_account(request):
    context = {}
    return render(request, 'account.html', context=context)


def about(request):
    context = {}
    return render(request, 'about.html', context=context)