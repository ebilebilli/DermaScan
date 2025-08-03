from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers.user_serializers import *
from chats.models import ChatMessage
from chats.serializers import ChatMessageSerializer
from ai.tasks import ai_response_model_task


__all__ = [
    'ChatMessagesListAPIView',
    'CreateMessageAPIView',
]

class ChatMessagesListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        user = request.user
        try :
            chats = ChatMessage.objects.filter(user=user)
            serializer = ChatMessageSerializer(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ChatMessage.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Create a new chat message and trigger AI analysis asynchronously.",
        request_body=ChatMessageSerializer,
        responses={201: ChatMessageSerializer}
    )
    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = ChatMessageSerializer(
            data=data, 
            context={'request': request}
        )
        if serializer.is_valid():
            message = serializer.save()
            ai_response_model_task(message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)