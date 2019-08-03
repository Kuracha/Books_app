from django.views.generic import CreateView, ListView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import Book, IndustryIdentifier, Author, ImageLink
from .forms import \
    IndustryIdentifiersFormSet, \
    AuthorsFormSet, \
    ImageLinkFormset, \
    BookForm, \
    SearchBookForm, \
    AuthorsForm, \
    IndustryIdentifiersForm, \
    ImageLinkForm
from .filters import BookFilter

import requests


class IndexView(ListView):
    model = Book
    template_name = 'books/book_index.html'
    context_object_name = 'books'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs,)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        return context


class BookCreate(CreateView):
    model = Book
    template_name = 'books/book_form.html'
    form_class = BookForm
    success_url = reverse_lazy('add_books')

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class()
        identifiers_form = IndustryIdentifiersFormSet
        authors_form = AuthorsFormSet
        images_form = ImageLinkFormset
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            images_form=images_form,
        ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST)
        identifiers_form = IndustryIdentifiersFormSet(self.request.POST)
        authors_form = AuthorsFormSet(self.request.POST)
        images_form = ImageLinkFormset(self.request.POST)

        if form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and images_form.is_valid():
            return self.form_valid(form, identifiers_form, authors_form, images_form)
        else:
            return self.form_invalid(form, identifiers_form, authors_form, images_form)

    def form_valid(self, form, identifiers_form, authors_form, images_form):
        if form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
            self.object = form.save()
            identifiers_form.instance = self.object
            identifiers_form.save()
            authors_form.instance = self.object
            authors_form.save()
            images_form.instance = self.object
            images_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('index_books'))

    def form_invalid(self, form, identifiers_form, authors_form, images_form):
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            images_form=images_form,
        ))


