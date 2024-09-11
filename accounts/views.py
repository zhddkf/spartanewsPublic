from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer,PasswordCheckSerializer
from rest_framework import generics,mixins
from django.shortcuts import render, get_object_or_404

class SignupAPIView(APIView): # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView): # 로그아웃
    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh is None:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAPIView(APIView): # 회원탈퇴
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = PasswordCheckSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.soft_delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Mypage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        my_page = get_object_or_404(User, username=username)
        
        if my_page == request.user:
            serializer = UserSerializer(my_page)
            return Response(serializer.data)
        return Response({"message":"다시 시도"}, status=400)