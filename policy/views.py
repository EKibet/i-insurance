from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import LoginSerializer, EmailVerificationSerializer,RegisterSerializer
from .serializers import AgentProfileSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from rest_framework.decorators import api_view, parser_classes
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FormParser
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth import get_user_model as user_model
import json
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
# User = settings.AUTH_USER_MODEL
# User = user_model()
# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_data = serializer.data

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(email=email, username=username, password=password)
    
        if user:
            auth_token = jwt.encode({"email": email}, 'rrffgguyuioommbf456788')

            serializer = LoginSerializer(user)

            user_data = User.objects.get(email=email)

            data = {
                'user': serializer.data, 'first_name': user_data.first_name, 'last_name':user_data.last_name, 'token': auth_token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
    
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING, required=True)
    

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email':'Successfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:

            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class AgentProfileList(ListAPIView):

    serializer_class = AgentProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return AgentProfile.objects.all()


class AgentProfileDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return AgentProfile.objects.filter(user=self.request.user)



