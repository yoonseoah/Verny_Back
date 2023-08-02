from .views import *
from django.urls import path

app_name = "main"


urlpatterns = [
    path("posts/", PostListView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<int:comment_pk>/", CommentDetailView.as_view()),
]
