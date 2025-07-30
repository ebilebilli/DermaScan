from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

from users.models.user import CustomerUser


__all__ = [
    'GoogleAuthClientIDAPIView',
    'GoogleAuthAPIView'
]

class GoogleAuthClientIDAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request):
        return Response(
            {"google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID},
            status=status.HTTP_200_OK
        )
    

class GoogleAuthAPIView (APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        token = request.data.get('credential')
        if not token:
            return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_data = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID
            )
        except ValueError:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_403_FORBIDDEN)

        user, created = CustomerUser.objects.get_or_create(
            email=user_data.get('email'),
            defaults={'username': user_data.get('name')}
        )

        refresh = RefreshToken.for_user(user)
        tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

        return Response({
            'user': {
                'email': user.email,
                'username': user.username,
            },
            'tokens': tokens
        }, status=status.HTTP_200_OK
        )
