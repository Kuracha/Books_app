from django import forms
from django.forms.models import inlineformset_factory

from .models import Book, IndustryIdentifier, Author, ImageLink


class IndustryIdentifiersForm(forms.ModelForm):

    class Meta:
        model = IndustryIdentifier
        exclude = ()


IndustryIdentifiersFormSet = inlineformset_factory(
    Book, IndustryIdentifier, form=IndustryIdentifiersForm,
    fields=['type', 'identifier'], extra=2, can_delete=False
)


class AuthorsForm(forms.ModelForm):

    class Meta:
        model = Author
        exclude = ()


AuthorsFormSet = inlineformset_factory(
    Book, Author, form=AuthorsForm, fields=['author', ], extra=3, can_delete=False
)


class ImageLinkForm(forms.ModelForm):

    class Meta:
        model = ImageLink
        exclude = ()


ImageLinkFormset = inlineformset_factory(
    Book, ImageLink, form=ImageLinkForm, fields=['small_thumbnail', 'thumbnail'], extra=1, can_delete=False
)


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ()


class SearchBookForm(forms.Form):
    keyword = forms.CharField(max_length=100)
    apikey = forms.CharField(max_length=100)
