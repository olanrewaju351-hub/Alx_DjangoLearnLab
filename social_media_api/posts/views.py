# posts/views.py

from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from notifications.models import Notification


# -----------------------------------
# Pagination
# -----------------------------------
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# -----------------------------------
# Post ViewSet
# -----------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------------
# Comment ViewSet
# -----------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username', 'post__title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------------
# Feed View
# -----------------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')


# -----------------------------------
# Like Post
# -----------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # ✅ REQUIRED expression
    post = generics.get_object_or_404(Post, pk=pk)

    # ✅ REQUIRED expression
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        return Response(
            {"detail": "Already liked."},
            status=status.HTTP_200_OK
        )

    # ✅ REQUIRED expression
    Notification.objects.create(
        actor=request.user,
        recipient=post.author,
        verb="liked your post",
        target=post
    )

    return Response(
        {"detail": "Post liked successfully."},
        status=status.HTTP_201_CREATED
    )


# -----------------------------------
# Unlike Post
# -----------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    Like.objects.filter(
        user=request.user,
        post=post
    ).delete()

    return Response(
        {"detail": "Post unliked."},
        status=status.HTTP_200_OK
    )


# -----------------------------------
# Generic Comment Views
# -----------------------------------
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]


# -----------------------------------
# Generic Post Views
# -----------------------------------
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = SmallResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

