from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to show in the change list (table) view
    list_display = ("id", "title", "author", "publication_year")
    # Add filters in the right sidebar
    list_filter = ("author", "publication_year")
    # Add a search box (searches these fields)
    search_fields = ("title", "author")
    # Optional: default ordering
    ordering = ("-publication_year", "title")
    # Optional: number of items per page in the list view
    list_per_page = 25

