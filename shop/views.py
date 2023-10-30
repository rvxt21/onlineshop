from typing import Any
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg
from . models import Category, Product, Brand
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import TemplateView, ListView, DetailView
from .selectors import lowest_price_products_selector, \
    hot_deals_products_selector, latest_products_selector,\
    random_products_selector


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'hot_deals_products': hot_deals_products_selector(),
            'latest_products': latest_products_selector(),
            'lowest_price_products': lowest_price_products_selector(),
            'random_products': random_products_selector()
        }
        return context


class CatalogView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 16

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Product.objects.filter(categories=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['category'] = category
        return context


class ProductView(DetailView):
    template_name = 'product-details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_product = context['product']
        sizes = single_product.size.all() if hasattr(single_product,
                                                     'size') else None
        categories = single_product.categories.all()
        related_products = Product.objects.filter(
            categories__in=single_product.categories.all()).\
        exclude(id=single_product.id).order_by('?')[:7]
        context |={
            'product': single_product,
            'sizes':sizes,
            'categories': categories,
            'related_products': related_products,
            'lowest_price_products': lowest_price_products_selector()[:4]
        }
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


def header_categories(request):
    top_categories = Category.objects.\
        annotate(product_count=Count('products')).\
        order_by('product_count')[:5]
    best_price_categories = Category.objects.\
        annotate(average_price=Avg('products__price')).\
        order_by('average_price')[:5]
    context = {
        'categories': top_categories,
        'best_price_categories': best_price_categories
    }





