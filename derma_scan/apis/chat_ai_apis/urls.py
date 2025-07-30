from django.urls import path

from apis.chat_ai_apis.chat_ai_views import *


app_name = 'chat_ai_apis'

urlpatterns = [
    path(
        'chat/request/', 
        ChatAITaskRequestAPIView.as_view(), 
        name='chat-ai-request'
        ),
    path(
        'chat/response/', 
        ChatAITaskResponseAPIView.as_view(), 
        name='chat-ai-response'
        ),
]