from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, null=True, blank=True)

# class Mypage(models.Model):
#     nickname = models.CharField(max_length=50)
#     email = models.EmailField()
#     image = models.ImageField(upload_to='images/')