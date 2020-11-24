from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views
from django.urls import path
from rest_framework.authtoken import views
from . import views

from .views import (PasswordTokenCheckAPI,RequestPasswordReset,
                    SetNEwPasswordAPIView,UserProfileAPIView,
                    SingleUserProfileAPIView,LogoutAPIView,
                    LoginAPIView, RegisterAPI, VerifyEmail)

    
app_name='policy'
urlpatterns=[
    path('request-reset-email/',RequestPasswordReset.as_view(),name='request-reset-email'),
    path('password-reset/<u_id64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password_reset'),
    path('pasword-reset-complete/',SetNEwPasswordAPIView.as_view(),name='password_reset_complete'),
    path('userprofile/',UserProfileAPIView.as_view(),name='user_profile'),
    path('single-profile/<int:pk>',SingleUserProfileAPIView.as_view(),name='single_profile'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email_verify'),
    path('logout/',LogoutAPIView.as_view(),name='logout')

]
