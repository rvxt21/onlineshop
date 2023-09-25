from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



from .views import index, catalog, product, contact, create_account, about

urlpatterns = [
    path('', index, name='index'),
    path('catalog/<slug:slug>/', catalog, name='catalog'),
    path('summernote/', include('django_summernote.urls')),
    path('product/', product, name='product'),
    path('contact/', contact, name='contact'),
    path('create_account/', create_account, name='create_account'),
    path('about/', about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)