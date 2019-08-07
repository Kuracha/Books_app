import requests

from django.views.generic import CreateView
from django.conf import settings


class BooksImporter(CreateView):

    def search_for_books(self, value, apikey=settings.APIKEY):
        params = {'q': value, 'key': apikey}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        books_json = google_books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            return bookshelf

    def add_title(self, book):
        if book['volumeInfo']['title']:
            return book['volumeInfo']['title']

    def add_published_date(self, book):
        date = book['volumeInfo'].get('publishedDate')
        if date:
            return book['volumeInfo']['publishedDate']

    def add_pages(self, book):
        pages = book['volumeInfo'].get('pageCount')
        if pages:
            return book['volumeInfo']['pageCount']

    def add_language(self, book):
        language = book['volumeInfo'].get('language')
        if language:
            return book['volumeInfo']['language']

    def add_identifier_type(self, identifier):
        if identifier["type"]:
            return identifier["type"]

    def add_identifier(self, identifier):
        if identifier["identifier"]:
            return identifier["identifier"]

    def add_author(self, author):
        if author:
            return author

    def add_small_thumbnail(self, book):
        small_thumbnail = book['volumeInfo'].get('imageLinks')
        if small_thumbnail:
            return book['volumeInfo']['imageLinks']['smallThumbnail']

    def add_thumbnail(self, book):
        thumbnail = book['volumeInfo'].get('imageLinks')
        if thumbnail:
            return book['volumeInfo']['imageLinks']['thumbnail']
