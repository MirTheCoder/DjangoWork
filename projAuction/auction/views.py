from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Auction

def home(request):
    return render(request,'auction/home.html')

#Make sure to use "LoginRequiredMixin" when creating a class function with a django view
#if you want to check to see if a user is logged in, else it won't work properly in the url page
class PostAnAuction(LoginRequiredMixin,CreateView):
    model = Auction
    fields = ['title', 'description','startPrice','image']
    template_name = 'auction/createAuction.html'

    def form_valid(self, form):
        form.instance.auctioneer = self.request.user
        # This runs the form_valid method but now will ensure that the author is listed as the current user
        return super().form_valid(form)

class ViewAuctions(ListView):
    model = Auction
    template_name = "auction/home.html"
    context_object_name = "auctions"
