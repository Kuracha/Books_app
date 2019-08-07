from django.contrib import messages
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django_filters.views import FilterView

from .caches import CacheMixin
from .books_importer import BooksImporter
from .filters import BookFilter
from .models import Book
from .forms import \
    IndustryIdentifiersFormSet, \
    AuthorsFormSet, \
    ThumbnailLinkFormset, \
    BookForm, \
    SearchBookForm, \
    AuthorsForm, \
    IndustryIdentifiersForm, \
    ThumbnailLinkForm


class IndexView(CacheMixin, FilterView):
    cache_timeout = 90
    filterset_class = BookFilter
    model = Book
    template_name = 'books/book_index.html'
    paginate_by = 4
    context_object_name = 'books'
    queryset = Book.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs,)
    #     context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
    #     return context


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
        thumbnail_form = ThumbnailLinkFormset
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            thumbnail_form=thumbnail_form,
        ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST)
        identifiers_form = IndustryIdentifiersFormSet(self.request.POST)
        authors_form = AuthorsFormSet(self.request.POST)
        thumbnail_form = ThumbnailLinkFormset(self.request.POST)

        if form.is_valid() and identifiers_form.is_valid() and authors_form.is_valid() and thumbnail_form.is_valid():
            return self.form_valid(form, identifiers_form, authors_form, thumbnail_form)
        else:
            return self.form_invalid(form, identifiers_form, authors_form, thumbnail_form)

    def form_valid(self, form, identifiers_form, authors_form, thumbnail_form):
        if form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
            self.object = form.save()
            identifiers_form.instance = self.object
            identifiers_form.save()
            authors_form.instance = self.object
            authors_form.save()
            thumbnail_form.instance = self.object
            thumbnail_form.save()

            return HttpResponseRedirect(reverse_lazy('add_books'))
        else:
            return HttpResponseRedirect(reverse_lazy('add_books'))

    def form_invalid(self, form, identifiers_form, authors_form, thumbnail_form):
        return self.render_to_response(self.get_context_data(
            form=form,
            identifiers_form=identifiers_form,
            authors_form=authors_form,
            thumbnail_form=thumbnail_form,
        ))


class GoogleBooks(BooksImporter):
    model = Book
    form_class_book = BookForm
    form_class_search = SearchBookForm
    form_class_identifier = IndustryIdentifiersForm
    form_class_author = AuthorsForm
    form_class_thumbnail = ThumbnailLinkForm
    template_name = 'books/import_book.html'

    def get(self, request, *args, **kwargs):
        form_2 = self.form_class_search()
        return render(request, self.template_name, {'form_2': form_2})

    def post(self, request, *args, **kwargs):
        self.object = None
        form_2 = self.form_class_search(self.request.POST)
        if form_2.is_valid():
            keyword = form_2.cleaned_data['keyword']
            books = self.search_for_books(keyword)

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
                    if form.is_valid() and form.cleaned_data["title"] not in Book.objects.values_list('title', flat=True):
                        self.object = form.save()

                        small_thumbnail = self.add_small_thumbnail(book)
                        thumbnail = self.add_thumbnail(book)
                        form_thumbnail = self.form_class_thumbnail(
                            {'small_thumbnail': small_thumbnail,
                                'thumbnail': thumbnail,
                                'book': self.object.id}
                        )
                        if form_thumbnail.is_valid():
                            form_thumbnail.save()

                        if book['volumeInfo'].get('authors'):
                            for author in book['volumeInfo']['authors']:
                                author = self.add_author(author)
                                form_author = self.form_class_author(
                                    {'author': author,
                                        'book': self.object.id}
                                )
                                if form_author.is_valid():
                                    form_author.save()

                        if book['volumeInfo'].get('industryIdentifiers'):
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

                messages.success(request, "Books added to database, "
                                          "remember that if added books already exist in database "
                                          "then won't be added second time")
                return HttpResponseRedirect(reverse_lazy('import_books'))
            else:
                messages.warning(request, "Couldn't find any books with provided keyword")
                return HttpResponseRedirect(reverse_lazy('import_books'))

        else:
            messages.error(request, "Provided keyword is invalid")
            return HttpResponseRedirect(reverse_lazy('import_books'))



