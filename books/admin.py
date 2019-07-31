from django.contrib import admin

from .models import IndustryIdentifier, Book, Author, ImageLink


class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'published_date', 'pages', 'language',)
    search_fields = ('title', )
    ordering = ('published_date', 'title')


admin.site.register(Book, BookAdmin)


class IndustryIdentifiersAdmin(admin.ModelAdmin):
    list_display = ('type', 'identifier', 'book')
    search_fields = ('book', 'type')


admin.site.register(IndustryIdentifier, IndustryIdentifiersAdmin)


class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('author', 'book')
    search_fields = ('author', )


admin.site.register(Author, AuthorsAdmin)


class ImageLinksAdmin(admin.ModelAdmin):
    list_display = ('small_thumbnail', 'thumbnail', 'book')


admin.site.register(ImageLink, ImageLinksAdmin)
