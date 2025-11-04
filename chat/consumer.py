import json
import jwt
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import uuid

from chat.agent import  agent_chat_stream, extract_text_from_delta, get_user_and_celebrity
from chat.models import Celebrity, User

class AsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode()
        token = None
        
        if "token=" in query_string:
            token = query_string.split("token=")[1].split("&")[0] if "&" in query_string else query_string.split("token=")[1]
        
        # Authenticate user
        user = await self.get_user_from_token(token)
        if user.is_anonymous:
            await self.close()
            return
        
        # Store user in scope
        self.scope["user"] = user
        self.user_id = user.id
        self.user_group_name = f'user_{user.id}'
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        await self.accept()
       
    @database_sync_to_async
    def get_user_from_token(self, token):
        if not token:
            return AnonymousUser()
        
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return AnonymousUser()
    async def receive(self, text_data):
        if self.scope['user'].is_anonymous:
            await self.close()
            return
        data=json.loads(text_data)
        message=data['message']
        celebrity_id = data['celebrity_id']
        user=self.scope['user']
        asyncio.create_task(self.process_ai_response(message,user.id,celebrity_id))
    async def process_ai_response(self, user_message, user_id, celebrity_id):
     user, celebrity = await get_user_and_celebrity(user_id, celebrity_id)
    
     instructions = f"{celebrity.description}. You are chatting with {user.username}. Use his name in the conversation."

     token_count = 0
     message_id = str(uuid.uuid4())
    
     try:
        # 🔥 BETTER: Use a thread with proper async streaming
        def generate_tokens():
            return agent_chat_stream(user_message, instructions)
        
        # Get the generator
        token_generator = await asyncio.to_thread(generate_tokens)
        
        # 🔥 Stream tokens as they come
        for token in token_generator:
            token_count += 1
            await self.send(text_data=json.dumps({
                'type': 'ai_message', 
                'message': token,
                'message_id': message_id,
                'username': 'AI Assistant'
            }))
            await asyncio.sleep(0.03)
            
     except Exception as e:
        print(f"Error: {e}")

     await self.send(text_data=json.dumps({
        'type': 'ai_message_done',
        'message': '',
        'message_id': message_id,  
        'username': 'AI Assistant'
    }))