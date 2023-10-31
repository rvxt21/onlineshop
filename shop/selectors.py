from django.db.models import QuerySet
from django.db.models import Count, Avg
from shop.models import Product, Category, Size, Brand


def lowest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('price')


def hot_deals_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('-discount')[:4]


def latest_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('-id')[:10]


def random_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('?')[:10]


def best_price_categories_selector() -> QuerySet[Category]:
    return Category.objects.\
        annotate(average_price=Avg('products__price')).\
        order_by('average_price')[:5]


def top_categories_selector() -> QuerySet[Category]:
    return Category.objects.\
        annotate(product_count=Count('products')).\
        order_by('product_count')[:5]


def filters_size_selector() -> QuerySet[Size]:
    return Size.objects.annotate(product_count=Count('products')).\
        order_by('product_count')


def filter_brand_selector() -> QuerySet[Brand]:
    return Brand.objects.annotate(product_count=Count('products')).\
        order_by('product_count')