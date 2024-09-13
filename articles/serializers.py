from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer) :
    author = serializers.ReadOnlyField(source='author.username')

    class Meta :
        model=Article
        fields='__all__'

class ArticleDetailSerializer(ArticleSerializer):
    # comments= CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)