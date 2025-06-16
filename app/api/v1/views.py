import os
import mimetypes
from django.conf import settings
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from docs.swagger_schema import *
from .serializers import FileCheckSerializer
import zipfile
import shutil
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from .utils import get_media_dir 
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser , FormParser
from redis import Redis
from rq import Queue
from .agent import ModelMistral
from time import perf_counter

load_dotenv()

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



class ImagesToPDF(APIView):


    serializer_class = FileUploadSerializer    
    parser_classes = (MultiPartParser , FormParser)

    def remove_images(self , file_name):

        get_dir = get_media_dir()
        unzipped_path = os.path.join(get_dir , 'unzipped')
        image_path = os.path.join(unzipped_path , file_name)

       
        try:
            shutil.rmtree(image_path)
            print("Directory removed successfully")
        except Exception as error:
            print("Directory doesn't exists")




    def convert_images_to_pdf(self, image_dir , pdf_name):
        
        pil_images = []
        
        media_dir = get_media_dir()

        pdf_path = os.path.join(media_dir,'Output')

        pdf_file_path = Path(pdf_path)
        pdf_file_path.mkdir(exist_ok=True)

        pdf_full_path = os.path.join(pdf_file_path , pdf_name)

        for image in image_dir:
            
            try:
                with Image.open(image) as img:
                    
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                   
                    max_size = (1200, 1600)  
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Create a copy to avoid issues with file handles
                    img_copy = img.copy()
                    pil_images.append(img_copy)
            except Exception as error:
                print(str(error))

        

        try:

            first_image = pil_images[0]
            other_images = pil_images[1:] if len(pil_images) > 1 else []

            print(f"{pdf_file_path}")
            first_image.save(
                pdf_full_path,
                format='PDF',
                save_all=True,
                append_images=other_images,
                resolution=100.0,
                quality=85
            )

            return pdf_full_path
        
        except Exception as error:
            print(str(error))
    
    @upload_zipfile_schema
    def post(self,request,*args,**kwargs):

        media_dir = get_media_dir()
        model = ModelMistral()

        input_dir = Path(os.path.join(media_dir , 'Input'))
        input_dir.mkdir(exist_ok=True)

        request_data = request.FILES.get('file')

        file_name = request_data.name.split(".")[0]

        mime_type , _ = mimetypes.guess_type(request_data.name)



        if mime_type == "application/x-zip-compressed":

            serializer = FileUploadSerializer(data=request.data)

            start_time = perf_counter()

            if serializer.is_valid():
                
                uploaded_file = serializer.validated_data['file']

                input_dir = os.path.join(media_dir , 'Input')

                os.makedirs(input_dir, exist_ok=True)

                input_file_path = os.path.join(input_dir , uploaded_file.name)

                
                try:
                    with open(input_file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    
                    pdf_name = uploaded_file.name.replace(".zip",".pdf")
                    
                    get_media = get_media_dir()


                    unzipped_dir = os.path.join(get_media , 'unzipped')
                    
                    unzipped_dir = Path(unzipped_dir)
                    unzipped_dir.mkdir(exist_ok=True)

                    extracted_images = []

                    with zipfile.ZipFile(uploaded_file,'r') as zip_ref:

                        file_list = zip_ref.namelist()

                        
                        for file in file_list:
                            
                            zip_ref.extract(file , unzipped_dir)

                            extracted_path = os.path.join(unzipped_dir, file)

                            extracted_images.append(extracted_path)
                            
                        
                            extracted_images.sort()
                    
                    output_file_path = self.convert_images_to_pdf(extracted_images , pdf_name)

                        
                    end_time = perf_counter()

                    total_taken_time =  f"Total time taken for coverting images to pdf {(end_time - start_time) : .2f} seconds"

                    metric_file = model.get_metric(total_taken_time)
                
                    

                    resp = model.extract_and_convert_to_audio(output_file_path)

                    print(resp)

                    

                    # q = Queue(connection=Redis())
                    # q.enqueue()



                    print(f"THIS IS THE OUTPUT FILE PATH  ###### {output_file_path}")
                    
                    return Response({"status":"PDF saved successfully"})

                except Exception as e:
                    return Response({'error': str(e)}, status=500)
                finally:
                    self.remove_images(file_name)
            
            else:

                return Response({"status":"Invalid file"})
        

        elif mime_type == "application/pdf":
            
            media_dir = get_media_dir()

            input_path= os.path.join(media_dir,"Input")
            input_dir = Path(input_path)

            input_dir.mkdir(exist_ok=True)

            serializer = FileUploadSerializer(data=request.data)

            if serializer.is_valid():
                
                uploaded_file = serializer.validated_data['file']

                input_file_path = os.path.join(input_dir , uploaded_file.name)


                with open(input_file_path , 'wb+') as file:

                    for chunk in uploaded_file.chunks():
                        file.write(chunk)


                model = ModelMistral()
                media_dir = get_media_dir()

                output_path= os.path.join(media_dir,"Output")
                output_dir = Path(output_path)

                output_dir.mkdir(exist_ok=True)

                output_file_path = os.path.join(input_dir , uploaded_file.name)

                resp = model.extract_and_convert_to_audio(output_file_path)

                print(resp)


                print(f"THIS IS THE INPUT FILE PATH {input_file_path}")
                return Response({"status":"File saved successfully"})

            else:

                return Response({"status":"File is not valid"})
            


        

        