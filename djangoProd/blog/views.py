from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

posts = [
    {
        'author': 'CoreyMS',
        'title' : 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title' : 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]
# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, "users/home.html", context)

def about(request):
    return render(request, "users/about.html", {'title': 'About'})

