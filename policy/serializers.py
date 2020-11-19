from rest_framework import serializers
from .models import User,UserProfile,Policy
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "middle_name","last_name","id_no","email","bio","is_admin","is_agent","date_joined","phone_no","address","pk")

class UserProfileSerializer(serializers.ModelSerializer):
    policy_name = serializers.RelatedField(source='policy', queryset=Policy.objects.all())
    class Meta:
        model = UserProfile
        fields = ("id_img", "profile_picture","date_joined","gender","employment_status","bank_accountno","policy_name","pk")

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


