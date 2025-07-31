from django.db import models

from .skin_image import SkinImage


class Diagnosis(models.Model):
    image = models.OneToOneField(
        SkinImage, 
        on_delete=models.CASCADE, 
        related_name='diagnosis'
    )
    result = models.CharField(
        max_length=255,
        verbose_name='Result'
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