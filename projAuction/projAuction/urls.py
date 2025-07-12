from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    #Url's starting with admin will be handled by admin
    path('admin/', admin.site.urls),
    #By default, when the program is run, the auction app will take the user to its default page
    path('', include('auction.urls')),
    #This url is for all user related things so that the users app can handle it
    path('users/', include('users.urls')),
]
