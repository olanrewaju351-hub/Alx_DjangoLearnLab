# api/serializers.py
from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields and performs validation.
    The validate_publication_year method ensures the year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future."""
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author and includes a nested list of their books.
    Uses BookSerializer to represent each related Book instance.
    The 'books' field is read-only here (serialization from Author -> nested Books).
    """
    # nest BookSerializer and set many=True because one author has many books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

