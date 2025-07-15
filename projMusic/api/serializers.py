from rest_framework import serializers
from .models import Room


#Serializer is a formating tool used to control how obejcts within a database table are displayed, in this case
#we are passing the fields of each object that we want to display.
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause', 'vote_to_skip', 'created_at')