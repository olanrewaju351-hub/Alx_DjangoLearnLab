# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadCreateUpdateOnly  # import custom permission

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Use the custom permission: read anyone, create/update authenticated, delete only staff
    permission_classes = [IsAdminOrReadCreateUpdateOnly]

