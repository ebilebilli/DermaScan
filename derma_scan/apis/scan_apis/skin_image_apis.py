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
            ai_response_model_task.delay(image_id=image.id) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
