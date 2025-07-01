from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile

#We are creating a form that inherits
class UserRegisterForm(UserCreationForm):
    #We are adding an email field for the user to input their email when creating their account
    email = forms.EmailField(required=False)

    #Specifies the model or database this form interacts with
    class Meta:
        model = User
        #This shows the fields the user needs to fill out in order to create their account
        fields = ["username", "email", "password1", "password2"]

#This will be used to allow the user to update their username and password
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    # Specifies the model or database this form interacts with
    class Meta:
        model = User
        # These are the fields that we are allowing the user to update
        fields = ["username", "email"]

#We will use this model to update a users profile
class ProfileUpdateForm(forms.ModelForm):

    # Specifies the model or database this form interacts with
    class Meta:
        model = Profile
        # These are the fields that we are allowing the
        fields = ["image"]