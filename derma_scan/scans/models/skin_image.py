from django.db import models

from users.models import CustomerUser
from utils import skin_image_upload_path


class SkinImage(models.Model):
    user = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='User'
    )
    image = models.ImageField(
        upload_to=skin_image_upload_path,
        verbose_name='Image'
    )
    body_part = models.CharField(
        max_length=100,
        verbose_name='Body Part'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    is_analyzed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'Skin image{self.image.id} for User{self.user.id}'

    class Meta:
        verbose_name = 'Skin Image'
        verbose_name_plural = 'Skin Images'