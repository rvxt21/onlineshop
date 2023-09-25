from . models import Category, Brand
from django.db.models import Count


def header_categories(request):
    categories = Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:10]
    return {
        'categories': categories
    }


def all_categories(request):
    categories_list = Category.objects.annotate(
        product_count=Count('products')).filter(product_count__gt=0)
    return {
        'categories_list': categories_list
    }


def brand_logo(request):
    brands = Brand.objects.distinct()
    return {
        'brands': brands
    }


