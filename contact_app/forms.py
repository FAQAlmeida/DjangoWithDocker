from django import forms
from django.core.mail import send_mail as s_e
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

import json


class ContactEmail(forms.Form):
    contact_name = forms.CharField(required=True, label="Seu nome")
    contact_email = forms.EmailField(required=True, label="Seu e-mail")
    subject = forms.CharField(required=True, label="Qual o assunto?")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label="Diga algo legal😅"
    )

    def send_email(self):
        email = EmailMultiAlternatives()
        
        name = self.cleaned_data["contact_name"]
        content = self.cleaned_data["content"]
        from_email = self.cleaned_data["contact_email"]
        subject = self.cleaned_data["subject"]

        context = {"data": {"name": name,
                            "content": content, "from": from_email}}

        template_text = render_to_string("contact_app/email.txt", context)
        template_html = render_to_string("contact_app/email.html", context)

        email.reply_to = [from_email]
        email.subject = subject
        email.from_email = f"{name} <{from_email}>"
        email.to = ["otavioalmeida650@gmail.com"]
        email.body = template_text
        email.attach_alternative(template_html, "text/html")
        email.send()
