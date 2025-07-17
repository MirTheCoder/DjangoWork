from django.shortcuts import render
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

#the 'generics.CreateApiView' is a preset page view that will display all the instances of a table in the database
#(similar to a ListView
#It also works as a create page that allows you to create an instance of the table of interest
class RoomView(generics.CreateAPIView):
    #Tells us which table we want to get
    queryset = Room.objects.all()
    #Serializer formats the instances in room to control how we present the rooms
    serializer_class = RoomSerializer