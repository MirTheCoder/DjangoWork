
from django.urls import path
from.views import *
urlpatterns = [
    path('get-auth-url', AuthURL.as_view(), name= 'auth'),
    path('redirect', spotify_callback, name= 'auth'),
    path('is-authenticated', IsAuthenticated.as_view(), name= 'isAuthenticated'),
    path('current-song', CurrentSong.as_view(), name='currentSong'),
    path('pause', PauseSong.as_view(), name="pause"),
    path('play', PlaySong.as_view(), name="play"),
    path('skip', SkipSong.as_view(),name="skip"),
    path('queue',GetQueue.as_view(), name='UserPlaylist')
]
