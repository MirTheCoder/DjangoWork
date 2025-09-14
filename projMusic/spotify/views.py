import base64

from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from .credentials import REDIRECT_URI,CLIENT_ID,CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
#Allows us to import everything from the util file
from .util import *
from .models import *
from api.models import Room
import os



#This will construct the url that we use to send the user to the spotify authentication page
class AuthURL(APIView):
    def get(self, request, format=None):
        print(f"Client ID value: {CLIENT_ID}")
        #This is the information that we are asking from the user regarding their spotify account
        #make sure that in this scope, you include everything that you want from the users account
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private'
        #Here we are constructing a url to use to reach spotify with our request
        url = Request('GET', "https://accounts.spotify.com/authorize", params={
            'scope': scopes,
            #this allows us to retrieve an authorization code back from the spotify end
            'response_type': 'code',
            #This tells spotify where to send the information to
            'redirect_uri': REDIRECT_URI,
            #This identifies our app to spotify
            'client_id': CLIENT_ID,
        }). prepare().url
        #Since this call will be made from the frontend, we want to return this back to the front end
        return Response({'url': url}, status=status.HTTP_200_OK)

#This will tell our csrf security to not block any incoming request from outside the server that are calling this
# function
@csrf_exempt
def spotify_callback(request,format=None):
    #We will use this in order to retrieve the response from spotify
    code = request.GET.get('code')
    error = request.GET.get('error')
    #This will allow our app to authenticate itself so that it can now request tokens and data
    #it allows spotify to know exactly which app is requesting its services and the client secret passed into it
    #shows that we are authorized because only we should know the client secret
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    #We are going to use this to reach out to spotify in order to get the access tokens to the account requested in
    #exchange for the authorization code that it gave us
    response = post('https://accounts.spotify.com/api/token', headers={
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"},
    data={
        #This it the type of grant that we want, we are supplying the spotify server with the code we got from the authurl
        #in order to get the needed access tokens and data required. Make sure to pass the code in the post request to
        #the spotify server
        'grant_type': 'authorization_code', #'authorization_code' because we are going to give spotify a code in exchange for data
        'code': code,
        'client_secret': CLIENT_SECRET,
        #Make sure that the redirect uri in this callback function post request matches the one in the get request
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,

    }).json() #We will convert the response we receive from our post request into json data


    #We will store within variables the various fields of our response that we get from spotify after sending
    #our post request
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
         request.session.create()
         user_id = request.session.session_key
    else:
        user_id = request.session.session_key

    update_or_create_user_tokens(user_id, access_token, token_type, expires_in, refresh_token)
    #After the request has been passed, and we do what we need to do with the information returned to us, we will
    #then go back to our frontend file
    return redirect('frontend:')

#Used to see whether the user is authenticated
class IsAuthenticated(APIView):
    def get(self,request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        if is_authenticated:
            return Response({'status':"is authenticated"}, status=status.HTTP_200_OK)
        else:
            return False

class CurrentSong(APIView):
    def get(self,request,format=json):
        if not request.session.exists:
            request.session.create()
        #This is made to check exactly which room the user is in
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        if not room:
            return Response({"Invalid Room": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        #Because this is a get request, we don't have to set the put of post request as True, we can leave them as their
        #default values which is 'False'
        response = execute_spotify_api_request(host, endpoint)
        #This will return nothing to the front end if there is content then we will ignore this and just get the
        #details we are interested in
        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        #These are the data of interest that we want to get and send to the frontend
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')
        artist_string = ""

        #Here we will organize all the names of the artist into one comma seperated string
        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            #Make sure that these lines are outside the if statement so that if there is indeed only on artist
            #it will be recorded and added to teh artist string
            name = artist.get('name')
            artist_string += name
        votes = Vote.objects.filter(room=room, song_id=song_id)
        #This is our custom data that returns the info we are interested in the format that we want
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': len(votes),
            'votes_required': room.votes_to_skip,
            'id': song_id
        }
        self.update_room_song(room, song_id)
        #Make sure to pass the response that you are getting into the response return statement so that you can view
        #it on the frontend
        return Response(song,status=status.HTTP_200_OK)

    #Here we are updating constantly the current song playing within the room
    def update_room_song(self,room, song_id):
        current_song = room.current_song
        #Here we will refresh the votes list so that whenever a new song is playing, we delete all teh votes from before
        if current_song != song_id:
            room.current_song = song_id
            room.save()
            votes = Vote.objects.filter(room=room).delete()


class PauseSong(APIView):
    def put(self,response,format=None):
        #We need this in order to see which room exactly is the pause request tailored to
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        #We first want to check and see if the host is the one asking to pause or if the host has enabled the guest can
        #pause attribute so that we can make sure that there is pausing authorization
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({"pause": "Song has now been paused"}, status=status.HTTP_200_OK)
        #This is important because iif the user is not the host and guest are not allowed to pause, then we will
        #Return a forbidden response
        return Response({"unauthorized": "Host has blocked users from pausing music"},status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self,response,format=None):
        #We need this in order to see which room exactly is the pause request tailored to
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        #We first want to check and see if the host is the one asking to pause or if the host has enabled the guest can
        #pause attribute so that we can make sure that there is pausing authorization
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({"play": "Song is now playing"}, status=status.HTTP_200_OK)
        #This is important because iif the user is not the host and guest are not allowed to pause, then we will
        #Return a forbidden response
        return Response({"unauthorized": "Host has blocked users from pausing music"},status=status.HTTP_403_FORBIDDEN)

class SkipSong(APIView):
    def post(self,request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        #Here we are grabbing the votes pertaining to the current song playing
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip

        #This will check and see if the number of votes along with the current users vote is meeting the required
        #amout of votes needed to skip, If it does then we will skip the song, this only apply to the guest
        #(the host can automatically skip the song if they are the one sending the request)
        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            #We will create a new vote if the
            vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

#This will be used to get the details of the users playlist
class GetQueue(APIView):
    def get(self, request, format=None):
        room_code = request.session.get('room_code')
        room = Room.objects.filter(code=room_code).first()
        if room:
            response = get_queue(room.host)
            print(response)
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response({"Invalid Room": "The room does not exist"}, status=status.HTTP_404_NOT_FOUND)

