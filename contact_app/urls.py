from django.contrib import admin
from django.urls import path

from . import views

app_name = "Contact"

urlpatterns = [
    path('', views.ContactView.as_view(), name='email'),
    path('success/', views.SuccessView.as_view(), name='success'),
]