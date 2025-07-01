from django.urls import path
from .views import *

urlpatterns = [
    path('get-pdf/', GetPDFView.as_view(), name='get-pdf'),
    path('get-audio/', GetAudioView.as_view(), name='get-audio'),
    path('upload_zip_file/',ImagesToPDF.as_view(), name='upload-zipfile'),
    path('book/save/', BookDraftView.as_view(), name='save-as-draft'),
    path('book/publish/', BookPublishedView.as_view(), name='save-as-published'),
    path('get-book-by-isbn/<isbn>/', GetBookByISBN.as_view(), name='get-book-by-isbn'),
    path('save', BookPublishedView.as_view(), name='save-as-published'),
    path('books/', GetAllBooks.as_view(), name='get-all-books'),
]
