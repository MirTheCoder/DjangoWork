
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostAnAuction



urlpatterns = [
    path('', views.home, name = 'auction-home'),
    path('postAnAuction/', PostAnAuction.as_view(), name = 'postAuction'),
]
