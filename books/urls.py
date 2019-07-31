from django.urls import path
from .views import BookCreate, IndexView, GoogleBooks

urlpatterns = [
    path('index/', IndexView.as_view(), name='index_books'),
    path('add_book/', BookCreate.as_view(), name='add_books'),
    path('import_book/', GoogleBooks.as_view(), name='import_books'),
]