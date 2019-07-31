from django.urls import path

from .views import BooksIndexAPIView

urlpatterns = [
    path('Index/', BooksIndexAPIView.as_view(), name='api_index_books'),
]
