from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils import timezone

# Create your models here.

#This table in our database will store the auctions that are posted and made
class Auction(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to="auction_photos", null=True, blank=True)
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
    startPrice = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        # This will be used in order to call the auction-home url in order to go to the home page to view all auctions
        return reverse('auction-home')

    # This will edit the size of the image of the item being auctioned off it the user wants to post an image
    # of the item on the auction post
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#Whenever a user uploads an image of the object that
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.title

#This will be the table in our database that will store the bids made by users on auctions
class Bids(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
