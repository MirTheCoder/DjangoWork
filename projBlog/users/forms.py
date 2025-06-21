from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#We are creating a form that inherits
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    #Specifies the model or database this form interacts with
    class Meta:
        model = User
        #This shows the fields the user needs to fill out in order to create their account
        fields = ["username", "email", "password1", "password2"]