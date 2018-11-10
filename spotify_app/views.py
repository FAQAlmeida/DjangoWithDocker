from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
from .authentication import auth

# Create your views here.
class SpotifyView(generic.View):
    template_name = "spotify_app/spotify.html"

    def get(self, request, req=None):
        http_resp = render(request, self.template_name)
        http_resp.set_cookie("req", request)
        return http_resp


class SpotifyAuthView(generic.View):
    def get(self, request):
        spotify_auth = auth.SpotifyAuth()
        return redirect(spotify_auth.url)


class SpotifyCallback(generic.View):
    template_name = "spotify_app/spotify.html"

    def get(self, request):
        return redirect("Spotify:spotify")
