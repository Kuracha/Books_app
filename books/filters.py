from django_filters import FilterSet

from .models import Book


class BookFilter(FilterSet):

    class Meta:
        model = Book
        fields = {
            'title': ['icontains', ],
            'published_date': ['icontains', ],
            'authors__author': ['icontains', ],
            'language': ['iexact', ],
        }
