from celery import shared_task
from .models import ImageProcessingRequest, Product
from PIL import Image
from io import BytesIO
import requests
import os
from django.conf import settings

@shared_task
def process_images_task(request_id):
    processing_request = ImageProcessingRequest.objects.get(request_id=request_id)
    products = Product.objects.filter(processing_request=processing_request)

    for product in products:
        input_urls = product.input_image_urls.split(',')
        processed_urls = []

        for url in input_urls:
            response = requests.get(url.strip())
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")
            img_io = BytesIO()
            img.save(img_io, 'JPEG', quality=50)
            img_io.seek(0)

            # Create a local file path to store the image
            image_name = f'processed_{url.split("/")[-1]}'
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)

            # Save the image locally
            with open(image_path, 'wb') as f:
                f.write(img_io.getbuffer())

            # Generate the URL for the saved image
            processed_url = f"{settings.MEDIA_URL}{image_name}"
            processed_urls.append(processed_url)

        product.output_image_urls = ','.join(processed_urls)
        product.save()

    processing_request.status = 'completed'
    processing_request.save()
