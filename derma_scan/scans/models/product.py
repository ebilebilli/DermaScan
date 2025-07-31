from django.db import models

from .diagnosis import Diagnosis


class ProductRecommendation(models.Model):
    diagnosis = models.ForeignKey(
        Diagnosis, 
        on_delete=models.CASCADE, 
        related_name="product_recommendations"
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    reason = models.TextField(
        max_length=500,
        verbose_name='Reason'
    )
    url = models.URLField(
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
   
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    