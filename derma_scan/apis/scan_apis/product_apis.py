from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.serializers.user_serializers import *
from scans.models import ProductRecommendation
from scans.serializers import ProductRecommendationSerializer


__all__ = [
    'ProductRecommendationListAPIView',
]

class ProductRecommendationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_description="Retrieve the list of Product Recommendations of the user.",
        request_body=ProductRecommendationSerializer,
        responses={
            200: ProductRecommendationSerializer,
            403: 'Forbidden: Permission denied.'
        }
    )

    def get(self, request):
        user = request.user
        if user != user:
            return Response({'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        diagnoses = ProductRecommendation.objects.filter(user=user)
        serializer = ProductRecommendationSerializer(diagnoses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)