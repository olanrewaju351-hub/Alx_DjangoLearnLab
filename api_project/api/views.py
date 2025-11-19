# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import AllowAny

class BookList(generics.ListAPIView):
    """
    Simple list endpoint (keeps your previous ListAPIView).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Book model:
    - list (GET /books_all/)
    - retrieve (GET /books_all/{id}/)
    - create (POST /books_all/)
    - update (PUT /books_all/{id}/)
    - partial_update (PATCH /books_all/{id}/)
    - destroy (DELETE /books_all/{id}/)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # change to proper auth in production

