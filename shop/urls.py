from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



from .views import index,catalog

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)