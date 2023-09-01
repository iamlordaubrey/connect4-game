from django.db.models import Count
from rest_framework import serializers

from game.models import Game
from game.utils import add_to_room_event_producer, broadcast_event_producer
from player.models import Player
from player.serializers import PlayerSerializer


class GameRoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        player_id = self.context['player-id']
        player = Player.objects.get(id=player_id)
        if not player:
            raise serializers.ValidationError('Player not found')

        game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
        if game:
            game.started = True
            game.save()
            event_type = 'room.joined'
        else:
            game = Game.objects.create()
            event_type = 'room.created'

        game.players.add(player)

        room_name = f'room_{str(game.id)}'
        # add_to_room_event_producer(room_name, player.id)
        # broadcast_event_producer(room_name, event_type)

        return game
