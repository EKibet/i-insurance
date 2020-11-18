from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views
from django.urls import path
from rest_framework.authtoken import views

from . import views
from .views import LoginAPIView, RegisterAPI, VerifyEmail

# from rest_framework.authtoken.views import obtain_jwt_token
app_name = 'policy'

urlpatterns = [

    path('register/', RegisterAPI.as_view(), name="register"),
        path('login/', LoginAPIView.as_view(), name="login"),
        # url(r'^api-token-auth/', obtain_jwt_token),
        path('email-verify/', VerifyEmail.as_view(), name="email-verify"),


]
