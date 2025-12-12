# posts/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    like_post,
    unlike_post,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
)

# Router for viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Include router URLs
    *router.urls,

    # Additional endpoints for like/unlike
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('posts/<int:post_id>/unlike/', unlike_post, name='unlike-post'),

    # Optional: generic views
    path('posts-list/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments-list/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

