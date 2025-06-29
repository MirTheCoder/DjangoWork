from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Auction(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
