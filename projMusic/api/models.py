from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        #This will generate a code that is of length six and only has the ascii uppercase characters in it
        code = ''.join(random.choices(string.ascii_uppercase, k= length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code

# Create your models here.
class Room(models.Model):
    #Whenever we create a new room, the table will by default call 'generate_unique_code' to create a default code
    # for the room
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(default=1,null=False)
    #This will allow the database to automatically add the current date time whenever a room is created
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, blank=True, null=True)