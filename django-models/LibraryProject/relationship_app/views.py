from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Book, Library
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse

# helper test functions
def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'Member'

# Admin view: only users with profile.role == 'Admin'
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    # You can render a template or return a HttpResponse
    return render(request, 'relationship_app/admin_view.html', {})

# Librarian view
@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {})

# Member view
@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {})

# Function-based View: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based View: Library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Registration view using Django's UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('relationship_app:login')  # redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
