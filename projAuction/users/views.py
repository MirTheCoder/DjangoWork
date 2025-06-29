from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request

def home(request):
    return render(request, 'users/home.html')
