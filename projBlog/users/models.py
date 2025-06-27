
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    #This creates a one to one ratio that connects users to their profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #You need to first install "Pillow" before you can use the Image Field within your database
    #Side note: the good thing is that
    image = models.ImageField(default='default.jpg', upload_to='profile.pics')

    def __str__(self):
        return f"{self.user.username} Profile"

class Chat(models.Model):
    #This creates a one to one ratio that connects users to their profile

    #Here we use chats_sent to specify how each chat relates to the users included in the chat. One User will have
    #The chat related to them as a chat received while the other will have the chat relating to them as a chat sent
    user1 = models.ForeignKey(User, related_name='chats_sent', on_delete=models.SET_NULL, null=True)
    user2 = models.ForeignKey(User, related_name='chats_received', on_delete=models.SET_NULL, null=True)
    #You need to first install "Pillow" before you can use the Image Field within your database
    #Side note: the good thing is that
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    #This tells the create view pertaining to this table where to go after it has created the new chat instance within
    #our database
    def get_absolute_url(self):
        # This will be used in order to call the post-detail url and pass the post primary key to find the blog post we
        # want to display
        return reverse('users-chat', kwargs={'pk': self.user2.id})