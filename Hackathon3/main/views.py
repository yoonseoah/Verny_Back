from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from django.db.models import Q, Count


# Create your views here.


class PostListView(views.APIView):
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

        filtered_post_count = queryset.count()

        # Serialize queryset and include filtered_post_count
        serializer = PostSerializer(queryset, many=True)
        response_data = {
            'post_count': filtered_post_count,
            'posts': serializer.data
        }
        
        return Response(response_data)



#http://your-domain/main/posts/?order_by=most_scrapped
#http://127.0.0.1:8000/main/posts/?type=고전미술, 현대미술

class PostAddView(views.APIView):
    def post(self, request, format=None):  # 게시글 작성 POST 메소드입니다!
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '포스트 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '포스트 작성 실패', 'errors': serializer.errors})


class PostDetailView(views.APIView):  # 작품 해설(detail) 조회
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

class PostScrapView(views.APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        scraped_by_user = request.user in post.scraps.all()
        return Response({'scraped': scraped_by_user})

    def post(self, request, pk):
        post = get_object_or_404(Post,id=pk)
        user = request.user

        if user in post.scraps.all():
            post.scraps.remove(user)
            scraped = False
        else:
            post.scraps.add(user)
            scraped = True

        return Response({"message": "스크랩 변경 성공",'scraped':scraped})

class CommentView(views.APIView):  # 댓글 조회, 작성
    def get(self, request, pk):
        order_by = request.query_params.get('order_by')

        queryset = Comment.objects.filter(post_id=pk)

        if order_by == 'latest': #최신순으로
            queryset = queryset.order_by('-created_at')
        elif order_by == 'most_liked': #좋아요 많은 순으로
            queryset = queryset.annotate(likes_count=Count('likes')).order_by('-likes_count')
        
        serializer = CommentSerializer(queryset, many=True)  # 적절한 시리얼라이저 사용
        return Response(serializer.data)
#http://127.0.0.1:8000/main/posts/1/comments/?order_by=lastest

    def post(self, request, pk, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id=pk)
            return Response({'message': '댓글작성 성공', 'data': serializer.data})
        return Response(serializer.errors) 
    


class CommentDetailView(views.APIView):  # 댓글 수정,삭제, 대댓글 작성
    def get(self, request, pk, comment_pk, format=None):
        comment = get_object_or_404(Comment,post_id=pk, pk=comment_pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk, post_id=pk)
        comment.delete()
        return Response({"message": "댓글 삭제 성공"})

    def put(self, request, pk, comment_pk, format=None):
        comment = get_object_or_404(Comment, pk=comment_pk, post_id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '댓글수정 성공', 'data': serializer.data})
        return Response({'message': '댓글수정 실패', 'data': serializer.errors})

    def post(self, request, pk, comment_pk, format=None):
        comment = get_object_or_404(Comment, post_id=pk, pk=comment_pk)
        serializer = RecommentSerializer(data=request.data)
        if serializer.is_valid():
            recomment = serializer.save(comment=comment)
            recomment_serializer = RecommentSerializer(recomment)
            return Response({'message': '대댓글 작성 성공', 'data': recomment_serializer.data}, status=HTTP_201_CREATED)
        return Response(serializer.errors)
    
class CommentLikeView(views.APIView): #댓글 좋아요
    def get(self, request,pk, comment_pk):
        comment = get_object_or_404(Comment, post_id=pk, pk=comment_pk)
        liked_by_user = request.user in comment.likes.all()
        return Response({'liked': liked_by_user})

    def post(self, request,pk, comment_pk):
        comment = get_object_or_404(Comment, post_id=pk, pk=comment_pk)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return Response({"message": "좋아요 변경 성공",'liked':liked})



class RecommentDetailView(views.APIView): #대댓글 조회, 수정, 삭제
    def get(self, request,pk,recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        serializer = RecommentSerializer(recomment)
        return Response(serializer.data)
    
    def put(self, request,pk, recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        serializer = RecommentSerializer(recomment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request,pk,recomment_pk, format=None):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        recomment.delete()
        return Response({"message": "대댓글 삭제 성공"})
    
    

class RecommentLikeView(views.APIView): #대댓글 좋아요
    def get(self, request,pk, recomment_pk):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        reliked_by_user = request.user in recomment.relikes.all()
        return Response({'reliked': reliked_by_user})

    def post(self, request,pk, recomment_pk):
        recomment = get_object_or_404(Recomment, pk=recomment_pk)
        user = request.user

        if user in recomment.relikes.all():
            recomment.relikes.remove(user)
            reliked = False
        else:
            recomment.relikes.add(user)
            reliked = True

        return Response({"message": "대댓글 좋아요 변경 성공",'reliked':reliked})



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
            search_result_count = queryset.count()
            
            if search_result_count > 0:
                serializer = PostSerializer(queryset, many=True)
                return Response({
                    'message': '검색 조회 성공',
                    'data': serializer.data,
                    'result_count': search_result_count  # Include the result count in the response
                })
            else:
                return Response({'message': '검색결과가 없어요. 다시 시도해주시겠어요?'}, status=HTTP_204_NO_CONTENT)
        else:
            return Response({'message': '검색어를 입력하세요.'}, status=HTTP_400_BAD_REQUEST)
    #http://your-domain/main/search/?q=search-keyword


