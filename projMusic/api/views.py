from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

#the 'generics.CreateApiView' is a preset page view that will display all the instances of a table in the database
#(similar to a ListView
#It also works as a create page that allows you to create an instance of the table of interest
class RoomView(generics.ListAPIView):
    #Tells us which table we want to get
    queryset = Room.objects.all()
    #Serializer formats the instances in room to control how we present the rooms
    serializer_class = RoomSerializer

#APIView allows us to override some request methods, when a request method 'GET, POST, or even PUT' is made,
#the apiview will check the type and dispatch it to the function that handles that type of method
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        #We are checking to see if the current user has an active session with the web server
        if not self.request.session.exists(self.request.session.session_key):
            #We will create a session for the user if they do not have an active one running
            self.request.session.create()
        #This will take our data, serialize it and then check to see if the data that was sent to us is valid. This will
        #only check the data corresponding to the fields of interest that we put into our CreateRoomSerializer
        serializer = self.serializer_class(data=request.data)
        #Here we check to see if the fields of interest have valid data in them
        if serializer.is_valid():
            guest_can_pause = serializer.validated_data.get('guest_can_pause')
            votes_to_skip = serializer.validated_data.get('votes_to_skip')
            host = self.request.session.session_key
            #Here, we check and see, if the user who is currently active has a room already made, and if they do then we
            #will just transport them back to their room but with the 'guest_can_pause' and 'votes_to_skip' details
            #being changed
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                #We use this line of code to update and existing room within our Rooms table in our database
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                #We will just create a new room if the user in session does not already have an active room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
             #This will send the room data using the RoomSerializer for formatting purposes
            #data will turn the data we receive from the RoomSerializer into json data
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwargs = 'code'

    def get(self, request, format=None):
        #This will give us the variables within our parameter, and it looks specifically for the one that matches the
        #variable name
        code = request.GET.get(self.lookup_url_kwargs)
        if code is not None:
            #Here, we cross-reference our database with the code given in the parameter to see exactly which room
            #has a code that matches the code given in the request url
            room = Room.objects.filter(code=code).first()
            if room:
                #This will allow us to get all the fields pertaining to the room
                data = RoomSerializer(room).data
                data['is_host'] = self.request.session.session_key == room.host
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):

    lookup_url_kwarg = 'code'
    #This is where we define the request that is being sent, or the type of request we will receive
    def post(self, request, format=None):
        # We are checking to see if the current user has an active session with the web server
        if not self.request.session.exists(self.request.session.session_key):
            # We will create a session for the user if they do not have an active one running
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code is not None:
            room = Room.objects.filter(code=code).first()
            if room:
                #We wil use this to ensure that the system knows that this user has successfully joined the room
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined'}, status=status.HTTP_200_OK)
            else:
                return Response({"BadRequest": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'BadRequest': "Invalid post data, did not find a 'code key'"}, status=status.HTTP_400_BAD_REQUEST)

#This function will allow us to check and see if the user is already in a room
class UserInRoom(APIView):
    def get(self,request,format=None):
        # We are checking to see if the current user has an active session with the web server
        if not self.request.session.exists(self.request.session.session_key):
            # We will create a session for the user if they do not have an active one running
            self.request.session.create()
        #Here we will send to the room code attached to the users session (whether they have one or not)
        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self,request, format=None):
        #We will check and see if the room code is attached to the users session in order
        #to remove the user from the room
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            #If the user is the host of the room, then we will delete the room
            room = Room.objects.filter(host=host_id).first()
            if room:
                room.delete()

            return Response({"Message": "You have successfully been removed from the room"}, status=status.HTTP_200_OK)
        return Response({"Bad Request": "You are not currently in a room"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    #Patch is another word for update, a way to update something that already exist (kind of like a put method)
    def patch(self, request, format=None):
        # We are checking to see if the current user has an active session with the web server
        if not self.request.session.exists(self.request.session.session_key):
            # We will create a session for the user if they do not have an active one running
            self.request.session.create()
        #Here we will get the data from the request and input it into our serializer_class in order to get the fields
        #values corresponding to the data
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            #Check to see if the room even exist
            room = Room.objects.filter(code=code).first()
            if not room:
                return Response({"msg": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

            #Check to see if the person requesting to update the room is the host or not
            user_id = self.request.session.session_key
            if room.host is not user_id:
                return Response({"Unauthorized": "You are not the host of this room"}, status=status.HTTP_403_FORBIDDEN)

            #If the room exist and the person requesting to edit the room is the host then we will edit the values
            #or fields of the room
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request', "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)