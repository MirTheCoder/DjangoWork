from django.db import models
from api.models import Room


# This will store all of our tokens for the hosts of the rooms
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150, null=True, blank=True, default=None)
    access_token = models.CharField(max_length=150, default='NO_ACCESS_TOKEN_YET', null=True, blank=True)
    expires_in = models.DateTimeField(null=True, blank=True)
    token_type = models.CharField(max_length=50, null=True, blank=True)


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


from django.db import models

# Create your models here.
