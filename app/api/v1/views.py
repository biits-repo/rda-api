import os
import mimetypes
from django.conf import settings
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from docs.swagger_schema import *
from .serializers import FileCheckSerializer


class GetPDFView(APIView):
    @download_pdf_schema
    def post(self, request):
        serializer = FileCheckSerializer(data=request.data)

        if serializer.is_valid():
            isbn = serializer.validated_data['isbn_number']
            filename = f"{isbn}.pdf"
            file_path = os.path.join(settings.PDF_DIR, filename)

            if os.path.isfile(file_path):
                return FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    content_type='application/pdf',
                    filename=filename
                )
            return Response({'message': 'PDF file not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAudioView(APIView):
    @download_audio_schema
    def post(self, request):
        serializer = FileCheckSerializer(data=request.data)

        if serializer.is_valid():
            isbn = serializer.validated_data['isbn_number']
            filename = f"{isbn}.mp3"
            file_path = os.path.join(settings.AUDIO_DIR, filename)

            if os.path.isfile(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                return FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    content_type=content_type or 'application/octet-stream',
                    filename=filename
                )
            return Response({'message': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
