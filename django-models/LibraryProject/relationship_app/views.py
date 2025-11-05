from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: list all books (simple HTML rendering)
def list_books(request):
    books = Book.objects.select_related('author').all()
    # render list_books.html with context {'books': books}
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: display details for a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # to reduce DB queries, prefetch related books and their authors
    def get_queryset(self):
        return Library.objects.prefetch_related("books__author")

