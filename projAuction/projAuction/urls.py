from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from auction.views import LoggingPasswordResetView

urlpatterns = [
    #Url's starting with admin will be handled by admin
    path('admin/', admin.site.urls),
    #By default, when the program is run, the auction app will take the user to its default page
    path('', include('auction.urls')),
    #This url is for all user related things so that the users app can handle it
    path('users/', include('users.urls')),
    path('password-reset/', LoggingPasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    #When the user submits a request to reset their password, the function that handles the submission will call this url in order to
    #authenticate the user and make sure that the email they typed in is linked to their account/session
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
