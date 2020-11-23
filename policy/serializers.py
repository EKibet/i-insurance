from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from .models import *
from django.contrib.auth import get_user_model as user_model
from django.conf import settings


User = user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password=serializers.CharField(max_length=68, min_length=6, write_only=True) 

    def validate (self, attrs):
        email= attrs.get('email', '')
        username =attrs.get('username', '')

        return attrs

    def create(self, validate_data):
    
        return User.objects.create_user(**validate_data)

    class Meta:
        model = User
        fields = ['email', 'password','first_name', 'last_name']

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
            

class AgentProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = AgentProfile
        fields = [
            'pk',
            'email',
            'profile_picture',
            'job_number',
            'gender',
            
        ]


# queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     filter_fields = ('name', 'email', 'department')