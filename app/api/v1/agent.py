from mistralai import Mistral
import os
from dotenv import load_dotenv
from gtts import gTTS
from pathlib import Path
from django.conf import settings
from time import perf_counter
from .logger_config import setup_logger
import logging

load_dotenv()
setup_logger()
class ModelMistral:
    

    def __init__(self):
        pass



    def get_metric(self,text):

        media_dir = Path(settings.MEDIA_DIR) 

        media_dir.mkdir(exist_ok=True)

        metric_file_path = os.path.join(media_dir , 'metric_file')

        print(metric_file_path)

        try:
            with open(f"{metric_file_path}.txt" , 'a') as f:
                f.seek(0)
                f.write(text)
                f.write("\n")
        
        except Exception as error:
            
            print(f"THIS IS THE EXCEPTION {str(error)}")



    def get_file_path(self,file_name):

        text_file = file_name.split('\\')[-1]
        text_file = text_file.replace(".pdf",".txt")
        
        audio_file = file_name.split('\\')[-1]
        audio_file = audio_file.replace(".pdf",".mp3")


        media_dir = Path(settings.MEDIA_DIR) 
        media_dir.mkdir(exist_ok=True)
        output_path = os.path.join(media_dir , 'Output')
        output_dir = Path(output_path)
        output_dir.mkdir(exist_ok=True)

        text_file_path = os.path.join(output_dir , text_file)

        audio_file_path = os.path.join(output_dir , audio_file)
        
        return text_file_path , audio_file_path
        


    def get_model(self):

        try:
            api_key = os.environ.get("API_KEY_MISTRAL")
            self.model = "mistral-small-latest"
            self.client = Mistral(api_key=api_key)

            return self.client
        
        except Exception as error:
            
            return str(error)
        

    def extract_and_convert_to_audio(self , file_path):

        
        mistral_start_time = perf_counter()
        client = self.get_model()
        
        text_file_path , audio_file_path = self.get_file_path(file_path)
        
        print(f"############# {text_file_path}")

        print(f"############# {audio_file_path}")

    

        try:
            uploaded_pdf = client.files.upload(
            file={
                    "file_name": file_path,
                    "content": open(file_path, "rb"),
                },
                purpose="ocr"
            ) 

            retrieved_file = client.files.retrieve(file_id=uploaded_pdf.id)

            #getting signed url
            signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

            ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            },
            include_image_base64=True
            )
            
            resp = "\n\n".join([f"{i+1}\n{ocr_response.pages[i].markdown}" for i in range(len(ocr_response.pages))])
            

            mistral_completion_time = perf_counter()
            
            total_time_taken = f"Total time taken by mistral for extracting text from pdf is {(mistral_completion_time - mistral_start_time) : .2f} seconds"

            print(total_time_taken)
            self.get_metric(total_time_taken)

            print(audio_file_path)

            with open(text_file_path , 'w') as f:
                f.write(resp) 
                
            resp = str(resp)
            tts = gTTS(resp)
            tts.save(audio_file_path)

            return "Process completed successfully"

        except Exception as error:
            return str(error)
        
    