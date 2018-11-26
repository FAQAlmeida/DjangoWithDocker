import requests as reqs
import urllib
import base64
import urllib3
import json
from ..models import AccessToken
from django.utils import timezone
from datetime import timedelta


class Spotify:
    redirect_uri = "http://127.0.0.1:8000/spotify/callback/"
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    API_VERSION = "v1"
    SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

    # Server-side Parameters
    CLIENT_SIDE_URL = "http://127.0.0.1"
    PORT = 8080
    REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
    SCOPE = "user-library-read"
    STATE = ""
    SHOW_DIALOG_bool = True
    SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

    client_id = "bb952912f06a4e3595d24c775444d818"
    client_secret = "0caf76080f414990882c5151b34d84e5"
    scope = "playlist-read-private user-top-read user-read-recently-played"
    state = None
    auth_header = base64.b64encode(
        str(client_id + ':' + client_secret).encode())


class SpotifyAuth(Spotify):
    def __init__(self):
        self.path = "authorize/?"
        self.response_type = "code"
        self.state = ""
        self.vars = {
            "client_id": self.client_id,
            "response_type": self.response_type,
            "redirect_uri": self.redirect_uri,
        }
        if self.scope:
            self.vars['scope'] = self.scope
        if self.state:
            self.vars['state'] = self.state

        self.url_args = "&".join(
            [f"{key}={urllib.parse.quote(val)}" for key, val in self.vars.items()])
        self.url_parsed = urllib.parse.urlparse(self.SPOTIFY_AUTH_URL)
        self.url_parsed._replace(params=urllib.parse.urlencode(self.vars))

        self.url = f"{self.SPOTIFY_AUTH_URL}/?{self.url_args}"


class AccesToken(Spotify):
    def __init__(self, code):
        self.code = code
        self.request_body = {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": self.redirect_uri,
        }
        if self.scope:
            self.request_body['scope'] = self.scope
        if self.state:
            self.request_body['state'] = self.state

        self.request_header = {
            'Authorization': 'Basic %s' % self.auth_header.decode()
        }
        self.req = reqs.post(self.SPOTIFY_TOKEN_URL, data=self.request_body,
                             headers=self.request_header, verify=True)
        self.resp_json = self.req.json()


class RefreshingToken(Spotify):
    def __init__(self, token_data: AccessToken):
        self.token_data = token_data
        self.grant_type = "refresh_token"
        self.refresh_token = self.token_data.refresh_token
        self.request_body = {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token
        }
        self.request_header = {
            'Authorization': 'Basic %s' % self.auth_header.decode()
        }

    def update_token(self):
        req = reqs.post(self.SPOTIFY_TOKEN_URL, data=self.request_body,
                        headers=self.request_header, verify=True)
        json = req.json()
        access_token = json.get("access_token", None)
        token_type = json.get("token_type", None)
        scope = json.get("scope", None)
        expires_in = timezone.now() + timedelta(seconds=json.get("expires_in", None))
        self.token_data.access_token = access_token
        self.token_data.token_type = token_type
        self.token_data.scope = scope
        self.token_data.expires_in = expires_in
        self.token_data.save()


class GetData(Spotify):
    def __init__(self, token_data: AccessToken):
        self.end_point = "https://api.spotify.com/v1/me/top/tracks"
        self.token_data = token_data
        self.grant_type = "refresh_token"
        self.refresh_token = self.token_data.refresh_token
        self.request_header = {
            'Authorization': f"{self.token_data.token_type} {self.token_data.access_token}"
        }
        self.resp = reqs.get(
            self.end_point, headers=self.request_header, verify=True)

    @property
    def data(self):
        return self.resp.json()
