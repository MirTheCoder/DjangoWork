from django.urls import path
from . import views
from .views import (PostListView, PostDetailView,
                    PostCreateView, PostUpdateView,
                    PostDeleteView, UsersPostListView)

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
    #We also pass the primary key as a variable into the url to ensure that we can get the right blog post via id number
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/seeUserPost/<str:person>/', UsersPostListView.as_view(), name='post-of-user'),
]