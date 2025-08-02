from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models.user import CustomerUser
from users.serializers.user_serializers import *
from chats.models import ChatMessage
from scans.models import SkinImage
from scans.serializers import SkinImageSerializer
from ai.tasks import ai_response_model_task


__all__ = [
    'UploadImageAPIView',
    'DeleteImageAPIView'
]


class UploadImageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Upload a skin image for AI-based dermatological analysis.",
        request_body=SkinImageSerializer,
        responses={201: SkinImageSerializer}
    )
    def post(self, request):
        data = request.data
        serializer = SkinImageSerializer(
            data=data, 
            context={'request': request}
        )
        if serializer.is_valid():
            image = serializer.save()
            ChatMessage.objects.create(
                sender=ChatMessage.USER,
                user=request.user,
                image=image,
                message=None  
            )

            ai_response_model_task.delay(image_id=image.id) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteImageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']
    
    @swagger_auto_schema(
        operation_description="Delete a image.",
        manual_parameters=[
            openapi.Parameter(
                'image_id',
                openapi.IN_PATH,
                description="ID of the image to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={204: 'No Content', 404: 'Not Found'}     
    )
    def delete(self, request, image_id):
        try:
            image = SkinImage.objects.get(id=image_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except SkinImage.DoesNotExist:
            return Response(
                {'message': 'Image not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        