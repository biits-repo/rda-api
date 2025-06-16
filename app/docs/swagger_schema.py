from drf_spectacular.utils import extend_schema , OpenApiParameter , OpenApiExample
from api.v1.serializers import FileCheckSerializer , FileUploadSerializer
from rest_framework.parsers import MultiPartParser , FormParser
from drf_spectacular.openapi import OpenApiTypes
from drf_spectacular.views import SpectacularAPIView
from django.conf import settings
from django.http import HttpResponseForbidden

download_pdf_schema = extend_schema(
    operation_id="DownloadPdf",
    request=FileCheckSerializer,
    responses={200: None}, 
    description="Download the PDF file by ISBN number",
    tags=["Media Access"],
)

download_audio_schema = extend_schema(
    operation_id="DownloadAudio",
    request=FileCheckSerializer,
    responses={200: None},
    description="Download the audio file by ISBN number",
    tags=["Media Access"],
)


upload_zipfile_schema = extend_schema(
    operation_id="UploadZipfile",
    #request=FileUploadSerializer,
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary'
                },
            }
        },
    },
    responses={200: None},
    description="Upload the zip file",
    tags=["Media Access"],
)


