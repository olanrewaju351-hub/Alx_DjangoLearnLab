from relationship_app.models import Author, Book, Library, Librarian

print("Query: all books by George Orwell")
try:
    author = Author.objects.get(name="George Orwell")
    for book in author.books.all():
        print(book.title)
except Author.DoesNotExist:
    print("Author not found")

print("\nQuery: all books in Central Library")
try:
    library = Library.objects.get(name="Central Library")
    for book in library.books.all():
        print(book.title, "-", book.author.name)
except Library.DoesNotExist:
    print("Library not found")

print("\nQuery: librarian for Central Library")
try:
    library = Library.objects.get(name="Central Library")
    print(library.librarian.name)
except Exception as e:
    print("Could not retrieve librarian:", e)
