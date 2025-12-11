from django.contrib.auth import get_user_model
from .models import Post
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )

        # Create Token for the user
        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serialize basic user info."""
    class Meta:
        model = User
        # adapt fields to your user model
        fields = ("id", "username", "email",)
        read_only_fields = ("id", "username")

class FollowActionSerializer(serializers.Serializer):
    target_username = serializers.CharField()
    action = serializers.ChoiceField(choices=['follow','unfollow','toggle'], default='toggle')

class MiniUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
