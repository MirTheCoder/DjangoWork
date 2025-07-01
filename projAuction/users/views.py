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
from .models import Profile


def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        #Checks to see if the form being passed back to the function is valid
        if form.is_valid():
            #This is what we use in order to save the user to our database
            form.save()
            #If it is valid, then we will get the username and send a message alert to the user to let them know it was
            #successful
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            voice = f"Account created for{username}"
            return render(request, "users/register.html", {"form": form, "voice": voice})
        else:
            #If the form was not valid, then we will alert the user that it wasn't successful
            alert = "Information was invalid, unable to create an account"
            return render(request, "users/register.html", {"form": form, "alert": alert})
    else:
        #If this was not a POST request then we will just create a blank form for the user to fill out
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


#This @login_required is a decelerator that adds functionality or requirements for this function to run
@login_required()
class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'users/updateProfile'
    fields = ['age','phone','email','bio','twitter','instagram','facebook','image']






