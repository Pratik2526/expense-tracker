from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import RegisterUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken 

class RegisterUserView(APIView):

    def post(self,request):

        data = request.data 
        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400) 
        
class LoginUserView(APIView):

    def post(self,request):
        data = request.data 
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] 
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })