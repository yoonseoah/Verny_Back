from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from main.models import *
from main.serializers import *

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

class CommentListView(views.APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        id = request.GET.get('id')
        author = request.GET.get('author')
        content = request.GET.get('content')
        created_at = request.GET.get('created_at')
        likes_count = request.GET.get('likes_count')
        recomments_count = request.GET.get('recomments_count')

        params = {'id': id, 'author': author, 'content': content, 'created_at': created_at, 'likes_count': likes_count, 'recomments_count': recomments_count}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        comments = (Comment.objects.filter(author=user.id)&(Comment.objects.filter(**arguments))).distinct()

        serializer = self.serializer_class(comments, many=True)
        return Response({'message': "작성 댓글 목록 조회 성공", 'data': serializer.data}, status=HTTP_200_OK)

class RecommentListView(views.APIView):
    serializer_class = RecommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        id = request.GET.get('id')
        author = request.GET.get('author')
        content = request.GET.get('content')
        created_at = request.GET.get('created_at')
        relikes_count = request.GET.get('relikes_count')

        params = {'id': id, 'author': author, 'content': content, 'created_at': created_at, 'relikes_count': relikes_count}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        recomments = (Recomment.objects.filter(author=user.id)&(Recomment.objects.filter(**arguments))).distinct()

        serializer = self.serializer_class(recomments, many=True)
        return Response({'message': "작성 대댓글 목록 조회 성공", 'data': serializer.data}, status=HTTP_200_OK)

