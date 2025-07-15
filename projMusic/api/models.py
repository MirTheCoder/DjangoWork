from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        #This will generate a code that is of length six and only has the ascii upercase characters in it
        code = ''.join(random.choices(string.ascii_uppercase, k= length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code

# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default='', unique=True)
    host = models.CharField(max_length=50, unique=True, null=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    vote_to_skip = models.IntegerField(default=1,null=False)
    #This will allow the database to automatically add the current date time whenever a room is created
    created_at = models.DateTimeField(auto_now_add=True)