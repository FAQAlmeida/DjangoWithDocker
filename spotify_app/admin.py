from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.SpotifyUser)
admin.site.register(models.AccessToken)
