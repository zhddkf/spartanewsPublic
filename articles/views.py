from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Article, Comment, LikeComments
from .serializers import (
        ArticleSerializer, 
        ArticleDetailSerializer,
        CommentSerializer,
        )


class ArticleListAPIView(ListAPIView):
        queryset = Article.objects.all().order_by('-created_at') # 오름차순 정렬, 내림차순 '-created'
        serializer_class = ArticleSerializer
        filter_backends = [SearchFilter]
        search_fields = ['author__username', 'title', 'content']

        def get(self, request, *args, **kwargs): # 글 전체 목록
                articles = self.filter_queryset(self.get_queryset())
                serializer = self.get_serializer(articles, many=True)
                if not serializer.data: # 글 검색 기능
                        return Response({"message": "글이 없습니다"}, status=200)
                return Response(serializer.data)
        
        def get_permissions(self):
                if self.request.method == 'POST': # 로그인 권한 설정
                        self.permission_classes = [IsAuthenticated]
                else:
                        self.permission_classes = [AllowAny]
                return super().get_permissions()

        def post(self, request): # 글 생성
                serializer = ArticleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        serializer.save(author=request.user)
                        return Response(serializer.data, status=201)
                else:
                        return Response(serializer.errors, status=400)


class ArticleDetailAPIView(APIView):
        def get_object(self, pk):
                return get_object_or_404(Article, pk=pk)

        def get(self, request, pk): # 글 상세페이지
                article = self.get_object(pk)
                serializer = ArticleDetailSerializer(article)
                return Response(serializer.data)

        @login_required
        def put(self, request, pk): # 글 수정
                article = self.get_object(pk)
                serializer = ArticleDetailSerializer(
                article, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response(serializer.data)

        @login_required
        def delete(self, request, pk): # 글 삭제
                article = self.get_object(pk)
                article.delete()
                return Response(status=204)


class AddCommentAPIView(APIView):
        permission_classes = [IsAuthenticated]
        def post(self, request, pk):
                article = get_object_or_404(Article, pk=pk)
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        serializer.save(article=article)
                        return Response(serializer.data, status=201)


class CommentDetailAPIView(APIView):
        permission_classes = [IsAuthenticated]
        def get_object(self, pk):
                return get_object_or_404(Comment, pk=pk)
        def delete(self, request, pk):
                comment = self.get_object(pk)
                comment.delete()
                data = {"pk": f"{pk} 삭제됨"}
                return Response(data, status=200)
        def post(self, request, pk):
                comment = self.get_object(pk)
                if comment.like_users.filter(pk=request.user.pk).exists():
                        like = get_object_or_404(LikeComments, comment=pk, user=request.user.pk)
                        if like.is_deleted == True:
                                like.soft_deleted()
                                data = {"pk": f"{pk} 추천 취소됨"}
                                return Response(data, status=200)
                        elif like.is_deleted == False:
                                like.restore()
                                data = {"pk": f"{pk} 추천 부활됨"}
                                return Response(data, status=200)
                else:
                        comment.like_users.add(request.user)
                        data = {"pk": f"{pk} 추천 완료됨"}
                        return Response(data, status=200)