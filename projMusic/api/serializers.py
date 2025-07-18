from rest_framework import serializers
from .models import Room


#Serializer is a formating tool used to control how objects within a database table are displayed, in this case
#we are passing the fields of each object that we want to display.
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')

#This serializer will check the request made by the user via frontend for making a room to make sure that it is a valid
#request and that all the required field are accurately filled out
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')