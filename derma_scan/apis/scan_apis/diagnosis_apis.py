from django.db import transaction
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
from scans.models import Diagnosis
from scans.serializers import DiagnosisSerializer


__all__ = [
    'DiagnosisListAPIView',
]

class DiagnosisListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_description="Retrieve the list of Diagnoses of the user.",
        request_body=DiagnosisSerializer,
        responses={
            200: DiagnosisSerializer,
            403: 'Forbidden: Permission denied.'
        }
    )

    def get(self, request):
        user = request.user
        if user != user:
            return Response({'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        diagnoses = Diagnosis.objects.filter(user=user)
        serializer = DiagnosisSerializer(diagnoses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)