from django.urls import path
from game import consumers

websocket_urlpatterns = [
    path('ws/socket-server/', consumers.GameConsumer.as_asgi()),
]
