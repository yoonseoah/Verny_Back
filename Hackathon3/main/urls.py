from .views import *
from django.urls import path

app_name = "main"

# 작품목록조회, 작품 해설(detail) 조회, 댓글 조회, 작성, 삭제, 수정 url.
urlpatterns = [
    path("posts/", PostListView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<int:comment_pk>/", CommentDetailView.as_view()),
    path('posts/<int:pk>/scrap/', PostScrapView.as_view(), name='post_scrap'),
]
