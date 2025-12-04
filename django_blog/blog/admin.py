# blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'published_date']
    list_filter = ['author', 'published_date']
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin, Tag)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
