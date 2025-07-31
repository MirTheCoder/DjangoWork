from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/me/"

#Used to check and see if the user has any tokens attached to their session id
def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id).first()
    if user_tokens:
        return user_tokens
    else:
        return None

#Used to either update the users token or create a new token
def update_or_create_user_tokens(session_id, access_token, token_type,expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    #If we don't get a time limit for each authentication then we will set it to one hour by default
    if not expires_in:
        expires_in = 3600
    # will start the timer from the current time when created
    expires_in = timezone.now() + timedelta(seconds=expires_in) #Token will expire every hour
    if tokens:
        #If the user does have a token attached to their session, then we will just update the fields in their token
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token','expires_in','token_type'])
    else:
        #If the user does not have a token then we will just create one for them
        tokens = SpotifyToken(user=session_id,access_token=access_token,refresh_token=refresh_token,token_type=token_type,expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        #Here we are checking to see if the authentication period has expired or if their token has expired
        #so that we can then refresh it if it has expired
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True


    return False

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    #Here we are using a post request to get a new access token
    response = post('https://accounts.spotify.com/api/token', headers={

    },data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    #Here we are going to set the new access token for the user
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')


    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    #Used to send the authorization token to spotify
    headers = {'Content-Type': "application/json", 'Authorization':"Bearer " + tokens.access_token}

    #Make sure to use a chain of if and elif statements to ensure that you are only sending the request of interest
    if post_:
        #Make sure to add a body to your request, even the json body is empty or else it won't work
        response = post(BASE_URL + endpoint, headers=headers, json={})
        print(response.text)
    elif put_:
        #Make sure to add a body to your request, even the json body is empty or else it won't work
        response = put(BASE_URL + endpoint, headers=headers)
        print(response.text)
    else:
        response = get(BASE_URL + endpoint, {}, headers=headers)
    #This is in case we encounter an error when we try to get the json data of our get request
    try:
        return response.json()
    except:
        return {"Error": "issue with request"}

#These two functions will both send put request to our execute_spotify_api_request function so that depending on if the
#user want to pause or play the
def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)

def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)

def skip_song(session_id):
    return execute_spotify_api_request(session_id, "player/next", post_=True)
def get_queue(session_id):
    endpoint = "player/queue"
    return execute_spotify_api_request(session_id,endpoint)