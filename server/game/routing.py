from django.urls import re_path, path
from game import consumers

websocket_urlpatterns = [
    # re_path(r'game/(?P<game_id>.+)/$', consumers.GameConsumer.as_asgi()),
    path('game/', consumers.GameConsumer.as_asgi()),
]
