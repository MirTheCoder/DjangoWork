
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    #This creates a one to one ratio that connects users to their profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #You need to first install "Pillow" before you can use the Image Field within your database
    #Side note: the good thing is that
    image = models.ImageField(default='default.jpg', upload_to='profile.pics')

    def __str__(self):
        return f"{self.user.username} Profile"