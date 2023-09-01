from rest_framework import generics

from player.models import Player
from player.serializers import PlayerSerializer


class CreatePlayerView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
