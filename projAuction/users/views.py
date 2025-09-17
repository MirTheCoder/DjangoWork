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
from .models import LoginReset
from .emails import login_code


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
            #This is used to get the email from the form the user submits for registration
            email = form.cleaned_data.get('email')
            number = form.cleaned_data.get('number')
            persona = User.objects.filter(username=username).first()
            messages.success(request, f"Account created for {username}")
            voice = f"Account created for{username}"
            if persona:
                #Here we will create a profile and a bidding code for each user who registers and makes an account
                Profile.objects.create(person=persona, email=email, phone=number)
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
#If the user doesn't have a profile (will most likely just be applicable to the creation of a superuser instead of the
#traditional registration way), then we will automatically generate one for them
def viewProfile(request):
    #This will cross-reference the Profile table with the user making the request to see if there is a match and then
    #return the matching profile to us
    character = Profile.objects.filter(person=request.user).first()

    if not character:
        profile = Profile.objects.create(person=request.user)
        profile.save()
        character = get_object_or_404(Profile, person=request.user)
    # Fetches parameter from our url and stores it within our context dictionary
    return render(request, "users/profile.html", {"profile": character})

#This will take the user to the forgot password page so that we can send a code to their email
#that they will have to type in, in order to log back into their account
def forgotPassword(request):
        if request.method == "POST":
            #For a post request, you ought to do a request.POST.get if you are using django
            uname = request.POST.get("username")
            uname = uname.strip()
            val = User.objects.filter(username = uname).first()
            #Here, if the username that was input is true,
            if val:
                #This will make sure that we don't create multiple recovery codes for the same user
                list = LoginReset.objects.filter(user=val)
                if list:
                    value = LoginReset.objects.filter(user=val).first()
                else:
                    value = LoginReset.objects.create(user = val)
                email = val.profile.email
                code = value.code
                #We use this to send the email with the code to the user that they can use
                #to reset their password
                login_code(uname,code,email)
                #Be sure to use direct url names for a redirect to another url in django
                #We also will be passing the username the user had given us into the redirect
                return redirect("loginCode", name=uname)

        return render(request, "users/forgotPassword.html")

def loginCode(request, name):
    if request.method == "POST":
        person = User.objects.filter(username=name).first()
        being = LoginReset.objects.filter(user=person).first()
        #Here we will check and see if the user has entered a new password
        if request.POST.get("newpswd"):
            #Here we will send the user to the login page
            return None
        #Checks to see if the code input does indeed match the code we gave the user
        if request.POST.get("code") == being.code:  
            codeValid = True
            #If the code is valid, then we will return the same html template but with a special context
            #attached to it
            return render(request, "users/codeLogin.html", {"codeValid": codeValid})
    return render(request, "users/codeLogin.html")








