from drf_spectacular.utils import extend_schema
from api.v1.serializers import FileCheckSerializer


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
