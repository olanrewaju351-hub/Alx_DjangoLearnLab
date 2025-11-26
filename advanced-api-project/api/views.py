# api/views.py
"""
Django REST Framework generic views for Book model.

We implement:
- BookListView      -> GET list of books (public)
- BookDetailView    -> GET single book (public)
- BookCreateView    -> POST create (authenticated)
- BookUpdateView    -> PUT/PATCH update (authenticated)
- BookDeleteView    -> DELETE (authenticated)

Permissions:
- Read-only (GET) allowed for any user.
- Create/Update/Delete require authentication.
"""

from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

# Default permission: allow read-only to unauthenticated users; require auth for unsafe methods.
class BookListView(generics.ListAPIView):
    """List all books. Supports optional search by title/author and ordering."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add simple search and ordering support (optional)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author']        # ?search=keyword
    ordering_fields = ['publication_year', 'title']  # ?ordering=publication_year

class BookDetailView(generics.RetrieveAPIView):
    """Retrieve a single Book by primary key (pk)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    """Create a new Book. Authentication required."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optionally, you can override perform_create to set fields programmatically:
    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

class BookUpdateView(generics.UpdateAPIView):
    """Update an existing Book (full or partial). Authentication required."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """Delete an existing Book. Authentication required."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

