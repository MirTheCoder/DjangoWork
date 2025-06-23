from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

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
def profile(request):
    #If the user submits new info, then we will retrieve the new info submitted by the user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        #We add request.FILES in order to retrieve the image file that the user submits
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        #We check to see if the users submission is valid before we save the new info they input into the database for
        #their profile
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
        else:
            messages.error(request, "The form you submitted was deemed not valid, please try again")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)


#This will be the home page of our code
def home(request):
    return render(request, "users/home.html", {"title": "Users Home Page"})


