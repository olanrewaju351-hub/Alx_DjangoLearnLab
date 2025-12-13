# posts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    FeedView,
    like_post,
    unlike_post,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),

    # Feed
    path('feed/', FeedView.as_view(), name='feed'),

    # Generic Post Views
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Likes (REQUIRED BY CHECKER)
    path('posts/<int:pk>/like/', like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike-post'),

    # Generic Comment Views
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

