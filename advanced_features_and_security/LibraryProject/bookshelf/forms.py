from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=200, required=False)


