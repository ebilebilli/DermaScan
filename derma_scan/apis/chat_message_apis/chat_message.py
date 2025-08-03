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
    'DeleteMessageAPIView'
]

class ChatMessagesListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_description="Retrieve the list of chat messages sent by the user.",
        request_body=ChatMessageSerializer,
        responses={200: ChatMessageSerializer}
    )

    def get(self, request):
        user = request.user
        chats = ChatMessage.objects.filter(user=user)
        serializer = ChatMessageSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

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


class DeleteMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']
    
    @swagger_auto_schema(
        operation_description="Delete a message.",
        manual_parameters=[
            openapi.Parameter(
                'message_id',
                openapi.IN_PATH,
                description="ID of the message to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={204: 'No Content', 404: 'Not Found'}     
    )
    def delete(self, request, message_id):
        try:
            image = ChatMessage.objects.get(id=message_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except ChatMessage.DoesNotExist:
            return Response(
                {'message': 'Message not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        