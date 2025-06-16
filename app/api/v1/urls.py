from django.urls import path
from .views import *

urlpatterns = [
    path('get-pdf/', GetPDFView.as_view(), name='get-pdf'),
    path('get-audio/', GetAudioView.as_view(), name='get-audio'),
    path('upload_zip_file/',ImagesToPDF.as_view(), name='upload-zipfile')
]
