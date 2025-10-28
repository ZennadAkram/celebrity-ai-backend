# middleware.py
import jwt
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Extract token from query string
        query_string = scope.get("query_string", b"").decode()
        token = None
        
        # Parse query string to get token
        query_params = query_string.split("&")
        for param in query_params:
            if param.startswith("token="):
                token = param.split("=")[1]
                break
        
        # Authenticate user
        scope["user"] = await self.get_user(token)
        
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        if not token:
            return AnonymousUser()
        
        try:
            # Decode and verify the token
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return AnonymousUser()