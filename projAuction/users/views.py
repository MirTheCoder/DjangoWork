from dataclasses import fields

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import request
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Code


def home(request):
    return render(request, 'users/home.html')

#This is used to help register users and create an account for them in our database
def register(request):
    create = False
    #If a POST request is made, the computer will take the info input by the user in order to geenrate and account for
    #them with the given information
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        #Checks to see if the form being passed back to the function is valid
        if form.is_valid():
            #This is what we use in order to save the user to our database
            form.save()
            #If it is valid, then we will get the username and send a message alert to the user to let them know it was
            #successful
            username = form.cleaned_data.get('username')
            persona = User.objects.filter(username=username).first()
            messages.success(request, f"Account created for {username}")
            voice = f"Account created for{username}"
            if persona:
                #Here we will create a profile and a bidding code for each user who registers and makes an account
                Profile.objects.create(person=persona)
                Code.objects.create(user=persona)
            return render(request, "users/register.html", {"form": form, "voice": voice})
        else:
            #If the form was not valid, then we will alert the user that it wasn't successful
            alert = "Information was invalid, unable to create an account"
            return render(request, "users/register.html", {"form": form, "alert": alert})
    else:
        #If this was not a POST request then we will just create a blank form for the user to fill out
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


#This allows the user to update their profile
class editProfile(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = 'users/updateProfile.html'
    fields = ['age','phone','email','bio','twitter','instagram','facebook','image']

@login_required()
#This will allow the user to access their profile
def viewProfile(request):
    #This will cross-reference the Profile table with the user making the request to see if there is a match and then
    #return the matching profile to us
    character = get_object_or_404(Profile, person=request.user)
    # Fetches parameter from our url and stores it within our context dictionary
    return render(request, "users/profile.html", {"profile": character})








