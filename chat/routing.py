from django.urls import re_path

from chat import consumer 


websocket_urlpatterns = [
    re_path(r'ws/socket-server/',consumer.AsyncConsumer.as_asgi()), 
]