class GoogleBooks(CreateView):
    model = Book
    form_class_book = BookForm
    form_class_search = SearchBookForm
    form_class_identifier = IndustryIdentifiersForm
    form_class_author = AuthorsForm
    form_class_thumbnail = ImageLinkForm
    template_name = 'books/import_book.html'

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

    def add_language(self, book):
        date = book['volumeInfo'].get('language')
        if date:
            return book['volumeInfo']['language']
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

    def search(self, value, apikey=""):
        params = {'q': value, 'key': apikey}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        books_json = google_books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            return bookshelf

    def get(self, request, *args, **kwargs):
        form_2 = self.form_class_search()
        return render(request, self.template_name, {'form_2': form_2})

    def post(self, request, *args, **kwargs):
        self.object = None
        form_2 = self.form_class_search(self.request.POST)
        if form_2.is_valid():
            keyword = form_2.cleaned_data['keyword']
            books = self.search(keyword)
            if books:
                for book in books:
                    title = self.add_title(book)
                    published_date = self.add_published_date(book)
                    pages = self.add_pages(book)
                    language = self.add_language(book)
                    form = self.form_class_book(
                        {'title': title,
                         'published_date': published_date,
                         'pages': pages,
                         'language': language}
                    )
                    if form.is_valid():
                        if form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
                            self.object = form.save()

                            small_thumbnail = self.add_small_thumbnail(book)
                            thumbnail = self.add_thumbnail(book)
                            form_thumbnail = self.form_class_thumbnail(
                                {'small_thumbnail': small_thumbnail,
                                 'thumbnail': thumbnail,
                                 'book': self.object.id}
                            )
                            print(form_thumbnail)
                            if form_thumbnail.is_valid():
                                form_thumbnail.save()

                        for author in book['volumeInfo']['authors']:
                            author = self.add_author(author)
                            form_author = self.form_class_author(
                                {'author': author,
                                 'book': self.object.id}
                            )
                            if form_author.is_valid():
                                form_author.save()

                        for identifier in book['volumeInfo']['industryIdentifiers']:
                            identifier_type = self.add_identifier_type(identifier)
                            identifier = self.add_identifier(identifier)
                            form_industryidentifier = self.form_class_identifier(
                                {'type': identifier_type,
                                 'identifier': identifier,
                                 'book': self.object.id}
                            )
                            if form_industryidentifier.is_valid():
                                form_industryidentifier.save()

                return HttpResponseRedirect(reverse_lazy('index_books'))
        else:
            return HttpResponseRedirect(reverse_lazy('index_books'))





        # self.object = None
        # form = self.form_class(initial={"title": "initial_data"})
        # form_2 = self.form_class_2(self.request.POST)
        # identifiers_form = IndustryIdentifiersFormSet()
        # authors_form = AuthorsFormSet()
        # images_form = ImageLinkFormset()
        # if form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and images_form.is_valid():
        # if form_2.is_valid():
        #         keyword = form_2.cleaned_data['keyword']
        #         books = self.search(keyword)
            # if books:
            #     for book in books:
            #         self.object = form.save(commit=False)
            #         self.object.title = self.add_title(book)
            #         self.object.published_date = self.add_published_date(book)
            #         self.object.pages = self.add_pages(book)
            #         self.object.language = self.add_language(book)
            #         self.object.save()
            #
            #         for identifier in book['volumeInfo']['industryIdentifiers']:
            #             identifiers_form.instance = self.object
            #             industry_identifiers = identifiers_form.save(commit=False)
            #             industry_identifiers.type = self.add_identifier_type(identifier)
            #             industry_identifiers.identifier = self.add_identifier(identifier)
            #             industry_identifiers.save()
            #
            #         for author in book['volumeInfo']['authors']:
            #             authors_form.instance = self.object
            #             authors = authors_form.save(commit=False)
            #             authors.author = self.add_author(author)
            #             authors.save()
            #
            #         images_form.instance = self.object
            #         images = images_form.save(commit=False)
            #         images.small_thumbnail = self.add_small_thumbnail(book)
            #         images.thumbnail = self.add_thumbnail(book)
            #         images.save()
            #         return HttpResponseRedirect(self.get_success_url())
            # else:
            #     return HttpResponseRedirect(reverse_lazy('index_books'))
            # return self.form_valid(form, form_2,  identifiers_form, authors_form, images_form)
        # else:
            # return self.form_invalid(form, identifiers_form, authors_form, images_form)

    # def form_valid(self, form, form_2, identifiers_form, authors_form, images_form):
        # keyword = form_2.cleaned_data['keyword']
        # books = self.search(keyword)
        # if books:
        #     for book in books:
        #         self.object = form.save(commit=False)
        #         self.object.title = self.add_title(book)
        #         self.object.published_date = self.add_published_date(book)
        #         self.object.pages = self.add_pages(book)
        #         self.object.language = self.add_language(book)
        #         self.object.save()
        #
        #         for identifier in book['volumeInfo']['industryIdentifiers']:
        #             identifiers_form.instance = self.object  #TODO Check in database if object already exist
        #             industry_identifiers = identifiers_form.save(commit=False)
        #             industry_identifiers.type = self.add_identifier_type(identifier)
        #             industry_identifiers.identifier = self.add_identifier(identifier)
        #             industry_identifiers.save()
        #
        #         for author in book['volumeInfo']['authors']:
        #             authors_form.instance = self.object
        #             authors = authors_form.save(commit=False)
        #             authors.author = self.add_author(author)
        #             authors.save()
        #
        #         images_form.instance = self.object
        #         images = images_form.save(commit=False)
        #         images.small_thumbnail = self.add_small_thumbnail(book)
        #         images.thumbnail = self.add_thumbnail(book)
        #         images.save()
        #         return HttpResponseRedirect(self.get_success_url())
        # else:
        #     return HttpResponseRedirect(reverse_lazy('index_books'))

        # if form.is_valid():
        #     keyword = form.cleaned_data['keyword']
        #     books = self.search(keyword)
        #     if books:
        #         for book in books:
        #             form_2 = self.form_class_2(self.request.POST, initial={"title": self.add_title(book)})
        #             if form_2.is_valid():
        #                 new_book = form_2.save(commit=False)
        #                 new_book.
        #
        #                 return HttpResponseRedirect(self.get_success_url())
        #             else:
        #                 return HttpResponseRedirect(reverse_lazy('index_books'))
        #     else:
        #         return HttpResponseRedirect(reverse_lazy('import_books'))
        #
        # return reverse_lazy('import_books')

