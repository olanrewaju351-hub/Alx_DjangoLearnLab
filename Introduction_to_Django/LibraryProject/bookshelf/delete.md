from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
result = book.delete()
result
Book.objects.all()

