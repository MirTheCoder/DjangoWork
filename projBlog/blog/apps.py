from django.apps import AppConfig
#Remeber to import this in order to interact with the image being saved
from PIL import Image

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'


