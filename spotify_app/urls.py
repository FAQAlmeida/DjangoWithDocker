from django.urls import path
from . import views

app_name="Spotify"

urlpatterns = [
    path("", views.SpotifyView.as_view(), name="spotify"),
    path("<code>", views.SpotifyView.as_view(), name="spotify"),
    path("auth/", views.SpotifyAuthView.as_view(), name="spotify_auth_view"),
    path("callback/", views.SpotifyCallback.as_view(), name="spotify_callback"),
]