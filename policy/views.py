from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from knox.models import AuthToken
from policy.models import User
from .models import Policy
from .serializers import PolicySerializer
from rest_framework import status


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # import pdb; pdb.set_trace()
        user = User.objects.create_user(
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        # import pdb; pdb.set_trace()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
      
        })



class policyList(APIView):
    def get(self,request, formart = None):
       all_policy = Policy.objects.all()
       serializers = PolicySerializer(all_policy, many = True)
       return Response(serializers.data)


    def post(self, request, formart=None):
        serializers = PolicySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)