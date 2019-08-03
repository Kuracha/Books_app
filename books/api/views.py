from rest_framework import generics, filters
from rest_framework.views import APIView

from .serializers import BookSerializer
from ..models import Book

import requests


class BooksIndexAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'authors__author', 'language', 'published_date']


class GoogleBooksImporter(APIView):

    def search(self, value, apikey):
        params = {'q': value, 'key': apikey}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)  #TODO Evebtually change this to request.query_params
        books_json = google_books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            return bookshelf
