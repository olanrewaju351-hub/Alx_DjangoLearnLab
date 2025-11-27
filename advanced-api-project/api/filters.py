# api/filters.py
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # example: publication_year range (gte/lte)
    publication_year_min = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year_max = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author': ['exact', 'icontains'],
            # publication_year handled with min/max above, but exact also possible
            'publication_year': ['exact'],
        }

