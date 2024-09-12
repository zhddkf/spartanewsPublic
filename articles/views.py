from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer


class ArticleListAPIView(APIView):
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
        filter_backends = [SearchFilter]
        search_fields = ['title', 'content', 'author']


        def get(self, request):
                articles = Article.objects.all()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data)
        

        @login_required
        def post(self, request):
                serializer = ArticleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response(serializer.data, status=201)


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
