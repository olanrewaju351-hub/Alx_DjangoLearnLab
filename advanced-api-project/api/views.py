from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend   # <<-- add this import
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as django_filters



class BookListView(generics.ListAPIView):
    """
    List all books with filtering, searching and ordering enabled.

    Examples:
      - /api/books/?title=Dune
      - /api/books/?author=George%20Orwell
      - /api/books/?publication_year=1949
      - /api/books/?search=Orwell
      - /api/books/?ordering=publication_year
      - /api/books/?ordering=-publication_year  (descending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Enable the three backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields you want to allow simple exact-filtering on:
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields you want to allow searching (text search, looks for partial matches)
    # NOTE: if author is a FK, you might want 'author__name' instead (adjust to your model)
    search_fields = ['title', 'author']

    # Fields allowed for ordering
    ordering_fields = ['title', 'publication_year']
    # default ordering (optional)
    ordering = ['title']

    # Permissions: allow read-only to anyone; writing is handled in the create/update views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can create


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can update


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can delete

