from django.urls import path
from .views import RegisterView,LoginAPIView,VerifyEmail,ListAPIView, RetrieveUpdateDestroyAPIView, AgentProfileList, AgentProfileDetailApi
from django.conf import settings
from django.contrib.auth import views
from . import views
from rest_framework.authtoken import views
from django.conf.urls import url
# from rest_framework.authtoken.views import obtain_jwt_token



urlpatterns = [

        path('register/', RegisterView.as_view(), name="register"),
        path('login/', LoginAPIView.as_view(), name="login"),
        # url(r'^api-token-auth/', obtain_jwt_token),
        path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
        path('agentprofile', AgentProfileList.as_view()),
        path("agentprofile/<int:id>", AgentProfileDetailApi.as_view()),

]