from django.urls import path

from apis.scan_apis.skin_image_apis import *
from apis.scan_apis.diagnosis_apis import *
from apis.scan_apis.product_apis import *


app_name = 'scan_apis'

urlpatterns = [
    # SkinImage endpoints
    path(
        'image/upload/', 
        UploadImageAPIView.as_view(), 
        name='upload-image'
    ),
    path(
        'image/<int:image_id>/delete/', 
        DeleteImageAPIView.as_view(), 
        name='delete-image'
    ),
    # Diagnosis endpoints
    path(
        'user/diagnoses/', 
        DiagnosisListAPIView.as_view(), 
        name='diagnoses-list'
    ),
    # Product endpoints
    path(
        'user/products/', 
        ProductRecommendationListAPIView.as_view(), 
        name='product-recommendation-list'
    )
]