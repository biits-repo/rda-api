from rest_framework import serializers


class FileCheckSerializer(serializers.Serializer):
    isbn_number = serializers.CharField(
        help_text="Provide a valid ISBN-10 (digits only).",
        required=True,
        min_length=10
    )

class FileUploadSerializer(serializers.Serializer):

    file = serializers.FileField(help_text  = "Please upload the zip file " , required = True)


    
        