from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextField
from django.utils import timezone
from PIL import Image


# Create your models here.
class Profile(models.Model):
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    uname = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)




