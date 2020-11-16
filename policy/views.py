from django.shortcuts import render
from rest_framework import generics,status
from .serializers import RegisterSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from knox.models import AuthToken
from policy.models import User







# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             form = SignUpForm()
#         return render(request, {'form': form})

# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer

#     def post(self,request):
#         user = request.data

#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()


#         user_data = serializer.data


#         return Response(user_data, status = status.HTTP_201_CREATED)




class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # import pdb; pdb.set_trace()
        user = User.objects.create(
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        # import pdb; pdb.set_trace()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })