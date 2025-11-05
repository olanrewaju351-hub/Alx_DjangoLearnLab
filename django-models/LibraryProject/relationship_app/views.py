from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# ✅ Function-based View: List all books
def list_books(request):
    books = Book.objects.all()  # <-- THIS is the required query
    return render(request, 'list_books.html', {'books': books})


# ✅ Class-based View: Display a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

