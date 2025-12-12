# posts/views.py
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from accounts.models import User
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification
from notifications.utils import create_notification  # if you have this utility

# Pagination
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# -------------------------------
# Post & Comment ViewSets
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username', 'post__title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# Feed View
# -------------------------------
class FeedView(generics.ListAPIView):
    """
    Returns posts from users the request.user is following (paginated).
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Post.objects.none()
        following_users = user.following.all()  # assumes `following` related_name in User model
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

# -------------------------------
# Like / Unlike Endpoints
# -------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create notification
def create_notification(actor, recipient, verb, target=None):
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        target=target
    )

    create_notification(actor=request.user, recipient=post.author, verb='liked your post', target=post)

    return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------
# Generic Comment Views (Optional)
# -------------------------------
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
