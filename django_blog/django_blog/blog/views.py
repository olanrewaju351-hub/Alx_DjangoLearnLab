# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone

def index(request):
    posts = Post.objects.all()  # ordering from Meta: newest first
    return render(request, 'blog/index.html', {'posts': posts, 'year': timezone.now().year})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'year': timezone.now().year})

