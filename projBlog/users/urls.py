from django.urls import path
from . import views
from .views import UsersList

#These url patterns help decided which function in our views file handle the request
urlpatterns = [
    #We leave the end of the url blank to navigate to our home page
    #We set the view to views.home which tells django to access the home function in our views pytho file if the home
    #page is requested
    #Because we can potentially have multiple home pages, we need to name the blog one "blog-home" to avoid confusion
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='profile'),
    path('seeUsers/', UsersList.as_view(), name='users-list'),

    #Be sure to identify the type of variable that you will be passing into the url (ex. <username> will be a string)
    path('', views.home, name='users-home'),
]