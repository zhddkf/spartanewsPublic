from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Article, Comment, LikeComments, LikeArticle
from .serializers import (
        ArticleSerializer, 
        ArticleDetailSerializer,
        CommentSerializer,
        )
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
        page_size = 5
        page_size_query_param = 'page_size'
        max_page_size = 100

class ArticleListAPIView(ListAPIView):
        queryset = Article.objects.all().order_by('-created_at') # 오름차순 정렬, 내림차순 '-created'
        serializer_class = ArticleSerializer
        filter_backends = [SearchFilter]
        search_fields = ['author__username', 'title', 'content']
        pagination_class = CustomPagination

        # def get(self, request, *args, **kwargs): # 글 전체 목록
        #         articles = self.filter_queryset(self.get_queryset())
        #         serializer = self.get_serializer(articles, many=True)
                
        #         if not serializer.data: # 글 검색 기능
        #                 return Response({"message": "글이 없습니다"}, status=200)
        #         return Response(serializer.data)
        
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

        def put(self, request, pk): # 글 수정
                if request.user.is_authenticated: # 로그인 상태일때
                        article = self.get_object(pk)
                        serializer = ArticleDetailSerializer(
                        article, data=request.data, partial=True)
                        if serializer.is_valid(raise_exception=True):
                                serializer.save()
                        return Response(serializer.data)
                return Response({'로그인 후 이용 가능합니다'}, status=400)
                
        def delete(self, request, pk): # 글 삭제
                if request.user.is_authenticated: # 로그인 상태일때
                        article = self.get_object(pk)
                        article.delete()
                        return Response({'글 삭제가 완료되었습니다'},status=204)
                return Response({'로그인 후 이용 가능합니다'}, status=400)
        
        def post(self, request, pk):
                article = self.get_object(pk)
                if article.like_users.filter(pk=request.user.pk).exists():
                        like = get_object_or_404(LikeArticle, article=pk, user=request.user.pk)
                        if like.is_deleted == True:
                                like.soft_deleted()
                                data = {"pk": f"{pk} 글 좋아요 취소"}
                                return Response(data, status=200)
                        elif like.is_deleted == False:
                                like.restore()
                                data = {"pk": f"{pk} 글 좋아요 부활"}
                                return Response(data, status=200)
                else:
                        article.like_users.add(request.user)
                        data = {"pk": f"{pk} 글 좋아요 완료"}
                        return Response(data, status=200)

class CommentAPIView(APIView):
        permission_classes = [IsAuthenticated]
        def get_object(self, pk):
                return get_object_or_404(Comment, pk=pk)
        def post(self, request, pk):
                article = get_object_or_404(Article, pk=pk)
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        serializer.save(article=article)
                        return Response(serializer.data, status=201)
        def delete(self, request, pk):
                comment = self.get_object(pk)
                comment.delete()
                data = {"pk": f"{pk} 삭제됨"}
                return Response(data, status=200)


class CommentLikeAPIView(APIView):
        def post(self, request, pk):
                comment = self.get_object(pk)
                if comment.like_users.filter(pk=request.user.pk).exists():
                        like = get_object_or_404(LikeComments, comment=pk, user=request.user.pk)
                        if like.is_deleted == True:
                                like.soft_deleted()
                                data = {"pk": f"{pk} 댓글 추천 취소됨"}
                                return Response(data, status=200)
                        elif like.is_deleted == False:
                                like.restore()
                                data = {"pk": f"{pk} 댓글 추천 부활됨"}
                                return Response(data, status=200)
                else:
                        comment.like_users.add(request.user)
                        data = {"pk": f"{pk} 댓글 추천 완료됨"}
                        return Response(data, status=200)
                

class TranslateAPIView(APIView):
        permission_classes = [AllowAny]
        def post(self, request):
                # LLM 모델 인스턴스 생성
                llm = ChatOpenAI(model="gpt-4o-mini")

                # 요청에서 번역할 텍스트 가져오기
                text_to_translate = request.data.get('text', '')

                # LLM에 들어갈 메시지 설정
                messages = [
                SystemMessage(content="Translate the following text from English to Korean."),
                HumanMessage(content=text_to_translate),
                ]

                # LLM 호출하여 결과 받기
                result = llm.invoke(messages)

                # 결과 반환
                return Response({'번역': result})