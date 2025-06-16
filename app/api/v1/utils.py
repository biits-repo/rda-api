from gtts import gTTS
from .agent import ModelMistral
from .storage import handle_upload_file 
import os
from django.conf import settings
from pathlib import Path

def extract_and_convert_to_audio(pdf_file_path, text_file_path, audio_file_path):
    """
    Extracts text from a PDF using OCR and converts it to an audio file.

    Args:
        pdf_file_path (str): Path to the input PDF file.
        text_file_path (str): Path where the extracted text will be saved.
        audio_file_path (str): Path where the audio file will be saved.

    Returns:
        str: "success" on success, or an error message.
    """
    try:
        model_obj = ModelMistral()
        client = model_obj.get_model()
    except Exception as error:
        return f"Model initialization failed: {str(error)}"

    try:
        with open(pdf_file_path, "rb") as file:
            uploaded_pdf = client.files.upload(
                file={
                    "file_name": os.path.basename(pdf_file_path),
                    "content": file,
                },
                purpose="ocr"
            )

        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            },
            include_image_base64=True
        )

        # Join OCR text from all pages
        extracted_text = "\n\n".join(
            f"{i + 1}\n{page.markdown}" for i, page in enumerate(ocr_response.pages)
        )

        # Write to text file
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        # Convert to audio
        tts = gTTS(text=str(extracted_text))
        tts.save(audio_file_path)

        return "success"

    except Exception as error:
        return f"Processing failed: {str(error)}"


def get_media_dir():

    """
    Creates and returns the media directory path

    ARGS:
        NONE

    Returns:
        str : media directory path
    
    """


    media_dir = Path(settings.MEDIA_DIR) 

    media_dir.mkdir(exist_ok=True)
    
    return media_dir


