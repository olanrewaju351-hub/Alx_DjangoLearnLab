from django.contrib import admin
from .models import Post, Comment  # import your models

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    filter_horizontal = ('tags',)  # make tags selectable nicely in admin

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')

