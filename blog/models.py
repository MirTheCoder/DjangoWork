from django.db import models
from django.utils import timezone
#We are going to inherit the author for our post model data table from the User data table made by django
from django.contrib.auth.models import User

# Create your models here.
# Side note: Remember to do python djangoProd/manage.py make migrations to update any changes made to the database
#Each Class is its own table in the database
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    #This will delete the post made for this model/table if the user is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)
#Don't forget to do djangoProd/manage.py migrate in order to execute those changes to the database

    #This tells the admin page of django to display the title of the blog post
    def __str__(self):
        return self.title

