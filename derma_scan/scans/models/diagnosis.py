from django.db import models

from .skin_image import SkinImage


class Diagnosis(models.Model):
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
    
    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'