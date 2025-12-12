from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()  # optional: whether request.user liked

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'created_at', 'updated_at',
            'likes_count', 'liked_by_user',
        ]
        read_only_fields = ['likes_count', 'liked_by_user']

    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if not request or request.user.is_anonymous:
            return False
        return Like.objects.filter(post=obj, user=request.user).exists()


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'author_username', 'created_at', 'updated_at']

