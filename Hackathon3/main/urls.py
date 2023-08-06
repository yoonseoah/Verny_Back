from .views import *
from django.urls import path

app_name = "main"

# 작품목록조회, 작품 해설(detail) 조회, 댓글 조회, 작성, 삭제, 수정 url.
urlpatterns = [
    path("posts/", PostListView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:pk>/comments/", CommentView.as_view()),
    #path("comments/<int:comment_pk>/", CommentDetailView.as_view()),
    path("comments/<int:comment_pk>/likes/", CommentDetailView.as_view()),
    #path("comments/<int:comment_pk>/recomments/", RecommentView.as_view()),
    path("comments/<int:comment_pk>/recomments/relikes", RecommentView.as_view()),
    #path("comments/<int:comment_pk>/recomments/<int:recomment_pk>/",RecommentDetailView.as_view()),
    #path("comments/<int:pk>/like/", Comment, name="toggle-like"),  # 댓글, 대댓글 좋아요 개수 update url
    path("posts/<int:pk>/scrap/", PostScrapView.as_view()),
    path("search/", SearchView.as_view()),
    
]
