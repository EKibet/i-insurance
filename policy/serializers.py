from django.conf import settings
# from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import *
from .models import User, UserProfile

# User = settings.AUTH_USER_MODEL
User = user_model()
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name' ,'middle_name','last_name','email', 'password',)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "middle_name","last_name","id_no","email","bio","is_admin","is_agent","date_joined","phone_no","address","pk")
        extra_kwargs = {'password': {'write_only': True}}



class RequestPasswordResetSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)

    class Meta:
        model = User
        fields=['email']



class SetNEwPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6,max_length=68, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)
    u_id64=serializers.CharField(min_length=1, write_only=True)

    class meta:
        fields = ['password', 'token','u_id64']

    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            u_id64 = attrs.get('uidb64')

            id=force_str(urlsafe_base64_encode(u_id64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed("The restlink is invalid ",401)

            user.Set_password(password)
            user.save
        except Exception as e:
            raise AuthenticationFailed("The restlink is invalid ",401)
        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields =['token']


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password =serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=65, min_length=6, read_only=True)

    class Meta:
        model = User
        fields =['email', 'password', 'username','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_active:
        # if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if user is not None and user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        if not user:
            raise AuthenticationFailed('Account disabled, contact admin')

            return{
                'email' : user.email,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'tokens' : user.token
            }
            return attrs
            
