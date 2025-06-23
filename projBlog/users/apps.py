from django.apps import AppConfig
from PIL import Image

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals


    #We will use this to override the save method for our images
    def save(self):
        #Use super when you want to override an already saved image
        super().save()
        img = Image.open(self.image.path)

        #Checks the dimensions of the image that the user is submitting
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            #Transforms the size of the image to the dimensions we had input
            img.thumbnail(output_size)
            img.save(self.image.path)