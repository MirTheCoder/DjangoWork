from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Auction, Bids

def home(request):
    return render(request,'auction/home.html')

#Make sure to use "LoginRequiredMixin" when creating a class function with a django view
#if you want to check to see if a user is logged in, else it won't work properly in the url page

#This class view will create the new auction that the user is making and store it in the auction table
class PostAnAuction(LoginRequiredMixin,CreateView):
    model = Auction
    fields = ['title', 'description','startPrice','image']
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

    #We wull get the id number passed to find out which auction we want to see the bids of in order to let our html
    #page know so that it can display the bids of interest
    def get_context_data(self, **kwargs):
        #This will allow us to create and fill a context dictionary that can be used in our template with default values
        context = super().get_context_data(**kwargs)
        auction = get_object_or_404(Auction,id=self.kwargs.get('pk'))
        #Fetches parameter from our url and stores it within our context dictionary
        context['auction'] = auction
        return context

