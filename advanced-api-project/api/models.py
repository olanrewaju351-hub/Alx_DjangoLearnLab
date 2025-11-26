# api/models.py
from django.db import models

class Author(models.Model):
    """
    Author model represents a book author.
    Fields:
      - name: string, the author's full name.
    Relationship:
      - One Author can have many Books (reverse relation: author.book_set or via related_name).
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book title.
    Fields:
      - title: string, the book's title.
      - publication_year: integer, the year the book was published.
      - author: ForeignKey to Author (one-to-many relationship).
    """
    title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

