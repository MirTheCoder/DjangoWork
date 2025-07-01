#sends off a signal when a user is created
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#When we create a user, it will send a signal so that it can create an instance of profile for the User
#Think of it as an automatic creation of a profile when a user account has been made
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)

#This will save the profile of the user to our profile database
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
