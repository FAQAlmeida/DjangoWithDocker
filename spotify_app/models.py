from django.db import models

# Create your models here.

# TODO sava my code on db, save access token for refreshing
class SpotifyUser(models.Model):
    my_code = models.CharField(max_length=150)

    def __str__(self):
        return self.my_code

class AccessToken(models.Model):
    access_token = models.CharField(max_length=300)
    token_type =models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    refresh_token = models.CharField(max_length=300)
    scope = models.CharField(max_length=200)

    def __str__(self):
        return self.access_token
