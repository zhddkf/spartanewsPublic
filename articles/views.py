from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer


class ArticleListAPIView(APIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
        filter_backends = [SearchFilter]
        search_fields = ['title', 'content', 'author']
