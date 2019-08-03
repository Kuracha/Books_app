import requests
import self as self


class GoogleSearch():

    def add_title(self, book):
        if book['volumeInfo']['title']:
            return book['volumeInfo']['title']
        else:
            return "No data"

    def add_author(self, author):
        if author:
            return author
        else:
            return None

    def add_published_date(self, book):
        date = book['volumeInfo'].get('publishedDate')
        if date:
            return book['volumeInfo']['publishedDate']
        else:
            return None

    def add_identifier_type(self, identifier):
        if identifier["type"]:
            return identifier["type"]
        else:
            return None

    def add_identifier(self, identifier):
        if identifier["identifier"]:
            return identifier["identifier"]
        else:
            return None

    def add_pages(self, book):
        pages = book['volumeInfo'].get('pageCount')
        if pages:
            return book['volumeInfo']['pageCount']
        else:
            return None

    def add_small_thumbnail(self, book):
        small_thumbnail = book['volumeInfo']['imageLinks'].get('smallThumbnail')
        if small_thumbnail:
            return book['volumeInfo']['imageLinks']['smallThumbnail']
        else:
            return None

    def add_thumbnail(self, book):
        thumbnail = book['volumeInfo']['imageLinks'].get('thumbnail')
        if thumbnail:
            return book['volumeInfo']['imageLinks']['thumbnail']
        else:
            return None

    def search(self, value, apikey="AIzaSyBjejFtcCA45MzR6MefoA7XbH6bGx9gBAc"):
        params = {'q': value, 'key': apikey}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        books_json = google_books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            for book in bookshelf:
                print("")
                title = self.add_title(book)
                print(f"title: {title}")

                for author in book['volumeInfo']['authors']:
                    authors = self.add_author(author)
                    print(f"author: {authors}")

                for identifier in book['volumeInfo']['industryIdentifiers']:
                    identifier_type = self.add_identifier_type(identifier)
                    print(f"type: {identifier_type}")
                    identifiers = self.add_identifier(identifier)
                    print(f"identifier: {identifiers}")

                pages = self.add_pages(book)
                print(f"pages: {pages}") #TODO keyError if no pageCount

                small_thumbnail = self.add_small_thumbnail(book)
                print(f"Small Thumbnail: {small_thumbnail}")
                thumbnail = self.add_thumbnail(book)
                print(f"Thumbnail: {thumbnail}")

r = GoogleSearch()
print(r.search(value="Witcher"))
