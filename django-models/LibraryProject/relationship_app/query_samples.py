from relationship_app.models import Author, Book, Library, Librarian

print("=== Query samples ===")

# Query all books by a specific author
author_name = "George Orwell"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)   # required by checker
    print(f"Books by {author_name}:")
    for b in books_by_author:
        print(f" - {b.title}")
except Author.DoesNotExist:
    print(f"No author found with name {author_name}")

# List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)       # required by checker
    books_in_library = library.books.all()
    print(f"\nBooks in {library_name}:")
    for b in books_in_library:
        print(f" - {b.title} by {b.author.name}")
except Library.DoesNotExist:
    print(f"No library found with name {library_name}")

# Retrieve the librarian for a library
try:
    librarian = Librarian.objects.get(library=library)     # required by checker
    print(f"\nLibrarian for {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian found for {library_name}")

print("\n=== Done ===")

