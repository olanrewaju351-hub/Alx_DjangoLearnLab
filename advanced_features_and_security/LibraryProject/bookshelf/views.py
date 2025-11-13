from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm  # create a simple ModelForm (see below)

def book_search(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.none()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        # Use ORM filtering (parameterized) — safe from SQL injection
        if q:
            # ILIKE-style behaviour (case-insensitive) limited to Django DB syntax:
            books = Book.objects.filter(title__icontains=q)
        else:
            books = Book.objects.all()
    return render(request, 'bookshelf/book_search.html', {'form': form, 'books': books})


def book_list(request):
    """
    Displays a list of all books in the library.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Add'})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:list_books')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# A view that requires only view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def detail_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})

