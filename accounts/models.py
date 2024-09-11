from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # 개인과제에서 가져온 User model 필요시 삭제
    gender_choices = [
        ('남성', 'M'),
        ('여성', 'F'),
    ]
    nickname = models.CharField(max_length=10, unique=True)
    birthday = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=2, blank=True)
    email = models.EmailField(unique=True)

######################

class Mypage(models.Model):
    nickname = models.CharField(max_length=50)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/')