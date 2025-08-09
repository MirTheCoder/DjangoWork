from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Auction, Bids, Reviews, BidLog
import logging
from django.contrib.auth.views import PasswordResetView
from .emails import *

logger = logging.getLogger(__name__)

class LoggingPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        print(f"The email used for password reset is: {email}")
        try:
            response = super().form_valid(form)
            print("response: ", response)
            return response
        except Exception as e:
            print("Error: ", e)


def home(request):
    return render(request,'auction/home.html')

#Make sure to use "LoginRequiredMixin" when creating a class function with a django view
#if you want to check to see if a user is logged in, else it won't work properly in the url page

#This class view will create the new auction that the user is making and store it in the auction table
class PostAnAuction(LoginRequiredMixin,CreateView):
    model = Auction
    fields = ['title', 'description','startPrice','image','stock']
    template_name = 'auction/createAuction.html'

    #Here we override the form valid to make the auctioneer requirement for an auction to be automatically equal to
    #the user creating the auction
    def form_valid(self, form):
        form.instance.auctioneer = self.request.user
        # This runs the form_valid method but now will ensure that the author is listed as the current user
        return super().form_valid(form)

#This will get all the auctions from our auctions table in order for us to display it
class ViewAuctions(ListView):
    model = Auction
    template_name = "auction/home.html"
    context_object_name = "auctions"

class ViewAuctionDetails(DetailView):
    model = Auction
    template_name = "auction/auctionDetails.html"
    context_object_name = "auction"

    def get_context_data(self, **kwargs):
        #This will allow us to create and fill a context dictionary that can be used in our template with default values
        context = super().get_context_data(**kwargs)
        auction = get_object_or_404(Auction,id=self.kwargs.get('pk'))
        bid_list = Bids.objects.filter(auction=auction)
        bid_amount = 0
        winningBids = []
        review_list = Reviews.objects.filter(auction=auction)
        context['reviews'] = review_list
        if bid_list:
            for bid in bid_list:
                if bid.amount > bid_amount:
                    bid_amount = bid.amount
                    winningBids = []
                    winningBids.append(bid)
                elif bid.amount == bid_amount:
                    winningBids.append(bid)
            context["winning"] = winningBids
        return context


def createBid(request):
    if request.method == "POST":
        #Mkae sure to use request.POST.get to obtain specific data in the form that has been submitted, do not use
        #request.form as it only works for flask
        name = request.POST.get('auctionName')
        auctionPiece = Auction.objects.filter(title=name).first()
        bid = request.POST.get('bidNum')
        Bids.objects.create(auction=auctionPiece, bidder=request.user, amount=bid)
    messages.success(request, "Your bid has been successfully added")
    return redirect(reverse('auction-home'))

#This view will be used to display the bids made
class viewBids(LoginRequiredMixin,ListView):
    model = Bids
    context_object_name = 'bids'
    template_name = 'auction/viewBids.html'

    #We will get the id number passed to find out which auction we want to see the bids of in order to let our html
    #page know so that it can display the bids of interest
    def get_context_data(self, **kwargs):
        #This will allow us to create and fill a context dictionary that can be used in our template with default values
        context = super().get_context_data(**kwargs)
        auction = get_object_or_404(Auction,id=self.kwargs.get('pk'))
        #Fetches parameter from our url and stores it within our context dictionary
        context['auction'] = auction
        context['related'] = Bids.objects.filter(auction=auction)
        return context

#Here we are passing bid id as an argument in order to get the correct bid or the bid that the user selects
#in order to see whom they are passing the auction to
@login_required()
def passAuction(request, bid_id):
    bid = Bids.objects.filter(id=bid_id).first()
    auction = bid.auction
    if bid:
        try:
            user = bid.bidder
            #Safe way to check and see if a valid image is being used for the auction
            if auction.image and auction.image.name:
                newLog = BidLog.objects.create(image=auction.image.url, user=user, auction=auction, title=auction.title,winPrice=bid.amount)
                newLog.save()
            else:
                newLog = BidLog.objects.create(user=user, auction=auction, title=auction.title,winPrice=bid.amount)
                newLog.save()
            #Once we save the bid, we will just redirect the user back to the view bids page
            val = changeStock(bid_id)
            notify_of_win(auction, bid)
            return redirect('auction-home')
        except Exception as e:
            print('Error:', e)
    print("the passing of the auction was unsuccessful")
    return redirect('auction-home')

#In this function we will check to see how much of the item is in stock, and if there are no more in stock, we will
#remove the auction
def changeStock(id):
    bid = Bids.objects.filter(id=id).first()
    auction = bid.auction
    if auction.stock > 1:
        stock = auction.stock
        stock -= 1
        auction.stock = stock
        auction.save(update_fields=['stock'])
    elif auction.stock == 1:
        auction.delete()

    return True

#Here we are getting all off the bids or auctions that the user won and compiling it into a list for them to view
@login_required()
def seeBidLog(request):
    user = request.user
    logs = BidLog.objects.filter(user=user)
    return render(request, "auction/BidLog.html", {'logs': logs})

#Here we will be creating the review that is posted by a user on a post, however, they must have had won the object in a
#previous auction
class addReview(LoginRequiredMixin,CreateView):
    model = Reviews
    template_name = "auction/addReview.html"
    fields = ['code','reviewReason','reviewRating']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = self.request.user
        auction = get_object_or_404(Auction, id=self.kwargs.get('pk'))
        context['person'] = person
        context['auction'] = auction
        return context


    #We will get the auction by looking for which auction matches the id value passed in the url
    # and auto setting the user to the user who submitted the form
    def form_valid(self, form, **kwargs):
        user = self.request.user
        auction = get_object_or_404(Auction, id=self.kwargs.get('pk'))
        form.instance.user = user
        form.instance.auction = auction
        # This runs the form_valid method but now will ensure that the author is listed as the current user
        return super().form_valid(form)

