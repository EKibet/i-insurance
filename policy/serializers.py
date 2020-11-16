from rest_framework import serializers
from policy.models import User
from .models import UserProfile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name','email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name' ,'middle_name','last_name','email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(validated_data['email'],validated_data['first_name'],validated_data['middle_name'],validated_data['last_name'], validated_data['password'])

        return user