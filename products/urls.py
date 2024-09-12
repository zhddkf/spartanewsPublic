from django.urls import path
from . import views



urlpatterns = [
    path('', views.ArticleListAPIView.as_view() ),
    path('<int:pk>/', views.ArticleDetailAPIView.as_view() ),
    
]
