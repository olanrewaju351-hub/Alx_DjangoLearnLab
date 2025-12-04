from django.urls import path
from . import views   # <- important!

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Comment creation (ensure CommentCreateView exists in blog/views.py)
    path("posts/<int:post_pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
]

