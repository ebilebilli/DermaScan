from django.urls import path

from apis.scan_apis.skin_image_apis import *


app_name = 'scan_apis'

urlpatterns = [
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
]