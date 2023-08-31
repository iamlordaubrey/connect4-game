from rest_framework import serializers

from game.models import Game
from player.serializers import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = '__all__'
