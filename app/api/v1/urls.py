from django.urls import path
from .views import *

urlpatterns = [
    path('get-pdf/', GetPDFView.as_view(), name='get-pdf'),
    path('get-audio/', GetAudioView.as_view(), name='get-audio'),
    path('upload_zip_file/',ImagesToPDF.as_view(), name='upload-zipfile'),
    path('books/draft/', BookDraftView.as_view(), name='save-as-draft'),
    path('books/publish/', BookPublishedView.as_view(), name='save-as-published'),
    path('books/', GetAllBooks.as_view(), name='get-all-books'),
]
