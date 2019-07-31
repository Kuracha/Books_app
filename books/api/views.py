from rest_framework import generics, filters

from .serializers import BookSerializer
from ..models import Book


class BooksIndexAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'authors__author', 'language', 'published_date']
