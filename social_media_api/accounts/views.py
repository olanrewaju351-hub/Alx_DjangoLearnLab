# accounts/views.py
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model

from accounts.models import User, Post
from .serializers import RegisterSerializer, UserSerializer, MiniUserSerializer, PostSerializer

User = get_user_model()


class FollowingListView(generics.GenericAPIView):
    """
    Returns the list of users the current user is following.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        following = user.following.all()  # use your User model relationship
        data = MiniUserSerializer(following, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_qs = user.following.all()
        posts_qs = Post.objects.filter(author__in=following_qs).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(posts_qs, request)
        serializer = PostSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    me = request.user
    target = get_object_or_404(User, pk=user_id)
    if target == me:
        return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    me.following.add(target)
    return Response(MiniUserSerializer(target).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    me = request.user
    ta

