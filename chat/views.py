from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from chat.filters import CelebrityFilter
from .models import Category, User, Celebrity, ChatSession, Message
from .serializers import (
    CategorySerializer,
    UserSerializer,
    CelebritySerializer,
    ChatSessionSerializer,
    MessageSerializer
)
from chat import serializers
import os
from dotenv import load_dotenv

load_dotenv()



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = None 

    def get_permissions(self):
        """Allow anyone to create (POST), but require auth for all other actions."""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Each user only sees their own account."""
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)
        return User.objects.none()  # Prevent listing when unauthenticated

    def perform_update(self, serializer):
        """Ensure users can only update their own data."""
        user = self.request.user
        instance = self.get_object()
        if instance != user:
            raise PermissionDenied("You can only update your own account.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure users can only delete their own account."""
        user = self.request.user
        if instance != user:
            raise PermissionDenied("You can only delete your own account.")
        instance.delete()
       

from django.db.models import Q
class CelebrityViewSet(viewsets.ModelViewSet):
    queryset = Celebrity.objects.all()
    serializer_class = CelebritySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,DjangoFilterBackend]
    search_fields = ['name',]
    ordering_fields = ['name', 'created_at']
    
    filterset_class = CelebrityFilter
    def get_queryset(self):
        user = self.request.user
        queryset = Celebrity.objects.all()

        # Get query parameter value
        is_private = self.request.query_params.get('is_Private')

        # Case 1: user asks specifically for private ones
        if is_private == 'true' or is_private == 'True' or is_private == '1':
            # return only their own private ones
            return queryset.filter(is_Private=True, creator=user)

        # Case 2: user asks for public ones only
        elif is_private == 'false' or is_private == 'False' or is_private == '0':
            return queryset.filter(creator=user, is_Private=False)

        # Case 3: no filter given → return public + user's private
        return queryset.filter(Q(is_Private=False) | Q(creator=user))

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class CategoryViewSet(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
   


class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['time_stamp',]
    filterset_fields = ['celebrity',]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        # Restrict to chats of the authenticated user
        user = self.request.user
        return ChatSession.objects.filter(user=user)

from rest_framework.exceptions import PermissionDenied        

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['created_at',]
    filterset_fields = ['session',]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get session ID from request data
        session_id = self.request.data.get('session')
        
        if not session_id:
            raise serializers.ValidationError({"detail": "Session ID is required."})

        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            raise serializers.ValidationError({"detail": "Session not found."})

        # ✅ Check ownership: only the user who created the session can send messages
        if session.user != self.request.user:
            raise PermissionDenied("You can only send messages in your own sessions.")

        # ✅ Save message with sender set to the current user automatically
        serializer.save(session=session)

         # Set the sender to the authenticated user

        
    def get_queryset(self):
        # Restrict to messages of the authenticated user
        user = self.request.user

        return Message.objects.filter(session__user=user)    
    

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


from rest_framework_simplejwt.authentication import JWTAuthentication
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = [JWTAuthentication]  # <-- class, not string

    def get_response(self):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })



from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class DiscordLogin(SocialLoginView):
    adapter_class = DiscordOAuth2Adapter

    def get_response(self):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
from django.http import JsonResponse
import requests
from django.conf import settings

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_SECRET")
REDIRECT_URI = 'https://celebrity-ai-629761755982.europe-west3.run.app/auth/discord/callback/'  # must match exactly
SCOPE = 'identify email'

def discord_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    # Exchange code for access token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(
        'https://discord.com/api/oauth2/token',
        data=data,
        headers=headers
    )

    if token_response.status_code != 200:
        return JsonResponse({'error': 'Failed to get token', 'details': token_response.text}, status=token_response.status_code)

    access_token = token_response.json().get('access_token')

    # You can fetch user info now
    user_response = requests.get(
        'https://discord.com/api/users/@me',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    user_data = user_response.json()

    # Example: return user data to Flutter (or create your own token)
    return JsonResponse({
        'discord_user': user_data,
        'access_token': access_token
    })
