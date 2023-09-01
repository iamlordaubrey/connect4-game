from django.db.models import Count
from rest_framework import serializers

from game.models import Game
from player.models import Player
from player.serializers import PlayerSerializer


class GameRoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        print('in serializer create game method')
        print('context should have player-id', self.context)
        # request_object = self.context['request']
        # print('dir request', dir(request_object))
        player_id = self.context['player-id']
        # player_id = self.context['request']['headers'].get('player-id')
        player = Player.objects.get(id=player_id)
        if not player:
            raise serializers.ValidationError('Player not found')

        game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
        if not game:
            game = Game.objects.create()
        game.players.add(player)

        return game


    # def get(self, request):
    #     player_id = request.headers.get('player-id')
    #     player = Player.objects.get(id=player_id)
    #     if not player:
    #         raise APIException('Player not found')
    #
    #     game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
    #     if not game:
    #         game = Game.objects.create()
    #     game.players.add(player)
    #
    #     return Response({
    #         'status': 'success',
    #         'data': {'game': GameSerializer(instance=game).data}
    #     })
