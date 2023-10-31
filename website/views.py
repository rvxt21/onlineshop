from django.contrib import messages
from django.views.generic import TemplateView, FormView

from utils.send_email import send_email
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
        send_email(
            subject='Thank you for your message!',
            to_email=[contact.email],
            message=f'We are thankful for your message {contact.name.title()}.'
                    f'Please subscribe our website to see more and to know'
                    f'more information about sales and other good opportunities.'
        )
        messages.add_message(self.request,
                             messages.SUCCESS,
                             f"Thank you "
                             f"{form.cleaned_data.get('name').upper()}"
                             f" for your message!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request,
                             messages.WARNING,
                             f"Please send correct data!"
                             )
        return super().form_invalid(form)
