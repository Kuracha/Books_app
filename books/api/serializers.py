from rest_framework import serializers
from ..models import Book, Author, IndustryIdentifier, Thumbnail


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('author',)


class IndustryIdentifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndustryIdentifier
        fields = ('type', 'identifier')


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thumbnail
        fields = ('thumbnail', 'small_thumbnail')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    industry_identifiers = IndustryIdentifierSerializer(many=True)
    thumbnails = ThumbnailSerializer(many=True)

    class Meta:
        model = Book
        fields = ('title', 'published_date', 'pages', 'language', 'authors', 'industry_identifiers', 'thumbnails')
