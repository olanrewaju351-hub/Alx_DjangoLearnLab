from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils import timezone

from .models import Post, Comment  # make sure Comment model exists


class TagPostListView(ListView):
    """
    Shows posts for a given tag name from the URL: /tags/<tag_name>/
    This implementation tries two common tag schemas:
      - Posts have a many-to-many Tag model: filter by tags__name
      - Posts have a tags CharField (comma-separated): filter by substring
    Adjust to match your Post model if needed.
    """
    model = Post
    template_name = "blog/posts_by_tag.html"  # create this template
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag = self.kwargs.get("tag_name", "").strip()
            return Post.objects.filter(tags__name__icontains=tag_name)

        # Try the most common pattern first: Post has a M2M Tag model (tags__name)
        qs = Post.objects.filter(tags__name__iexact=tag).order_by("-created_at")
        if qs.exists():
            return qs

        # Fallback: Post has a simple CharField 'tags' (comma-separated)
        qs = Post.objects.filter(tags__icontains=tag).order_by("-created_at")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs.get("tag_name", "")
        return ctx

# ---- Posts ----
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 10

class PostSearchView(ListView):
    """
    Search posts by title or content using the `q` GET parameter.
    Example: /search/?q=django
    """
    model = Post
    template_name = "blog/post_search.html"  # create this template
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Post.objects.none()  # or Post.objects.all() if you prefer
        # search in title or content (case-insensitive)
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        # optional: set published_date on create if you want
        # form.instance.published_date = timezone.now()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# ---- Comments ----
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Expecting URL like: /post/<int:pk>/comments/new/  (pk = post pk)
        self.post = get_object_or_404(Post, pk=kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        # optional: set created time
        # form.instance.created_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

