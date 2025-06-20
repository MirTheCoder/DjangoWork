from django.urls import path
from . import views
#These help map different URL's or routes to functions within the view file
urlpatterns = [
    path('', views.home, name ='users-home'),
    path('about/', views.about, name='users-about'),
    path('home/', views.home, name='users-homepage')
]