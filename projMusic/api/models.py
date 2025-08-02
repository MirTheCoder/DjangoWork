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

def generate_unique_number():
    length = 8
    i = 0
    code = ""
    while True:
        while i < length:
            #This will add a random value between 0 and 9 (with 0 and 9 included) to add to our code string
            code += str(random.randrange(10))
            i += 1
        code = int(code)
        if UsersInRoom.objects.filter(user_code=code).count() == 0:
            break
        else:
            code = ""
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
    #This will handle if a user can join a room directly or if they need to be admitted by the user
    admit_required = models.BooleanField(default=False, null=True, blank=True)

#This will be used to keep track of which users are in which room
class UsersInRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.JSONField(null=True, blank=True)
    #This tells our database table to automatically save the current time stamp at the creation of an instance within
    # this datatable to the created_at field in this datatable
    created_at = models.DateTimeField(auto_now_add=True)
    #Each user when added to a room will get a unique number
    user_code = models.IntegerField(default=generate_unique_number, unique=True)

class Requests(models.Model):
    #This is required in order to store the session data of a user
    user_requesting = models.JSONField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)