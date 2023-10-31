from django.urls import path, include
from . views import ContactUsView

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact'),
]