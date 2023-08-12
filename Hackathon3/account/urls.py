from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('mypage/', ProfileView.as_view()),
    path('mypage/commentlist/', CommentListView.as_view()),
    path('mypage/recommentlist/', RecommentListView.as_view()),
]