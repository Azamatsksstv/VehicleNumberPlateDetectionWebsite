from rest_framework import serializers

from detections.models import EnteredImage, FilteredImage


class EnteredImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnteredImage
        fields = '__all__'


class FilteredImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilteredImage
        fields = '__all__'