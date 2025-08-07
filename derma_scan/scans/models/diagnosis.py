from django.db import models

from .skin_image import SkinImage
from users.models.user import CustomerUser


class Diagnosis(models.Model):
    user = models.OneToOneField(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name='diagnosis'
    )
    image = models.OneToOneField(
        SkinImage, 
        on_delete=models.CASCADE, 
        related_name='diagnosis'
    )
    label = models.CharField(
        max_length=150,
        verbose_name='Label'
        )
    description = models.TextField(
        max_length=350
    )
    ai_response = models.TextField(
        null=True,
        blank=True
    )
    confidence = models.FloatField(
        verbose_name='Confidence'
    )  
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f'Diagnosis for {self.user.username}'

    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'