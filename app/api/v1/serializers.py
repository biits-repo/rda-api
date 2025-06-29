from rest_framework import serializers
from rest_framework import serializers
from .models import SaveAsDraft, SaveAsPublished


class FileCheckSerializer(serializers.Serializer):
    isbn_number = serializers.CharField(
        help_text="Provide a valid ISBN-10 (digits only).",
        required=True,
        min_length=10
    )


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text  = "Please upload the zip file " , required = True)


class BaseBookSerializer(serializers.ModelSerializer):
    call_number = serializers.CharField(required=True)
    material = serializers.CharField(required=True)
    audience = serializers.CharField(required=True)
    isbn = serializers.CharField(required=True, max_length=13)
    year_of_publication = serializers.IntegerField(required=True)
    publisher = serializers.CharField(required=True)
    overview = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    type = serializers.CharField(read_only=True)


    class Meta:
        model = SaveAsDraft
        exclude = ['id', 'created_at', 'updated_at']


class BookDraftSerializer(BaseBookSerializer):
    class Meta(BaseBookSerializer.Meta):
        model = SaveAsDraft


class BookPublishedSerializer(BaseBookSerializer):
    class Meta(BaseBookSerializer.Meta):
        model = SaveAsPublished
        