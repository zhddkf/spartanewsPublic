from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics, mixins
from .models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, get_object_or_404

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Mypage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        my_page = get_object_or_404(User, username=username)
        
        if my_page == request.user:
            serializer = UserSerializer(my_page)
            return Response(serializer.data)
        return Response({"message":"다시 시도"}, status=400)