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

