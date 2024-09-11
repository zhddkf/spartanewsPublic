from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
# Create your views here.

class Mypage(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user = User.objects.get(username=username)
        print(user)