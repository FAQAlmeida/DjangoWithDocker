from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import FormView
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactEmail

# Create your views here.


class ContactView(FormView):
    form_class = ContactEmail
    success_url = "success"
    template_name = "contact_app/contact.html"

    def form_valid(self, form:ContactEmail):
        form.send_email()
        return super().form_valid(form)

class SuccessView(generic.View):
    template_name = "contact_app/success.html"
    def get(self, request):
        return render(request, self.template_name)
