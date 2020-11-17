from django.urls import path
from . import views
from .views import RegisterAPI

app_name='policy'
urlpatterns=[
    path('register/', RegisterAPI.as_view(), name='register'),
]
