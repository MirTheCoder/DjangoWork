
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name= 'frontend-home'),
    #We will let the system know that the 'join' path will be handled by the index html which will allow react to
    #handle the path and rendering pretty much
    path('join', index, name= 'frontend-home'),
    path('create', index, name= 'frontend-home'),

]
