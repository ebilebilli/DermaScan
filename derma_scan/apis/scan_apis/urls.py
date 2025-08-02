from django.urls import path

from apis.scan_apis.skin_image_apis import *


app_name = 'scan_apis'

urlpatterns = [
    path(
        'upload/', 
        UploadImageAPIView.as_view(), 
        name='upload-image'
        ),
]