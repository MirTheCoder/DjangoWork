
from django.urls import path
from.views import *
urlpatterns = [
    path('get-auth-url', AuthURL.as_view(), name= 'auth'),
    path('redirect', spotify_callback, name= 'auth'),
    path('is-authenticated', IsAuthenticated.as_view(), name= 'isAuthenticated'),
    path('current-song', CurrentSong.as_view(), name='currentSong'),
]
