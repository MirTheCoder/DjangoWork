
from django.urls import path
from .views import index

#Allows django to know that this url page belongs to front end
app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    #We will let the system know that the 'join' path will be handled by the index html which will allow react to
    #handle the path and rendering pretty much
    path('join', index, name= 'frontend-home'),
    path('create', index, name= 'frontend-home'),
    path('room/<str:roomCode>', index, name= 'frontend-home'),
    path("info", index, name="info"),
]
