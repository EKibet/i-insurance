from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets
from .models import User,UserProfile
from .serializers import UserSerializer,RequestPasswordResetSerializer,SetNEwPasswordSerializer,UserProfileSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            u_id64=urlsafe_base64_encode(str(user.id).encode('utf-8'))
            u_id64 = u_id64
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('policy:password_reset',kwargs={'u_id64':u_id64,'token':token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hello  Use link below to reset password \n'+absurl
            data = {'email_body':email_body,'to_email':user.email,'email_subject':'Password Reset'}
            Util.send_email(data)
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request,u_id64,token):
        try:
            id=smart_bytes(urlsafe_base64_encode(u_id64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):

                return Response({"Error":"Token is not valid, Please request a new one "},status=status.HTTP_401_UNAUTHORIZED)
            return Response({"success":True,"message":"Credentials is valid" ,"u_id64":u_id64,"token":token},status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator():
                return Response({"Error":"Token is not valid, Please request a new one "},status=status.HTTP_401_UNAUTHORIZED)


class SetNEwPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNEwPasswordSerializer

    def patch(self,requeest):
        serializer=self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'Success':True, 'messsage':'Password reset success'},status=status.HTTP_200_OK)