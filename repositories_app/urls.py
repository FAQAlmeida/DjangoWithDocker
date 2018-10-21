from django.urls import path
from . import views

app_name="Repositories"

urlpatterns = [
    path("", views.RepositoriesView.as_view(), name="repositories"),
]