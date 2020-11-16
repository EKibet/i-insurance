from django.conf.urls import url,include
from . import views
from .views import PasswordTokenCheckAPI,RequestPasswordReset,SetNEwPasswordAPIView


urlpatterns=[
    url('request-reset-email/',RequestPasswordReset.as_view(),name='request-reset-email'),
    url('password-reset/<u_id64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password_reset'),
    url('pasword-reseet-complete/',SetNEwPasswordAPIView.as_view(),name='password reset complete')

]
