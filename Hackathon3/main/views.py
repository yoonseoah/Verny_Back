from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework import views
from rest_framework.response import Response

# Create your views here.


class PostListView(views.APIView):
    # 게시글 목록 view 부분. 조회, 작성. 지금 보니까 api명세서에 POST 메소드 추가 필요한 것 같아요. 의견 주세요!

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # 게시글 작성 POST 메소드입니다!
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)


class PostDetailView(views.APIView):  # 작품 해설(detail) 조회
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentView(views.APIView):  # 댓글 조회, 작성
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentDetailView(views.APIView):  # 댓글 수정,삭제
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


class PostScrapView(views.APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        scraped_by_user = request.user in post.scraps.all()
        return Response({'scraped': scraped_by_user})

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        if user in post.scraps.all():
            post.scraps.remove(user)
            scraped = False
        else:
            post.scraps.add(user)
            scraped = True

        return Response({'scraped':scraped, 'post': serializers.data})



