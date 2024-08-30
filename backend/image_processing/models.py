from django.db import models

# Create your models here.

class ImageProcessingRequest(models.Model):
    request_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Product(models.Model):
    processing_request = models.ForeignKey(ImageProcessingRequest, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    input_image_urls = models.TextField()
    output_image_urls = models.TextField(blank=True, null=True)
    
    