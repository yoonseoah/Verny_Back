from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, Count

# Create your views here.


class PostListView(views.APIView):
    # 게시글 목록 view 부분. 조회, 작성. 지금 보니까 api명세서에 POST 메소드 추가 필요한 것 같아요. 의견 주세요!

    def get(self, request):
        order_by = request.query_params.get('order_by')
        type_filter = request.query_params.get('type')

        queryset = Post.objects.all()

        if order_by == 'latest': #최신순으로
            queryset = queryset.order_by('-created_at')
        elif order_by == 'most_scrapped': #스크랩 많은 순으로
            queryset = queryset.annotate(scraps_count=Count('scraps')).order_by('-scraps_count')
        elif order_by == 'most_commented': #댓글 많은 순으로
            queryset = queryset.annotate(comments_count=Count('comments')).order_by('-comments_count')
        
        if type_filter:
            queryset = queryset.filter(type=type_filter)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#http://your-domain/main/posts/?order_by=most_scrapped
#http://127.0.0.1:8000/main/posts/?type=고전미술, 현대미술

    def post(self, request, format=None):  # 게시글 작성 POST 메소드입니다!
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)


class PostDetailView(views.APIView):  # 작품 해설(detail) 조회
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PosDetailSerializer(post)
        return Response(serializer.data)


class CommentView(views.APIView):  # 댓글 조회, 작성


    def get(self, request, pk, format=None):
        comment = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comment, many=True)
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


class RecommentView(views.APIView):
    def get(self, request, format=None):
        recomments = Recomment.objects.all()
        serializer = RecommentSerializer(recomments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RecommentDetailView(views.APIView):
    def put(self, request, recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        serializer = RecommentSerializer(recomment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        recomment.delete()
        return Response({"message": "대댓글 삭제 성공"})


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

class SearchView(views.APIView):
    def get(self, request):
        queryset = Post.objects.all()
        search_query = request.query_params.get('q')

        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) |  
                Q(title__icontains=search_query) |
                Q(painter__icontains=search_query)
            )
        serializer = PostSerializer(queryset,many=True)
        return Response(serializer.data)
    #http://your-domain/main/search/?q=search-keyword


class CommentLikeView(views.APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        liked_by_user = request.user in comment.likes.all()
        return Response({'liked': liked_by_user})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return Response({'liked':liked, 'comment': serializers.data})
    
class RecommentLikeView(views.APIView):
    def get(self, request, recomment_id):
        recomment = get_object_or_404(Recomment, pk=recomment_id)
        reliked_by_user = request.user in recomment.relikes.all()
        return Response({'reliked': reliked_by_user})

    def post(self, request, recomment_id):
        recomment = get_object_or_404(Recomment, pk=recomment_id)
        user = request.user

        if user in recomment.relikes.all():
            recomment.relikes.remove(user)
            reliked = False
        else:
            recomment.relikes.add(user)
            reliked = True

        return Response({'reliked':reliked, 'recomment': serializers.data})