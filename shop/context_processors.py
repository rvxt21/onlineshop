from . models import Category, Brand
from django.db.models import Count


def header_categories(request):
    categories = Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:10]
    return {
        'categories': categories
    }


def brand_logo(request):
    brands = Brand.objects.distinct()
    return {
        'brands': brands
    }