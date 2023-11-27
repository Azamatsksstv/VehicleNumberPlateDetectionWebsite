from django.db import models


class EnteredImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(upload_to='enteredImages/', null=True, blank=True)

    def __str__(self):
        return f'Entered image at {self.created_at}'


class FilteredImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(upload_to='filteredImages/')
    original_image = models.ForeignKey(EnteredImage, on_delete=models.CASCADE)
    filter_used = models.CharField(max_length=255)

    def __str__(self):
        return f'Filtered image at {self.created_at} with {self.filter_used} filter'