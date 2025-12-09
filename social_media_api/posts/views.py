from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend  # optional if you add django-filter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Pagination
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Post viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('comments').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comment viewset
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = SmallResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username', 'post__title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        # author is logged-in user; client should send 'post' id in payload
        serializer.save(author=self.request.user)

