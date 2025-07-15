from django.shortcuts import render
from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer

# Create your views here.
class RoomView(generics.CreateAPIView):
    #Tells us which table we want to get
    queryset = Room.objects.all()
    #Serializer formats the instances in room to control how we present the rooms
    serializer_class = RoomSerializer