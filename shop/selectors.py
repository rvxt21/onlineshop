from django.db.models import QuerySet

from shop.models import Product


def lowest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('price')


def hot_deals_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('-discount')[:4]


def latest_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('-id')[:10]


def random_products_selector() -> QuerySet[Product]:
    return Product.objects.order_by('?')[:10]

