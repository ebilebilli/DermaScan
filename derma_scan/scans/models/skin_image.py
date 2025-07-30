from django.db import models
from datetime import datetime

from users.models import CustomerUser

class SkinImage(models.Model):
    user = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        verbose_name='User'
    )

    image = models.ImageField(
        upload_to=f'SkinImages/skin_image:{datetime.now()}',
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
