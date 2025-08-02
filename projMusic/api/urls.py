from django.urls import path
from .views import *


urlpatterns = [
    path('', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view(), name='api-create_room'),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view()),
    path('users-in-room', GetUsersInRoom.as_view())
]