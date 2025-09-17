from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import editProfile, forgotPassword, loginCode


urlpatterns = [
    path('', views.home, name = 'users-home'),
    path('register/', views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.viewProfile, name = 'user-profile'),
    #You must past an argument into the url for the editProfile in order for it to work since it is
    #inherting from the update view
    path('updateProfile/<int:pk>/', editProfile.as_view() , name = 'updateProfile'),
    path('forgotPassword/',forgotPassword , name = "forgotPassword"),
    path('loginCode/<str:name>', loginCode , name = "loginCode"),
]