from django.contrib import admin
from .models import Post

# Here we wil register our models or tables so that they can be registered and used or displayed by admin page

#This will register our Post table in the admin page
admin.site.register(Post)