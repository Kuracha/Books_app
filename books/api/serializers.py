from rest_framework import serializers
from ..models import Book, Author, IndustryIdentifier, ImageLink


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('author',)


class IndustryIdentifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndustryIdentifier
        fields = ('type', 'identifier')


class ImageLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageLink
        fields = ('thumbnail', 'small_thumbnail')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    industry_identifiers = IndustryIdentifierSerializer(many=True)
    images = ImageLinkSerializer(many=True)

    class Meta:
        model = Book
        fields = ('title', 'published_date', 'pages', 'language', 'authors', 'industry_identifiers', 'images')
