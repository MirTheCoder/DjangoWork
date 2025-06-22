from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView

#These url patterns help decided which function in our views file handle the request
urlpatterns = [
    #We leave the end of the url blank to navigate to our home page
    #We set the view to views.home which tells django to access the home function in our views pytho file if the home
    #page is requested
    #Because we can potentially have multiple home pages, we need to name the blog one "blog-home" to avoid confusion
    #Also, remember to do PostListView.as_view() to pass the class view PostListView as an actual view since it is not
    #a view on its own
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    #We are going to use this url to go see the details of a selected Blog
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]