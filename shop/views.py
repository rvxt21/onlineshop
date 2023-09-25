from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from . models import Category, Product, Brand
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def index(request):
    products_main = Product.objects.order_by('-price')[:4]
    products_latest = Product.objects.order_by('price')[:9]
    context = {
        'products_main': products_main,
        'products_latest': products_latest
    }
    return render(request, 'index.html', context=context)


def catalog(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.filter(categories=category)[:16]
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'shop.html', context=context)


def product(request, **kwargs):
    single_product = get_object_or_404(Product, slug=kwargs.get('slug'))
    sizes = single_product.size.all() if hasattr(single_product,
                                                 'size') else None
    categories = single_product.categories.all()
    context = {
        'product': single_product,
        'sizes': sizes,
        'categories': categories,
    }
    return render(request, 'product-details.html', context=context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context=context)


def create_account(request):
    context = {}
    return render(request, 'account.html', context=context)


def about(request):
    context = {}
    return render(request, 'about.html', context=context)





