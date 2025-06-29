from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request

def home(request):
    return render(request,'auction/home.html')



