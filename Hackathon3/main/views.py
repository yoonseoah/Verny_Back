from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework import views
from rest_framework.response import Response

# Create your views here.


class PostListView(views.APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serilaizer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serilaizer.error)


class PostDetailView(views.APIView):
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentView(views.APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentDetailView(views.APIView):
    def get(self, request, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = CommentSerializer(Comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response({"message": "댓글 삭제 성공"})
