from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name ='users-home'),
    path('about/',views.about, name='users-about'),
    path('home/' , views.home, name='users-home')
]