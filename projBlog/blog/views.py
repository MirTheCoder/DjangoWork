from django.shortcuts import render
from django.http import HttpResponse
#The dot means that you are importing from the same directory as the python file you are in
from . models import Post
#This will check and see if the user is logged in before we allow them to create a blog post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.
#This will be used when the user ask for the home page in the blog app
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, "blog/home.html", context)


#This will be used when the user ask for the about page in the blog app
def about(request):
    return render(request,  "blog/about.html", {'title': 'About'})

#This class List view is a view that is meant to display a list of objects from a database
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"    #class View will by default look for an html file with this path "<app>/<model>_list.html"
    #This sets the name of the list that we will be passing into our template context
    context_object_name = 'posts'
    #This helps to change the order in which the values within our Post database are displayed
    ordering = ['-date_posted']
    #This limits the amount of Post displayed on each page to 2
    paginate_by = 2
    #If you add a question mark to your url, it allows you to pass a parameter to your url file
    #ex: ?page = 2 will send you to the second page of blogs

class PostDetailView(DetailView):
    model = Post

#This will allow users to create Post from their end
#The CreateView automatically creates a post when form is submitted and tries to save it to our POST database
#We will also pass the "LoginRequiredMixin" into out PostCreateView class in order to ensure that the user is logged in
#before we allow them to create a new blog post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  #The create view looks for the template in the path "blog/post_form.html"
    fields = ["title", "content"]

    #We are going to override the form_valid method (method that checks if the users form submission is valid)
    #In order to automatically input the user as the author whenever the blog post is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        #This runs the form_valid method but now will ensure that the author is listed as the current user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  #The update view looks for the template in the path "blog/post_form.html"
    #Both "PostCreateView" and "PostUpdateView" share the same template which is "blog/post_form.html"
    fields = ["title", "content"]

    #We are going to override the form_valid method (method that checks if the users form submission is valid)
    #In order to automatically input the user as the author whenever the blog post is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        #This runs the form_valid method but now will ensure that the author is listed as the current user
        return super().form_valid(form)

    #This function will run a test to see if the blog that the user wants to edit was actually posted by the user
    # or checking to see if the user owns it
    def test_func(self):
        post = self.get_object()
        #We check and see if the user matches the author of the post which will let us know whether we can let
        #The user edit the post
        if self.request.user == post.author:
            return True
        else:
            return False
#The imports that we use to test if the user is logged in or if the user is the owner of the post
#("LoginRequiredMixin" and "UserPassesTestMixin") we must make sure that we put it to the left of the
#view we inherit when we add it to our parameters of our class view
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    #This will direct our user to the home page for blogs once the have confirmed deletion
    success_url = '/'

    # This function will run a test to see if the blog that the user wants to edit was actually posted by the user
    # or checking to see if the user owns it
    def test_func(self):
        post = self.get_object()
        # We check and see if the user matches the author of the post which will let us know whether we can let
        # The user edit the post
        if self.request.user == post.author:
            return True
        else:
            return False