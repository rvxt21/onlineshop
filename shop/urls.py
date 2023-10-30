from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . views import IndexView, CatalogView, product, contact, about

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/<slug:slug>/', CatalogView.as_view(), name='catalog'),
    path('summernote/', include('django_summernote.urls')),
    path('product/<slug:slug>/', product, name='product'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)