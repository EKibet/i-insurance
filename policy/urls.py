from django.urls import path
from . import views
from .views import PasswordTokenCheckAPI,RequestPasswordReset,SetNEwPasswordAPIView,UserProfileAPIView,SingleUserProfileAPIView

app_name='policy'
urlpatterns=[
    path('request-reset-email/',RequestPasswordReset.as_view(),name='request-reset-email'),
    path('password-reset/<u_id64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password_reset'),
    path('pasword-reset-complete/',SetNEwPasswordAPIView.as_view(),name='password_reset_complete'),
    path('userprofile/',UserProfileAPIView.as_view(),name='user_profile'),
    path('single-profile/<int:pk>',SingleUserProfileAPIView.as_view(),name='single_profile')

]
