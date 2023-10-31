from django.contrib import messages
from django.views.generic import TemplateView, FormView

from . models import Contact
from .forms import ContactForm

# Create your views here.


class ContactUsView(FormView):
    template_name = 'contact.html'
    model = Contact
    success_url = '/contact-us/'
    form_class = ContactForm

    def form_valid(self, form):
        contact, _ = Contact.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'name': form.cleaned_data['name'],
                'message': form.cleaned_data['message']
            }
        )
        messages.add_message(self.request,
                             messages.SUCCESS,
                             f"Thank you {form.cleaned_data.get('name').upper} "
                             f"for your message"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)