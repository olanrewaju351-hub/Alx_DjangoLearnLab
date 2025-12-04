# blog/admin.py
from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'published_date']
    list_filter = ['author', 'published_date']
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin)

