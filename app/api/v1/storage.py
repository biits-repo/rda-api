from django.core.files.storage import FileSystemStorage


def handle_upload_file(pdf_file):

    fs = FileSystemStorage()
    
    pdf_file.name = pdf_file.name.replace(" ","")

    filename = fs.save(pdf_file.name,pdf_file)

    file_url = fs.url(filename)
    
    return file_url