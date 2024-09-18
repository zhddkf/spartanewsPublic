from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings

User = get_user_model()


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=True)

    def soft_deleted(self):
        self.is_deleted = False
        self.save()

    def restore(self):
        self.is_deleted = True
        self.save()
    
    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # 카테고리의 이름을 담는 필드, unique=True로 하여 같은 이름의 카테고리를 만들지 못하도록 함

class Article(models.Model):
    # on_delete=models.SET_NULL 은 포스트 삭제 시 카테고리만 null이 되게끔 하기 위해 작성한 코드
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="like_article", through="LikeArticle")
    image = models.ImageField(upload_to="%Y/%m/%d")

class LikeArticle(SoftDelete):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"    
    )
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name="like_comment", through="LikeComments")

class LikeComments(SoftDelete):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)