import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageProcessingRequest, Product
from .serializers import ImageProcessingRequestSerializer
from .tasks import process_images_task
import uuid

class UploadCSV(APIView):
    def post(self, request):
        file = request.FILES['file']
        request_id = str(uuid.uuid4())
        processing_request = ImageProcessingRequest.objects.create(request_id=request_id)

        reader = csv.reader(file.read().decode('utf-8').splitlines())
        next(reader)  # Skip the header row

        for row in reader:
            Product.objects.create(
                processing_request=processing_request,
                product_name=row[1],
                input_image_urls=row[2]
            )

        process_images_task(request_id)
        return Response({"request_id": request_id}, status=status.HTTP_201_CREATED)


class CheckStatus(APIView):
    def get(self, request, request_id):
        try:
            processing_request = ImageProcessingRequest.objects.get(request_id=request_id)
            serializer = ImageProcessingRequestSerializer(processing_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ImageProcessingRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
