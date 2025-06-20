from django.apps import AppConfig

#Helps to initiate something like a settings manager for your app that you create
class BlogConfig(AppConfig):
    #Helps automatically create ID numbers or primary keys for the data within each table in your database
    default_auto_field = 'django.db.models.BigAutoField'
    #Tells Django which app this configuration belongs to
    name = 'blog'
