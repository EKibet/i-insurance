from django.urls import path
from .views import RegisterAPI
from . import views
from django.conf.urls import url



urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/policy', views.policyList.as_view()),
    url(r'api/policy/policy-id/(?P<pk>[0-9]+)/$',views.PolicyDescription.as_view())

]




