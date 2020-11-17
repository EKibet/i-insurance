from django.urls import path
from . import views
from .views import PasswordTokenCheckAPI,RequestPasswordReset,SetNEwPasswordAPIView

app_name='policy'
urlpatterns=[
    path('request-reset-email/',RequestPasswordReset.as_view(),name='request-reset-email'),
    path('password-reset/<u_id64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password_reset'),
    path('pasword-reseet-complete/',SetNEwPasswordAPIView.as_view(),name='password reset complete')

]
