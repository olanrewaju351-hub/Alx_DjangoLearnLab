# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    A ModelForm for the Book model. Adjust `fields` as needed.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # change as needed
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author', 'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Year', 'class': 'form-control'}),
        }


