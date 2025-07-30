from django.urls import path

from apis.user_apis.google_views import *
from apis.user_apis.auth_views import *
from apis.user_apis.profile_views import *


app_name = 'user_apis'

urlpatterns = [
    #Google endpoints
    path(
        'google/client-id/', 
        GoogleAuthClientIDAPIView.as_view(),
        name='sign-in'
        ),
    path(
        'google/auth/',
        GoogleAuthAPIView.as_view() , 
        name='google-auth'
        ),
    # Auth endpoints
    path(
        'register/', 
        RegisterAPIView.as_view(), 
        name='register'
        ),
    path(
        'login/',
        LoginAPIView.as_view(), 
        name='login'
        ),
    path(
        'logout/', 
        LogoutAPIView.as_view(), 
        name='logout'
        ),
    # Profile endpoints
    path(
        'profile/update/', 
        ProfileUpdateAPIView.as_view(), 
        name='profile-update'
        ),
    path(
        'profile/<int:profile_id>/',
        ProfileDetailAPIView.as_view(), 
        name='profile-detail'
        ),
]