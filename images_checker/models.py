import uuid
from django.db import models
from images_checker.images_checker import calculate_image_hash, delete_image

class Property (models.Model):
    class Meta:
        verbose_name_plural = 'properties'

    address = models.CharField(max_length=100)

class Image (models.Model):
    url = models.URLField()
    image_hash = models.CharField(
        max_length=64, 
        unique=True,
        blank=True,

    )
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='images',
    )

    def save(self, *args, **kwargs):
        if not self.image_hash:
            self.image_hash = calculate_image_hash(self.url)
        return super().save(*args, **kwargs)

    @staticmethod
    def check_and_save_image(link: str, property, *args, **kwargs) -> bool:

        file_name = '/tmp/' + uuid.uuid4().hex
        image_hash = calculate_image_hash(link, file_name)
        delete_image(file_name)

        qs = Image.objects.filter(
            property=property, 
            image_hash=image_hash,
        )

        if qs.exists() is False:
            Image.objects.create(
                property=property, 
                url=link, 
                image_hash=image_hash,
            )
            return True

        return False
