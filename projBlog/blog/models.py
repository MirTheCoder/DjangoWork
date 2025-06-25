from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
#Make sure to run "python projBlog/manage.py makemigrations " to create the table

#Run "python projBlog/manage.py sqlmigrate blog 0001" in the terminal line to ensure that the table is added to the
#database.


#In this case we used blog 0001 because we made the table in the blog models python file, but you would change
#that based on the app you are creating the table in

#Here are some steps for apply changes to your table to the database
#1. to ensure that the change is updated to your migrations folder, run "python manage.py makemigrations"
#2. to apply the change to the table in the database, run "python manage.py migrate"


#This creates a table within our database for the post for each user
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    #Automatically saves the post with the time it was posted as a default method if the user does not want to create
    #their own time
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #We will have this in order to allow the user to add a photo to their blog post
    #The "null=True" and "blank=True" allow us to have Null values in our database and allow the forms to store blank
    #values
    image = models.ImageField(upload_to='post.pics',null=True,blank=True)

#Controls how the data in Post table will display the data in admin
    def __str__(self):
        return self.title

    #This method will redirect us to the detail page of the POST we create once we create a new blog post
    def get_absolute_url(self):
        #This will be used in order to call the post-detail url and pass the post primary key to find the blog post we
        #want to display
        return reverse('post-detail', kwargs={'pk':self.pk})

#This will edit the size of the image put with the post, make sure to also
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

#This is where we will store the comments made on different post
class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    speaker = ForeignKey(User, on_delete=models.CASCADE)
    post = ForeignKey(Post, on_delete=models.CASCADE)

    # This method will redirect the user to the detail page of the post once the user adds a comment
    def get_absolute_url(self):
        #This will be used in order to call the post-detail url and pass the post primary key to find the blog post we
        #want to display
        return reverse('post-comment', kwargs={'pk':self.pk})