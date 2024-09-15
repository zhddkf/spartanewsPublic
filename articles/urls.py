from django.urls import path
from .views import (
    ArticleListAPIView, 
    ArticleDetailAPIView, 
    CommentAPIView,
    CommentLikeAPIView,
    TranslateAPIView
)

app_name = "articles"

urlpatterns = [
    path("<int:pk>/comments/", CommentAPIView.as_view(),name="add_delete_comment"),
    path('comments/<int:pk>/like/', CommentLikeAPIView.as_view(),name="like_comment"),
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('', ArticleListAPIView.as_view(), name='article-list'),
    path('translate/', TranslateAPIView.as_view(), name='translate')
] 

