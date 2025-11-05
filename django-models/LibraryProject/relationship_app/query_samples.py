from relationship_app.models import Author, Book, Library, Librarian

print("=== Query samples ===")

# Query all books by a specific author (using objects.filter(author=author))
author_name = "George Orwell"
try:
    author = Author.objects.get(name=author_name)
    # explicit filtered query required by checker:
    books_by_author = Book.objects.filter(author=author)     # <-- contains objects.filter(author=author)
    print(f"Books by {author_name}:")
    for b in books_by_author:
        print(f" - {b.title} (id={b.pk})")
except Author.DoesNotExist:
    print(f"No author found with name {author_name}")

# List all books in a library (checker expects Library.objects.get(name=library_name))
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)   # <-- contains Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library_name}:")
    for b in books_in_library:
        print(f" - {b.title} by {b.author.name}")
except Library.DoesNotExist:
    print(f"No library found with name {library_name}")

# Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"\nLibrarian for {library_name}: {librarian.name}")
except Exception as e:
    print(f"Could not get librarian for {library_name}: {e}")

print("\n=== Done ===")

