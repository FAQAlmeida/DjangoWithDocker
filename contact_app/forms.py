from django import forms
from django.core.mail import send_mail as s_e
from django.core.mail import EmailMessage


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
        # send email using the self.cleaned_data dictionary
        email = EmailMessage()
        name = self.cleaned_data["contact_name"]
        content = self.cleaned_data["content"]
        from_email = self.cleaned_data["contact_email"]
        subject = self.cleaned_data["subject"]
        email.body = content
        email.subject = subject
        email.from_email = f"{name} <{from_email}>"
        email.to = ["otavioalmeida650@gmail.com"]
        email.extra_headers = {"labelIds": ["CATEGORY_SOCIAL"]}
        email.send()

