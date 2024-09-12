from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer


class ArticleListAPIView(ListAPIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
        filter_backends = [SearchFilter]
        search_fields = ['author__username', 'title', 'content']

        def get(self, request, *args, **kwargs):
                articles = self.filter_queryset(self.get_queryset())
                serializer = self.get_serializer(articles, many=True)
                if not serializer.data:
                        return Response({"message": "글이 없습니다"}, status=200)
                return Response(serializer.data)
        
        def get_permissions(self):
                if self.request.method == 'POST':
                        self.permission_classes = [IsAuthenticated]
                else:
                        self.permission_classes = [AllowAny]
                return super().get_permissions()

        def post(self, request):
                serializer = ArticleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        serializer.save(author=request.user)
                        return Response(serializer.data, status=201)
                else:
                        return Response(serializer.errors, status=400)



class ArticleDetailAPIView(APIView):
        def get_object(self, pk):
                return get_object_or_404(Article, pk=pk)

        def get(self, request, pk):
                article = self.get_object(pk)
                serializer = ArticleDetailSerializer(article)
                return Response(serializer.data)

        @login_required
        def put(self, request, pk):
                article = self.get_object(pk)
                serializer = ArticleDetailSerializer(
                article, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response(serializer.data)

        @login_required
        def delete(self, request, pk):
                article = self.get_object(pk)
                article.delete()
                return Response(status=204)
