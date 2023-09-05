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

    def _get_players_count(self, obj):
        return obj.players.count()

    def create(self, validated_data):
        player_id = self.context['player-id']
        player = Player.objects.get(id=player_id)
        if not player:
            raise serializers.ValidationError('Player not found')

        # ToDo: Use player_one and player_two
        game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
        # if game:
        #     event_type = 'room.joined'
        # else:
        #     game = Game.objects.create()
        #     event_type = 'room.created'
        print('game started should be false/None: ', game)
        if game:
            if player is not game.player_one:
                game.player_two = player
                game.save()
        else:
            game = Game.objects.create(player_one=player)

        # if not game:
        #     # game = Game.objects.create()
        #     game = Game.objects.create(player_one=player)
        # else:
        #     game.player_two = player
        #     game.save()

        game.players.add(player)
        print('in serializer ', self._get_players_count(game))
        if self._get_players_count(game) == 2:
            print('game player count is 2; serializer')
            game.started = True
            game.save()

        # room_name = f'room_{str(game.id)}'
        # add_to_room_event_producer(room_name, player.id)
        # broadcast_event_producer(room_name, event_type)

        return game
