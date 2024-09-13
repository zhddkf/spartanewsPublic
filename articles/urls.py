from django.urls import path
from .views import (
    ArticleListAPIView, 
    ArticleDetailAPIView, 
    AddCommentAPIView,
    CommentDetailAPIView
)


urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('<int:pk>/', ArticleDetailAPIView.as_view()),
    path(
        "<int:pk>/comments/",
        AddCommentAPIView.as_view(),
        name="add_comment",
    ),
    path(
        "comments/<int:pk>/",
        CommentDetailAPIView.as_view(),
        name="comment_detail",
    ),
    path(
        'comments/<int:pk>/like', 
        CommentDetailAPIView.as_view(),
        name="like_comment"
    )
]