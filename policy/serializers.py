from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,UserProfile,Policy
from rest_framework.exceptions import AuthenticationFailed
from .models import *



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name' ,'middle_name','last_name','email', 'password',)


    default_error_messages = {
        
    }


    def validate(self, attrs):
        email = attrs.get('email', '')
        first_name = attrs.get('first_name', '')
        middle_name = attrs.get('middle_name', '')
        last_name = attrs.get('last_name', '')
        if first_name=='' or last_name=='':
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "middle_name","last_name","id_no","email","bio","is_admin","is_agent","date_joined","phone_no","address","pk")
        extra_kwargs = {'password': {'write_only': True}}

    password=serializers.CharField(max_length=68, min_length=6, write_only=True) 
    def validate (self, attrs):
        email= attrs.get('email', '')
        username =attrs.get('username', '')

        return attrs

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields =( 'id', 'user', 'category', 'policy_number', 'policy_contact', 'form', 'slug', 'signed', 'updated')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("pk","id_img", "profile_picture","date_joined","gender","employment_status","bank_accountno")

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


class LogoutSerislizer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'Bad_Token':{'Token is expired or invalid'}
    }
    def validate(self,attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Bad_Token')

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

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields =( 'id', 'user', 'category', 'policy_number', 'policy_contact', 'form', 'signed', 'updated')


