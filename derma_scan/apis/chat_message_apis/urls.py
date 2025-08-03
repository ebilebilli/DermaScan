from django.urls import path

from apis.chat_message_apis.chat_message import *


app_name = 'chat_apis'

urlpatterns = [
    path(
        'message/create/', 
        CreateMessageAPIView.as_view(), 
        name='create-message'
    ),
 
]