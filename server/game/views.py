from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from game.models import Game
from game.serializers import GameSerializer
from player.models import Player


class JoinView(APIView):
    def get(self, request):
        player_id = request.headers.get('player-id')
        player = Player.objects.get(id=player_id)
        if not player:
            raise APIException('Player not found')

        game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
        if not game:
            game = Game.objects.create()
        game.players.add(player)

        return Response({
            'status': 'success',
            'data': {'game': GameSerializer(instance=game).data}
        })
