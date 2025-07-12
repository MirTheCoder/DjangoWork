
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostAnAuction, ViewAuctions, ViewAuctionDetails



urlpatterns = [
    #Default url for all urls handled by the auction app, this will take us to the page displaying all auctions
    path('', ViewAuctions.as_view(), name = 'auction-home'),
    #Url to the page where the user can post their auction
    path('postAnAuction/', PostAnAuction.as_view(), name = 'postAuction'),
    path('auctionDetails/<int:pk>/',ViewAuctionDetails.as_view(), name = 'auctionDetails'),
    path('newBid/',views.createBid, name = 'createBid'),

]
