from django.views.generic import TemplateView


# Create your views here.
class ContactUsView(TemplateView):
    template_name = 'contact.html'