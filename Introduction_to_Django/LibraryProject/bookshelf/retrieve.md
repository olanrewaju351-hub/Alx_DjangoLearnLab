from bookshelf.models import Book
books = Book.objects.all()
list(books)

for bk in books:
    print(bk.id, bk.title, bk.author, bk.publication_year)


