import django
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from datetime import timedelta

from .authentication import auth
from .models import AccessToken
from .models import SpotifyUser

# Create your views here.


class SpotifyView(generic.View):
    template_name = "spotify_app/spotify.html"

    def get(self, request):
        try:
            token = AccessToken.objects.first()
        except ObjectDoesNotExist:
            redirect(resolve_url("Spotify:spotify_auth_view"))

        if token.expires_in <= timezone.now():
            rt = auth.RefreshingToken(token)
            rt.update_token()
            token = AccessToken.objects.get(pk=token.pk)

        data = auth.GetData(token).data

        http_resp = render(request, self.template_name,
                           {"data": data.get("items"), "token": token})
        http_resp.set_cookie(key="data", value=data.get("items", None))
        return http_resp


class SpotifyAuthView(generic.View):
    def get(self, request):
        spotify_auth = auth.SpotifyAuth()
        return redirect(spotify_auth.url)


class SpotifyCallback(generic.View):
    template_name = "spotify_app/spotify.html"

    def get(self, request):
        code = request.GET.get("code", None)
        sp_toke_obj = auth.AccesToken(code)
        json = sp_toke_obj.resp_json
        now = timezone.now()
        date_expire = now + timedelta(seconds=json.get("expires_in", None))
        token = AccessToken()
        token.access_token = json.get("access_token", None)
        token.refresh_token = json.get("refresh_token", None)
        token.token_type = json.get("token_type", None)
        token.scope = json.get("scope", None)
        token.expires_in = date_expire
        token.save()

        return redirect("Spotify:spotify")
