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
# This will be our home function that handles request to the home page
def home(request):
    #We are going to store all the blog data into context and pass it into our rendering
    context = {
        #Used to fetch all the blog posts from the database
        'posts': Post.objects.all()
    }
    return render(request, "users/home.html", context)

#This will be our about page for users to access
def about(request):
    return render(request, "users/about.html", {'title': 'About'})

def register(request):
    return render(request, "users/register.html")