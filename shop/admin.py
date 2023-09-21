from django.contrib import admin
from django.utils.html import format_html

from shop.models import Product,Category,Brand,Size,Image






admin.site.site_header = 'Online tennis shop Django'
admin.site.site_title = 'Tennis shop'
admin.site.index_title = 'Welcome to Tennis shop'
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Image)
# admin.site.register(Size)

