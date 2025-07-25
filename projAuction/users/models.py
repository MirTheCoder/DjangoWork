from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import string
import random



def generate_unique_code():
    length = 8
    while True:
        #This will generate a code that is of length six and only has the ascii uppercase characters in it
        code = ''.join(random.choices(string.ascii_letters, k= length))
        if Code.objects.filter(codeName=code).count() == 0:
            break
    return code


# Create your models here.

#This is the profile model in which we will store each profile that is created in this table within our database
class Profile(models.Model):
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='auction_profile_pics', default='default.jpg')
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        # This will be used in order to send the user back to the profile page
        return reverse('updateProfile', kwargs={'pk':self.pk})

    # This will edit the size of the image of the item being auctioned off it the user wants to post an image
    # of the item on the auction post
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Whenever a user uploads an image of the object that
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"{self.person.username}'s Profile"


class Code(models.Model):
    codeName = models.CharField(max_length=8, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #Here we are going to override the save method in order to have the computer generate a unique code for the user
    #which we will use to display for them when they go to bid
    def save(self, *args, **kwargs):
        bidName = generate_unique_code()
        self.codeName = bidName
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s bidding code:{self.codeName}"





