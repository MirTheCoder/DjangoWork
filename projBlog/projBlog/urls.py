"""
URL configuration for projBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

#The system will look to see what the user has put in the url and see which url pattern it matches with so that it
#can know where to send the information
urlpatterns = [
    path('admin/', admin.site.urls),
    #This will make sure that if we type "/blog" in our url it will send us to our blog app
    path('', include("blog.urls")),
    #This will make sure that when the site is rendered, we will go straight to the users app to handle stuff initially
    path('users/', include("users.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

#We will add this url to our url patterns only if the settings has the DEBUG running
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)