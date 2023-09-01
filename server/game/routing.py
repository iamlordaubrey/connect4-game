from django.urls import path
from game import consumers

websocket_urlpatterns = [
    path('game/', consumers.GameConsumer.as_asgi()),
]
