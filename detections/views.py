import os
import shutil

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src import settings
from .models import EnteredImage, FilteredImage
from .serializers import EnteredImageSerializer, FilteredImageSerializer
import cv2
from io import BytesIO
from PIL import Image


original_images_folder = 'C:\\Users\\AZAMAT\\PycharmProjects\\NumberPlateDetection\\originalimages'
number_plate_images_folder = 'C:\\Users\\AZAMAT\\PycharmProjects\\NumberPlateDetection\\numberplateimages'
haar_cascade_for_vehicle_number_plate = cv2.CascadeClassifier('C:\\Users\\AZAMAT\\PycharmProjects\\NumberPlateDetection\\cascade.xml')


class DetectNumberPlate(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_images_path = os.path.join(settings.MEDIA_ROOT, 'enteredImages')
            filtered_images_path = os.path.join(settings.MEDIA_ROOT, 'filteredImages')
            self.clear_folder(entered_images_path)
            self.clear_folder(filtered_images_path)

            entered_image = self.save_original_image(image_file)
            filtered_image = self.getting_picture_of_vehicle_number_plate(entered_image.image_file.path)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image, 'number_plate')

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def clear_folder(self, folder_path):
        # Удаляем содержимое папки
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {str(e)}")

        # Создаем пустую папку, чтобы убедиться, что она существует
        os.makedirs(folder_path, exist_ok=True)

    def getting_picture_of_vehicle_number_plate(self, image_path):
        haar_cascade = cv2.CascadeClassifier('C:\\Users\\AZAMAT\\PycharmProjects\\VehicleNumberPlateDetection\\detections\\cascade.xml')
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        number_plate_borders = haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in number_plate_borders:
            number_plate_image = image[y - 2:y + h + 2, x - 35:x + w + 35]

        pil_image = Image.fromarray(number_plate_image)

        output_buffer = BytesIO()
        pil_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        pil_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_path.split(".")[0]}_bw.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return pil_image

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def save_filtered_image(self, filtered_image, entered_image, filter_used):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used=filter_used
        )
        return filtered_image_obj
