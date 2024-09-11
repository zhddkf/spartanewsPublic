from rest_framework import serializers
from .models import User  # User 모델 임포트

class MypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'gender','nickname','email']