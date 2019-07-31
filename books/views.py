from django.views.generic import CreateView, ListView, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Book, IndustryIdentifier, Author, ImageLink
from .forms import IndustryIdentifiersFormSet, AuthorsFormSet, ImageLinkFormset, BookForm, SearchBookForm
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
        form_class = self.get_form_class()
        form = self.get_form(form_class)
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
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        identifiers_form = IndustryIdentifiersFormSet(self.request.POST)
        authors_form = AuthorsFormSet(self.request.POST)
        images_form = ImageLinkFormset(self.request.POST)

        if form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and images_form.is_valid():
            return self.form_valid(form, identifiers_form, authors_form, images_form)
        else:
            return self.form_invalid(form, identifiers_form, authors_form, images_form)

    def form_valid(self, form, identifiers_form, authors_form, images_form):
        self.object = form.save()
        identifiers_form.instance = self.object
        identifiers_form.save()
        authors_form.instance = self.object
        authors_form.save()
        images_form.instance = self.object
        images_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, identifiers_form, authors_form, images_form):
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            images_form=images_form,
        ))


class GoogleBooks(View):
    form_class = SearchBookForm
    template_name = 'books/import_book.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def search(self, value, apikey):
        params = {'q': value, 'key': apikey}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        books_json = google_books.json()
        if 'items' in books_json:
            bookshelf = books_json['items']
            return bookshelf

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            apikey = form.cleaned_data['apikey']
            books = self.search(keyword, apikey)
            if books is not None:
                self.add_book_to_library(books)
                return HttpResponseRedirect(reverse_lazy('import_books'))
            else:
                return HttpResponseRedirect(reverse_lazy('import_books'))

        return reverse_lazy('import_books')

