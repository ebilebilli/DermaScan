from django.urls import path

from apis.chat_message_apis.chat_message import *


app_name = 'chat_apis'

urlpatterns = [
    path(
        'chat/messages', 
        ChatMessagesListAPIView.as_view(), 
        name='chat-messages'
    ),
    path(
        'chat/message/create/', 
        CreateMessageAPIView.as_view(), 
        name='create-message'
    ),
    path(
        'chat/message/<int:message_id>/delete/', 
        DeleteMessageAPIView.as_view(), 
        name='delete-message'
    ),
 
]