# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    public_url = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.public_url:
            self.public_url = str(uuid4())[:8]  # Generate a unique URL if not provided
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'public_url': self.public_url})

class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdf_files/')
    public_url = models.CharField(max_length=100, blank=True, null=True)