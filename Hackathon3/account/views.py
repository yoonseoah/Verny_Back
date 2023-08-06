from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.

class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class ProfileView(views.APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # def get(self, request, format=None):
    #     serializer = ProfileSerializer(request.user)
    #     return Response({'message': '프로필 가져오기 성공', 'data': serializer.data}, status=HTTP_200_OK)

    # def put(self, request, format=None):
    #     serializer = ProfileSerializer(data=request.user)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': '프로필 가져오기 성공', 'data': serializer.data}, status=HTTP_200_OK)
    #     return Response(serializer.errors)

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)  # Assuming the profile is related to the user
        return Response({'message': '프로필 가져오기 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def put(self, request, format=None):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)  # Using request data to update the profile
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '프로필 업데이트 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '프로필 업데이트 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)