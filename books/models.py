from django.db import models
from .validators import check_if_value_is_negative, max_year_validator


class Book(models.Model):
    title = models.CharField(max_length=75, verbose_name='Book title')
    published_date = models.IntegerField(
        validators=[check_if_value_is_negative, max_year_validator], verbose_name='Publishing date')
    pages = models.IntegerField(validators=[check_if_value_is_negative] , verbose_name='Number of pages')
    language = models.CharField(max_length=2, verbose_name='Language')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class IndustryIdentifier(models.Model):
    type = models.CharField(max_length=25, verbose_name='Type')
    identifier = models.CharField(max_length=25, verbose_name='Identifier')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book', related_name='industry_identifiers')

    def __str__(self):
        return f'{self.type}: {self.identifier}'


class Author(models.Model):
    author = models.CharField(max_length=150, verbose_name='Author')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book', related_name='authors')

    def __str__(self):
        return self.author


class ImageLink(models.Model):
    small_thumbnail = models.URLField(default=None, blank=True, verbose_name='Small thumbnail')
    thumbnail = models.URLField(default=None, blank=True, verbose_name='Thumbnail')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book', related_name='images')

    def __str__(self):
        return f'{self.small_thumbnail} and {self.thumbnail} from {self.book}'
