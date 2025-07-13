from django.db import models
from django.core.exceptions import ValidationError
import os

# Create your models here.

def validate_file_extension(value):
    """Validate that uploaded file is PDF only"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf']
    if ext not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension {ext}. Please upload a PDF file only.'
        )

class File(models.Model):
    file = models.FileField(
        upload_to="files",
        validators=[validate_file_extension],
        help_text="Upload a PDF resume file"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name

class Form(models.Model):
      name = models.CharField(max_length=122)
      email = models.CharField(max_length=122)
      phone = models.CharField(max_length=12)
      education = models.CharField(max_length=122)
      experience = models.CharField(max_length=122)
      skills = models.CharField(max_length=122)

      def __str__(self):
        return self.name
