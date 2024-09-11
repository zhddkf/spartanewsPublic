from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics
from .models import User
from rest_framework.permissions import IsAuthenticated

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Mypage(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user = User.objects.get(username=username)
        print(user)