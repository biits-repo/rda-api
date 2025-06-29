from django.db import models
import uuid


AUDIENCE_CHOICES = (
    ('General', 'General'),
    ('Children', 'Children'),
    ('Teen', 'Teen'),
    ('Adult', 'Adult'),
)


CATEGORY_CHOICES = (
    ('Fiction', 'Fiction'),
    ('Non-Fiction', 'Non-Fiction'),
    ('Science', 'Science'),
    ('History', 'History'),
    ('Biography', 'Biography'),
    ('Children', 'Children'),
    ('Fantasy', 'Fantasy'),
    ('Education', 'Education'),
    ('Technology', 'Technology'),
)


BOOK_TYPE_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]


class BaseBook(models.Model):
    """Model for creating a book"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    call_number = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    audience = models.CharField(max_length=50,choices=AUDIENCE_CHOICES,default='General')
    isbn = models.CharField(max_length=13)
    year_of_publication = models.PositiveBigIntegerField()
    publisher = models.CharField(max_length=100)
    overview = models.TextField()
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,default='Fiction')
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SaveAsDraft(BaseBook):
    """Model to save the book as a draft"""
    class Meta:
        db_table = 'save_as_draft'

    def save(self, *args, **kwargs):
        self.type = 'draft'
        super().save(*args, **kwargs)


class SaveAsPublished(BaseBook):
    """Model to save the book as published"""
    class Meta:
        db_table = 'save_as_published'

    def save(self, *args, **kwargs):
        self.type = 'published'
        super().save(*args, **kwargs)
