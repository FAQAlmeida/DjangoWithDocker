import requests as reqs
import urllib
import base64
import urllib3
import json


class Spotify:
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    API_VERSION = "v1"
    SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"
    
    #Server-side Parameters
    CLIENT_SIDE_URL = "http://127.0.0.1"
    PORT = 8080
    REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
    SCOPE = "user-library-read"
    STATE = ""
    SHOW_DIALOG_bool = True
    SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

    client_id = "bb952912f06a4e3595d24c775444d818"
    client_secret = "0caf76080f414990882c5151b34d84e5"


class SpotifyAuth(Spotify):
    def __init__(self):
        self.path = "authorize/?"
        self.response_type = "code"
        self.redirect_uri = "http://127.0.0.1:8000/spotify/callback/"
        self.scopes = "playlist-read-private user-top-read user-read-recently-played"
        self.state = ""
        self.vars = {
            "client_id": self.client_id,
            "response_type": self.response_type,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "state": self.state,
        }
        self.url_args = "&".join([f"{key}={urllib.parse.quote(val)}" for key, val in self.vars.items()])
        self.url_parsed = urllib.parse.urlparse(self.SPOTIFY_AUTH_URL)
        self.url_parsed._replace(params=urllib.parse.urlencode(self.vars))

        self.url = f"{self.SPOTIFY_AUTH_URL}/?{self.url_args}"
